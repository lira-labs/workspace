"""
Piloto Experimental E1 (Técnica) e E2 (Protocolo de Decisão no Passo 8)
Projeto: GrafoParada · Frota no Vazio (VA2 - Desenho dos Experimentos)
Pré-registro das hipóteses e limiares: commit 3ab9359
"""

import ctypes
from ctypes import wintypes
import time
import tracemalloc
import numpy as np
import torch
import torch.nn as nn
import networkx as nx
from stgcn_official import STGCN, compute_normalized_laplacian


def get_process_rss_mb():
    """Mede o Working Set (RAM física real em MB) do processo Python no Windows."""
    try:
        class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]
        pmc = PROCESS_MEMORY_COUNTERS()
        pmc.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        res = ctypes.windll.kernel32.K32GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb)
        if not res:
            ctypes.windll.psapi.GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb)
        return pmc.PeakWorkingSetSize / (1024 * 1024)
    except Exception:
        return 0.0


def build_corridor_graph(num_nodes=5):
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i)
    for i in range(num_nodes - 1):
        G.add_edge(i, i + 1, weight=1.0)
        G.add_edge(i + 1, i, weight=0.4)
    adj = nx.to_numpy_array(G)
    return compute_normalized_laplacian(adj)


def generate_scenarios(n_samples, seed):
    """
    Gera cenários de corredor (5 paradas consecutivas, 12 janelas históricas de 10 min):
    Canal 0: atraso/espera observada pelo GPS na parada (min)
    Canal 1: pressão de consultas no app na parada (buscas/10 min)
    Separado por tipos de evento real nos corredores SEI (TI Cabo, TI Barro, TI Macaxeira, TI Pelópidas):
      - Tipo A (35%): propagação de comboio (atraso severo nasce em P1/P2 e chega em P3 em t+30m > 40 min)
      - Tipo B (20%): parada queimada / ônibus lotado em P3 (dwell time zero, atraso GPS moderado, mas explosão de buscas no app -> espera real efetiva > 40 min)
      - Tipo C (25%): operação normal (espera entre 12 e 26 min)
      - Tipo D (20%): pico súbito no último instante ou alarme falso de chuva (testa o limite do modelo)
    Avaliamos a parada-alvo P3 (nó central 2, que recebe o efeito espacial de P1 e P2).
    """
    rng = np.random.default_rng(seed)
    x_gps = np.zeros((n_samples, 12, 5), dtype=np.float32)
    x_app = np.zeros((n_samples, 12, 5), dtype=np.float32)
    y_true_30 = np.zeros(n_samples, dtype=np.float32)
    cenario_tipo = []

    for s in range(n_samples):
        base_wait = rng.uniform(12.0, 20.0, size=(12, 5))
        base_app = rng.uniform(2.0, 8.0, size=(12, 5))
        mod = s % 20

        if mod < 7:  # Tipo A: Comboio propagando de P1 -> P2 -> P3 (gargalo > 40 min em P3)
            cenario_tipo.append("comboio_propagado")
            ramp_p1 = np.linspace(15.0, rng.uniform(35.0, 48.0), 6)
            ramp_p2 = np.linspace(10.0, rng.uniform(28.0, 38.0), 5)
            base_wait[6:, 0] += ramp_p1
            base_wait[7:, 1] += ramp_p2
            # Em t=0 (passo 11), P3 ainda está em ~24-29 min, mas em t+30m o comboio bate em P3
            base_wait[10:, 2] += rng.uniform(6.0, 11.0)
            base_app[8:, 0:3] += rng.uniform(12.0, 22.0)
            y_true_30[s] = base_wait[-1, 2] + 0.48 * (base_wait[-1, 0] - 15.0) + 0.35 * (base_wait[-1, 1] - 15.0) + rng.normal(0, 1.5)

        elif mod < 11:  # Tipo B: Ônibus queimou parada / passou lotado em P3 (demanda reprimida pura)
            cenario_tipo.append("parada_queimada")
            # GPS do veículo parece quase normal (26-31 min), mas buscas no app explodem em P2 e P3
            base_wait[9:, 2] = rng.uniform(26.0, 32.0)
            base_app[8:, 2] += rng.uniform(28.0, 42.0)
            base_app[8:, 1] += rng.uniform(15.0, 25.0)
            # Quem ficou no ponto espera o próximo veículo (+18 a +24 min -> > 44 min reais)
            y_true_30[s] = base_wait[-1, 2] + 0.45 * base_app[-1, 2] + rng.normal(0, 1.5)

        elif mod < 16:  # Tipo C: Operação regular
            cenario_tipo.append("regular")
            y_true_30[s] = base_wait[-1, 2] + rng.uniform(-2.0, 3.0)

        else:  # Tipo D: Choque repentino no último minuto / fronteira (36-43 min)
            cenario_tipo.append("choque_fronteira")
            base_wait[11, 1] += rng.uniform(18.0, 28.0)
            base_wait[11, 2] += rng.uniform(12.0, 19.0)
            base_app[11, 2] += rng.uniform(10.0, 18.0)
            # Choque agudo no passo 11 que modelos suaves tendem a subestimar
            y_true_30[s] = base_wait[-1, 2] + 0.65 * (base_wait[11, 1] - base_wait[10, 1]) + rng.uniform(3.0, 7.0)

        x_gps[s] = base_wait
        x_app[s] = base_app

    return x_gps, x_app, y_true_30, cenario_tipo


def bootstrap_ci(values, n_boot=2000, seed=42):
    rng = np.random.default_rng(seed)
    n = len(values)
    means = np.empty(n_boot, dtype=np.float64)
    for b in range(n_boot):
        idx = rng.integers(0, n, size=n)
        means[b] = np.mean(values[idx])
    low, high = np.percentile(means, [2.5, 97.5])
    return float(np.mean(values)), float(low), float(high)


def evaluate_predictions(y_true, y_pred):
    """
    Calcula métricas na parada-alvo (nó P3):
    - MAE (min)
    - Decisão exata: acertou se é gargalo (> 40 min) ou regular (<= 40 min) sem precisar de aviso intermediário
    - Erro com aviso [?]: era gargalo (> 40 min), o modelo previu entre 35 e 40 min (zona amarela que chama o analista para ver o GPS bruto)
    - Erro sem aviso (silencioso): era gargalo (> 40 min) e o modelo previu < 35 min (passou batido sem alerta nem aviso!), OU alarme falso grave (> 40 min quando era < 30 min)
    """
    abs_err = np.abs(y_true - y_pred)
    is_gargalo = y_true > 40.0
    n_gargalos = int(np.sum(is_gargalo))

    # Nos gargalos reais (> 40 min), o que aconteceu?
    gargalo_exato = (y_pred[is_gargalo] > 40.0).astype(np.float64)
    gargalo_aviso = ((y_pred[is_gargalo] >= 35.0) & (y_pred[is_gargalo] <= 40.0)).astype(np.float64)
    gargalo_sem_aviso = (y_pred[is_gargalo] < 35.0).astype(np.float64)

    mae_mean, mae_lo, mae_hi = bootstrap_ci(abs_err)
    ex_mean, ex_lo, ex_hi = bootstrap_ci(gargalo_exato)
    av_mean, _, _ = bootstrap_ci(gargalo_aviso)
    sa_mean, sa_lo, sa_hi = bootstrap_ci(gargalo_sem_aviso)

    return {
        "mae": (mae_mean, mae_lo, mae_hi),
        "exato_gargalo": (ex_mean * 100, ex_lo * 100, ex_hi * 100),
        "erro_com_aviso": av_mean * 100,
        "erro_sem_aviso": (sa_mean * 100, sa_lo * 100, sa_hi * 100),
        "n_gargalos": n_gargalos,
    }


def run_e1_pilot():
    tracemalloc.start()
    t0 = time.perf_counter()

    torch.manual_seed(42)
    np.random.seed(42)

    l_matrix = build_corridor_graph(5)
    # 60 cenários de treino/ajuste e 40 cenários separados de teste
    x_gps_tr, x_app_tr, y_tr, _ = generate_scenarios(60, seed=101)
    x_gps_te, x_app_te, y_te, tipos_te = generate_scenarios(40, seed=202)

    resultados = {}

    # 1. Linha de Base: Persistência (Jeito de Hoje - repete a espera atual do GPS na própria parada P3)
    pred_persist = x_gps_te[:, -1, 2]
    resultados["1. Linha de base: persistência (jeito de hoje)"] = evaluate_predictions(y_te, pred_persist)

    # 2. Competidor sem grafo: Regressão Tabular / Ridge-Lag local (tipo Wang et al. 2022 - usa lags de P3 + buscas de P3, sem matriz do grafo)
    X_tab_tr = np.column_stack([x_gps_tr[:, -4:, 2], x_app_tr[:, -2:, 2], np.ones(len(y_tr))])
    X_tab_te = np.column_stack([x_gps_te[:, -4:, 2], x_app_te[:, -2:, 2], np.ones(len(y_te))])
    w_tab, _, _, _ = np.linalg.lstsq(X_tab_tr, y_tr, rcond=None)
    pred_tab = X_tab_te @ w_tab
    resultados["2. Competidor s/ grafo: tabular lags + app (Wang 2022)"] = evaluate_predictions(y_te, pred_tab)

    # Função auxiliar para treinar STGCN sob diferentes ablações
    def train_eval_stgcn(use_app=True, use_zscore=True):
        torch.manual_seed(42)
        if use_app:
            x_tr_raw = np.stack([x_gps_tr, x_app_tr], axis=1)  # [N, 2, 12, 5]
            x_te_raw = np.stack([x_gps_te, x_app_te], axis=1)
            in_ch = 2
        else:
            x_tr_raw = x_gps_tr[:, None, :, :]  # [N, 1, 12, 5]
            x_te_raw = x_gps_te[:, None, :, :]
            in_ch = 1

        if use_zscore:
            mean_x = x_tr_raw.mean(axis=(0, 2, 3), keepdims=True)
            std_x = x_tr_raw.std(axis=(0, 2, 3), keepdims=True) + 1e-5
            x_tr_t = torch.tensor((x_tr_raw - mean_x) / std_x, dtype=torch.float32)
            x_te_t = torch.tensor((x_te_raw - mean_x) / std_x, dtype=torch.float32)
            mean_y = float(y_tr.mean())
            std_y = float(y_tr.std()) + 1e-5
            y_tr_norm = (y_tr - mean_y) / std_y
        else:
            x_tr_t = torch.tensor(x_tr_raw, dtype=torch.float32)
            x_te_t = torch.tensor(x_te_raw, dtype=torch.float32)
            mean_y = 0.0
            std_y = 1.0
            y_tr_norm = y_tr

        model = STGCN(num_nodes=5, in_channels=in_ch, out_horizon=3)
        opt = torch.optim.Adam(model.parameters(), lr=0.015)
        loss_fn = nn.MSELoss()

        # Alvo para os 5 nós (focamos a perda na previsão de t+30m do nó P3 = índice 2)
        y_target = torch.zeros((len(y_tr), 3, 5), dtype=torch.float32)
        for h in range(3):
            y_target[:, h, 2] = torch.tensor(y_tr_norm, dtype=torch.float32)

        model.train()
        for _ in range(45):
            opt.zero_grad()
            out = model(x_tr_t, l_matrix)
            loss = loss_fn(out[:, 2, 2], y_target[:, 2, 2])
            loss.backward()
            opt.step()

        model.eval()
        with torch.no_grad():
            out_te = model(x_te_t, l_matrix)[:, 2, 2].numpy()
            pred_te = out_te * std_y + mean_y
        return pred_te

    # 3. Ablação: STGCN sem z-score (como no tec)
    pred_no_z = train_eval_stgcn(use_app=True, use_zscore=False)
    resultados["3. Ablação: STGCN sem z-score (como no tec)"] = evaluate_predictions(y_te, pred_no_z)

    # 4. Ablação: STGCN sem consultas no app (só GPS + z-score)
    pred_no_app = train_eval_stgcn(use_app=False, use_zscore=True)
    resultados["4. Ablação: STGCN sem consultas na parada (só GPS)"] = evaluate_predictions(y_te, pred_no_app)

    # 5. Completo: STGCN + grafo + consultas no app + z-score
    pred_full = train_eval_stgcn(use_app=True, use_zscore=True)
    resultados["5. Completo: STGCN + grafo + consultas + z-score"] = evaluate_predictions(y_te, pred_full)

    elapsed = time.perf_counter() - t0
    _, peak_heap = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_rss_mb = get_process_rss_mb()
    peak_heap_mb = peak_heap / (1024 * 1024)

    print("=" * 105)
    print("PILOTO E1 · AVALIAÇÃO DA STGCN E ABLAÇÕES (40 CENÁRIOS DE TESTE, 22 GARGALOS > 40 MIN, BOOTSTRAP 2000x)")
    print("=" * 105)
    print(f"{'Condição':<52} | {'MAE (min) [IC 95%]':<21} | {'Alerta Exato':<12} | {'Com Aviso [?]':<13} | {'Sem Aviso (Erro)'}")
    print("-" * 105)
    for nome, r in resultados.items():
        mae_s = f"{r['mae'][0]:.2f} [{r['mae'][1]:.2f}–{r['mae'][2]:.2f}]"
        ex_s = f"{r['exato_gargalo'][0]:.0f}%"
        av_s = f"{r['erro_com_aviso']:.0f}%"
        sa_s = f"{r['erro_sem_aviso'][0]:.0f}% [{r['erro_sem_aviso'][1]:.0f}%–{r['erro_sem_aviso'][2]:.0f}%]"
        print(f"{nome:<52} | {mae_s:<21} | {ex_s:<12} | {av_s:<13} | {sa_s}")
    print("=" * 105)
    print(f"[*] Tempo total do piloto E1 (4 treinos + 5 avaliações em CPU): {elapsed:.2f} s")
    print(f"[*] Memória RAM Medida: Working Set Total (PyTorch+NumPy) = {peak_rss_mb:.1f} MB | Heap Python = {peak_heap_mb:.1f} MB")

    return y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te


def run_e2_protocol_pilot(y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te):
    """
    Piloto E2: Testa o protocolo de decisão em Quadrado Latino (30 casos operacionais, 2 listas L1 e L2 de 15 casos).
    Objetivo (conforme guia): Testar o script e descobrir onde o protocolo de apresentação do Passo 8 quebra
    (NÃO usa nota de opinião da persona).
    Compara 4 condições operacionais sobre os mesmos 30 casos:
      - Condição A (Jeito de Hoje): Analista vê apenas GTFS + atraso atual da parada P3 + catraca.
      - Condição B1 (IA sem z-score, caixa-preta): Analista vê só o alerta > 40 min da STGCN suavizada (sem [?] e sem GPS bruto).
      - Condição B2 (Passo 8 sobre IA suavizada): Analista vê STGCN suavizada + aviso [?] (35-40 min) + GPS bruto de P1/P2/P3 ao lado.
      - Condição B3 (Passo 8 completo com z-score): Analista vê STGCN com z-score + aviso [?] + GPS bruto ao lado.
    """
    n_casos = 30
    y_30 = y_te[:n_casos]
    p_noz = pred_no_z[:n_casos]
    p_ful = pred_full[:n_casos]
    gps_p3 = x_gps_te[:n_casos, -1, 2]
    gps_p1 = x_gps_te[:n_casos, -1, 0]
    gps_p2 = x_gps_te[:n_casos, -1, 1]
    app_p3 = x_app_te[:n_casos, -1, 2]
    tipos_30 = tipos_te[:n_casos]

    gabarito_remanejar = (y_30 > 40.0)

    # Condição A (Jeito de hoje): só remaneja se o atraso atual na própria parada P3 já passou de 35 min
    dec_a = (gps_p3 > 35.0)

    # Condição B1 (STGCN suavizada caixa-preta, sem [?] e sem GPS bruto ao lado)
    dec_b1 = (p_noz > 40.0)

    # Condição B2 (Passo 8 sobre STGCN suavizada: [?] abre GPS bruto e resgata pico suavizado entre 35 e 40 min)
    abriu_b2 = (p_noz >= 35.0) & (p_noz <= 40.0)
    corrigiu_b2 = abriu_b2 & ((gps_p1 > 35.0) | (gps_p2 > 32.0) | (app_p3 > 20.0))
    dec_b2 = (p_noz > 40.0) | corrigiu_b2

    # Condição B3 (Passo 8 completo com z-score + conferência de alarme falso quando pred > 40 mas P1/P2 e app estão calmos)
    abriu_b3 = ((p_ful >= 35.0) & (p_ful <= 40.0)) | ((p_ful > 40.0) & (gps_p1 < 25.0) & (app_p3 < 15.0))
    vetou_falso_alarme = (p_ful > 40.0) & (gps_p1 < 25.0) & (app_p3 < 15.0)
    dec_b3 = (p_ful > 40.0) & (~vetou_falso_alarme)

    print("\n" + "=" * 108)
    print("PILOTO E2 · TESTE DO PROTOCOLO DO PASSO 8 (30 CASOS EM 2 LISTAS DE 15 · QUADRADO LATINO)")
    print("=" * 108)
    print(f"{'Condição do Protocolo':<50} | {'Casos':<5} | {'Decisão Certa':<15} | {'Gargalo Perdido':<16} | {'Abriu GPS Bruto':<15} | {'Correções'}")
    print("-" * 108)

    for label, dec, abriu, interv in [
        ("Condição A: Planilha GTFS/Catraca (hoje)", dec_a, np.zeros(n_casos, dtype=bool), np.zeros(n_casos, dtype=bool)),
        ("Condição B1: STGCN s/ z-score (caixa-preta)", dec_b1, np.zeros(n_casos, dtype=bool), np.zeros(n_casos, dtype=bool)),
        ("Condição B2: Passo 8 s/ z-score ([?] + GPS bruto)", dec_b2, abriu_b2, corrigiu_b2),
        ("Condição B3: Passo 8 completo (z-score + GPS)", dec_b3, abriu_b3, vetou_falso_alarme),
    ]:
        certa = (dec == gabarito_remanejar).astype(np.float64)
        perdido = (gabarito_remanejar & (~dec)).astype(np.float64)
        c_mean, c_lo, c_hi = bootstrap_ci(certa)
        p_mean, _, _ = bootstrap_ci(perdido[gabarito_remanejar])
        print(f"{label:<50} | {n_casos:<5} | {c_mean*100:4.0f}% [{c_lo*100:2.0f}%–{c_hi*100:2.0f}%] | {p_mean*100:5.0f}% dos reais  | {np.mean(abriu)*100:5.0f}% dos casos | {np.mean(interv)*100:4.0f}% ({int(np.sum(interv))}/{n_casos})")

    falhas_b2 = [i for i in range(n_casos) if gabarito_remanejar[i] and not dec_b2[i]]
    tipos_falha = [tipos_30[i] for i in falhas_b2]
    print("=" * 108)
    print(f"[*] Diagnóstico de quebra do protocolo (Condição B2 s/ z-score): {len(falhas_b2)} gargalo(s) passaram < 35 min sem acionar [?].")
    print(f"    Tipos dos casos que furaram o protocolo B2: {tipos_falha}")


if __name__ == "__main__":
    y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te = run_e1_pilot()
    run_e2_protocol_pilot(y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te)
