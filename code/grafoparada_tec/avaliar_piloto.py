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
    """Mede o Working Set (RAM física total C++/LibTorch + Python em MB) no Windows 64-bit."""
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
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.K32GetProcessMemoryInfo.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    kernel32.K32GetProcessMemoryInfo.restype = wintypes.BOOL
    handle = kernel32.GetCurrentProcess()
    if kernel32.K32GetProcessMemoryInfo(handle, ctypes.byref(pmc), pmc.cb):
        return pmc.PeakWorkingSetSize / (1024 * 1024)
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
    Inclui interação não linear entre comboio (P1/P2) e retenção na parada (P3) + ruído realista.
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
            ramp_p1 = np.linspace(12.0, rng.uniform(32.0, 44.0), 6)
            ramp_p2 = np.linspace(8.0, rng.uniform(24.0, 34.0), 5)
            base_wait[6:, 0] += ramp_p1
            base_wait[7:, 1] += ramp_p2
            base_wait[10:, 2] += rng.uniform(5.0, 10.0)
            base_app[8:, 0:3] += rng.uniform(12.0, 22.0)
            # Propagação não linear (efeito cascata quando P1 e P2 atrasam juntos)
            efeito_cascata = 0.42 * (base_wait[-1, 0] - 15.0) + 0.35 * (base_wait[-1, 1] - 15.0)
            y_true_30[s] = base_wait[-1, 2] + efeito_cascata + rng.normal(0, 2.5)

        elif mod < 11:  # Tipo B: Ônibus queimou parada / passou lotado em P3
            cenario_tipo.append("parada_queimada")
            base_wait[9:, 2] = rng.uniform(26.0, 31.0)
            base_app[8:, 2] += rng.uniform(24.0, 38.0)
            base_app[8:, 1] += rng.uniform(12.0, 22.0)
            y_true_30[s] = base_wait[-1, 2] + 0.42 * base_app[-1, 2] + rng.normal(0, 2.5)

        elif mod < 16:  # Tipo C: Operação regular (12 a 28 min)
            cenario_tipo.append("regular")
            y_true_30[s] = base_wait[-1, 2] + rng.uniform(-2.0, 4.0)

        else:  # Tipo D: Choque repentino de fronteira (36 a 43 min) - testa zona [?] (35-40 min) e falsos alarmes
            cenario_tipo.append("choque_fronteira")
            base_wait[11, 1] += rng.uniform(15.0, 25.0)
            base_wait[11, 2] += rng.uniform(11.0, 17.0)
            base_app[11, 2] += rng.uniform(10.0, 18.0)
            y_true_30[s] = base_wait[-1, 2] + 0.55 * (base_wait[11, 1] - base_wait[10, 1]) + rng.normal(2.0, 3.0)

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
    - MAE (min) em todos os 40 cenários
    - Nos gargalos reais (y_true > 40 min):
      * Alerta Exato: previu > 40 min
      * Com Aviso [?]: previu entre 35 e 40 min (chama conferência do GPS bruto no Passo 8)
      * Erro Sem Aviso (falso negativo silencioso): previu < 35 min quando era > 40 min
    - Nos cenários sem gargalo (y_true <= 40 min):
      * Alarme Falso (falso positivo): previu > 40 min quando a espera real era <= 40 min
    """
    abs_err = np.abs(y_true - y_pred)
    is_gargalo = y_true > 40.0
    is_normal = ~is_gargalo

    gargalo_exato = (y_pred[is_gargalo] > 40.0).astype(np.float64)
    gargalo_aviso = ((y_pred[is_gargalo] >= 35.0) & (y_pred[is_gargalo] <= 40.0)).astype(np.float64)
    gargalo_sem_aviso = (y_pred[is_gargalo] < 35.0).astype(np.float64)
    falso_alarme = (y_pred[is_normal] > 40.0).astype(np.float64)

    mae_mean, mae_lo, mae_hi = bootstrap_ci(abs_err)
    ex_mean, _, _ = bootstrap_ci(gargalo_exato)
    av_mean, _, _ = bootstrap_ci(gargalo_aviso)
    sa_mean, sa_lo, sa_hi = bootstrap_ci(gargalo_sem_aviso)
    fa_mean, _, _ = bootstrap_ci(falso_alarme)

    return {
        "mae": (mae_mean, mae_lo, mae_hi),
        "exato_gargalo": ex_mean * 100,
        "erro_com_aviso": av_mean * 100,
        "erro_sem_aviso": (sa_mean * 100, sa_lo * 100, sa_hi * 100),
        "falso_alarme": fa_mean * 100,
        "n_gargalos": int(np.sum(is_gargalo)),
    }


def run_e1_pilot():
    tracemalloc.start()
    t0 = time.perf_counter()

    torch.manual_seed(42)
    np.random.seed(42)

    l_matrix = build_corridor_graph(5)
    x_gps_tr, x_app_tr, y_tr, _ = generate_scenarios(60, seed=101)
    x_gps_te, x_app_te, y_te, tipos_te = generate_scenarios(40, seed=202)

    resultados = {}

    # 1. Linha de Base: Persistência (Jeito de Hoje - repete a espera atual do GPS na própria parada P3)
    pred_persist = x_gps_te[:, -1, 2]
    resultados["1. Linha de base: persistência (jeito de hoje)"] = evaluate_predictions(y_te, pred_persist)

    # 2a. Competidor s/ grafo local: Regressão Tabular só na parada P3 (tipo Wang et al. 2022 local)
    X_tab_tr = np.column_stack([x_gps_tr[:, -4:, 2], x_app_tr[:, -2:, 2], np.ones(len(y_tr))])
    X_tab_te = np.column_stack([x_gps_te[:, -4:, 2], x_app_te[:, -2:, 2], np.ones(len(y_te))])
    w_tab, _, _, _ = np.linalg.lstsq(X_tab_tr, y_tr, rcond=None)
    pred_tab = X_tab_te @ w_tab
    resultados["2a. Competidor tabular local (só P3 + app)"] = evaluate_predictions(y_te, pred_tab)

    # 2b. Competidor s/ grafo espacial: Regressão Tabular com lags de P1, P2 e P3 achatados (sem matriz Laplaciana)
    X_all_tr = np.column_stack([x_gps_tr[:, -2:, 0:3].reshape(len(y_tr), -1), x_app_tr[:, -2:, 2], np.ones(len(y_tr))])
    X_all_te = np.column_stack([x_gps_te[:, -2:, 0:3].reshape(len(y_te), -1), x_app_te[:, -2:, 2], np.ones(len(y_te))])
    w_all, _, _, _ = np.linalg.lstsq(X_all_tr, y_tr, rcond=None)
    pred_all_tab = X_all_te @ w_all
    resultados["2b. Competidor tabular corredor (P1+P2+P3 + app)"] = evaluate_predictions(y_te, pred_all_tab)

    def train_eval_stgcn(use_app=True, use_zscore=True):
        torch.manual_seed(42)
        if use_app:
            x_tr_raw = np.stack([x_gps_tr, x_app_tr], axis=1)
            x_te_raw = np.stack([x_gps_te, x_app_te], axis=1)
            in_ch = 2
        else:
            x_tr_raw = x_gps_tr[:, None, :, :]
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

    # 4. Ablação: STGCN sem consultas na parada (só GPS + z-score)
    pred_no_app = train_eval_stgcn(use_app=False, use_zscore=True)
    resultados["4. Ablação: STGCN sem consultas na parada (só GPS)"] = evaluate_predictions(y_te, pred_no_app)

    # 5. Completo: STGCN + grafo + consultas + z-score
    pred_full = train_eval_stgcn(use_app=True, use_zscore=True)
    resultados["5. Completo: STGCN + grafo + consultas + z-score"] = evaluate_predictions(y_te, pred_full)

    elapsed = time.perf_counter() - t0
    _, peak_heap = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_rss_mb = get_process_rss_mb()
    peak_heap_mb = peak_heap / (1024 * 1024)

    n_garg = resultados["5. Completo: STGCN + grafo + consultas + z-score"]["n_gargalos"]
    print("=" * 116)
    print(f"PILOTO E1 · AVALIAÇÃO DA STGCN E ABLAÇÕES (40 CENÁRIOS DE TESTE, {n_garg} GARGALOS > 40 MIN, BOOTSTRAP 2000x)")
    print("=" * 116)
    print(f"{'Condição':<50} | {'MAE (min) [IC 95%]':<20} | {'Exato':<6} | {'Aviso [?]':<9} | {'Sem Aviso (FN)':<16} | {'Alarme Falso'}")
    print("-" * 116)
    for nome, r in resultados.items():
        mae_s = f"{r['mae'][0]:.2f} [{r['mae'][1]:.2f}–{r['mae'][2]:.2f}]"
        ex_s = f"{r['exato_gargalo']:.0f}%"
        av_s = f"{r['erro_com_aviso']:.0f}%"
        sa_s = f"{r['erro_sem_aviso'][0]:.0f}% [{r['erro_sem_aviso'][1]:.0f}%–{r['erro_sem_aviso'][2]:.0f}%]"
        fa_s = f"{r['falso_alarme']:.0f}%"
        print(f"{nome:<50} | {mae_s:<20} | {ex_s:<6} | {av_s:<9} | {sa_s:<16} | {fa_s}")
    print("=" * 116)
    print(f"[*] Tempo total do piloto E1 (4 treinos + 6 avaliações em CPU): {elapsed:.2f} s")
    print(f"[*] Memória RAM Medida: Working Set Total (C++/LibTorch + Python) = {peak_rss_mb:.1f} MB | Heap Python = {peak_heap_mb:.1f} MB")

    return y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te


def run_e2_protocol_pilot(y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te):
    """
    Piloto E2: Testa o protocolo de decisão em Quadrado Latino (30 casos operacionais, 2 listas L1 e L2 de 15 casos).
    Nota metodológica: Humanos no estudo completo testam APENAS 2 condições (Condição A: Planilha vs. Condição B3: Passo 8 Completo).
    As condições B1 e B2 são ablações computacionais offline para isolar o efeito do [?] e do z-score.
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

    # Condição A (Jeito de hoje - testada com humanos): só remaneja se o atraso atual na própria parada P3 já passou de 35 min
    dec_a = (gps_p3 > 35.0)

    # Condição B1 (Ablação offline: STGCN s/ z-score caixa-preta)
    dec_b1 = (p_noz > 40.0)

    # Condição B2 (Ablação offline: Passo 8 sobre STGCN s/ z-score)
    abriu_b2 = (p_noz >= 35.0) & (p_noz <= 40.0)
    corrigiu_b2 = abriu_b2 & ((gps_p1 > 32.0) | (gps_p2 > 28.0) | (app_p3 > 20.0))
    dec_b2 = (p_noz > 40.0) | corrigiu_b2

    # Condição B3 (Passo 8 completo com z-score - testada com humanos):
    # Aciona aviso [?] quando pred está entre 35 e 40 min, permitindo ao analista checar GPS bruto de P1/P2 e app
    abriu_b3 = (p_ful >= 35.0) & (p_ful <= 40.0)
    corrigiu_b3 = abriu_b3 & ((gps_p1 > 32.0) | (gps_p2 > 28.0) | (app_p3 > 20.0))
    dec_b3 = (p_ful > 40.0) | corrigiu_b3

    print("\n" + "=" * 116)
    print("PILOTO E2 · TESTE DO PROTOCOLO DO PASSO 8 (30 CASOS EM 2 LISTAS DE 15 · QUADRADO LATINO)")
    print("=" * 116)
    print(f"{'Condição do Protocolo':<52} | {'Casos':<5} | {'Decisão Certa':<15} | {'Gargalo Perdido':<16} | {'Abriu GPS [?]':<14} | {'Correções'}")
    print("-" * 116)

    for label, dec, abriu, interv in [
        ("Condição A (Humano): Planilha GTFS/Catraca (hoje)", dec_a, np.zeros(n_casos, dtype=bool), np.zeros(n_casos, dtype=bool)),
        ("Condição B1 (Offline): STGCN s/ z-score caixa-preta", dec_b1, np.zeros(n_casos, dtype=bool), np.zeros(n_casos, dtype=bool)),
        ("Condição B2 (Offline): Passo 8 s/ z-score + GPS", dec_b2, abriu_b2, corrigiu_b2),
        ("Condição B3 (Humano): Passo 8 completo (z-score+GPS)", dec_b3, abriu_b3, corrigiu_b3),
    ]:
        certa = (dec == gabarito_remanejar).astype(np.float64)
        perdido = (gabarito_remanejar & (~dec)).astype(np.float64)
        c_mean, c_lo, c_hi = bootstrap_ci(certa)
        p_mean, _, _ = bootstrap_ci(perdido[gabarito_remanejar])
        print(f"{label:<52} | {n_casos:<5} | {c_mean*100:4.0f}% [{c_lo*100:2.0f}%–{c_hi*100:2.0f}%] | {p_mean*100:5.0f}% dos reais  | {np.mean(abriu)*100:5.0f}% dos casos | {np.mean(interv)*100:4.0f}% ({int(np.sum(interv))}/{n_casos})")

    falhas_b3 = [i for i in range(n_casos) if gabarito_remanejar[i] and not dec_b3[i]]
    tipos_falha_b3 = [tipos_30[i] for i in falhas_b3]
    print("=" * 116)
    print(f"[*] Diagnóstico de quebra do protocolo (Condição B3): {len(falhas_b3)} gargalo(s) passaram < 35 min sem acionar [?]: {tipos_falha_b3}")


if __name__ == "__main__":
    y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te = run_e1_pilot()
    run_e2_protocol_pilot(y_te, pred_full, pred_no_z, x_gps_te, x_app_te, tipos_te)
