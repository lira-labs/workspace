# -*- coding: utf-8 -*-
"""
Medicao Reprodutivel de Custo e Falha Real · Seminario 2 (AI4Good / UFRPE).
Execucao:
    uv run --project code/grafoparada_tec python code/grafoparada_tec/medir_custo_sem2.py
"""

from __future__ import annotations

import platform
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

TEC_DIR = Path(__file__).resolve().parent
if str(TEC_DIR) not in sys.path:
    sys.path.insert(0, str(TEC_DIR))

from avaliar_piloto import get_process_rss_mb
from modelo_predicao_e_abandono import avaliar_trava_hibrida_defensiva
from motor_evolucao_prototipo import KinematicStopFSM_V3
from stgcn_official import STGCN, compute_normalized_laplacian

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def detectar_cpu_nome() -> str:
    try:
        out = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).Name"],
            text=True,
            timeout=5,
        ).strip()
        if out:
            return out
    except Exception:
        pass
    return platform.processor() or platform.machine()


def main() -> None:
    torch.manual_seed(42)
    rng = np.random.default_rng(42)

    cpu_nome = detectar_cpu_nome()
    print("=" * 80)
    print("  AUDITORIA DE CUSTO E FALHA REAL · SEM2 (AI4GOOD / UFRPE)")
    print("=" * 80)
    print(f"  Maquina: {cpu_nome} | SO: {platform.system()} {platform.release()}")
    print(f"  Runtime: Python {platform.python_version()} | PyTorch {torch.__version__} (CPU)")

    # --------------------------------------------------------------------------
    # 1. MEDICAO ON-DEVICE: FSM CINEMATICA V3 (EXCLUINDO IMPORT DE MODULOS)
    # --------------------------------------------------------------------------
    fsm = KinematicStopFSM_V3()
    steps = []
    for i in range(15):
        dist = 10.0 if i < 10 else 150.0 + (i - 10) * 80.0
        elapsed = float(i) * 0.5
        probs = np.array([0.7, 0.2, 0.05, 0.05]) if i < 10 else np.array([0.05, 0.05, 0.1, 0.8])
        steps.append({
            "distance_to_stop_m": dist,
            "elapsed_min": elapsed,
            "probs": probs,
            "state": "Still" if i < 10 else "Car",
        })

    # Warmup fora da janela de medicao
    _ = fsm.processar(steps, official_bus_at_stop=False, stopped_at_next_gtfs_stop=False)

    tracemalloc.start()
    t0_fsm = time.perf_counter()
    n_fsm_iters = 500
    decision = "UNKNOWN"
    for _ in range(n_fsm_iters):
        decision = fsm.processar(steps, official_bus_at_stop=False, stopped_at_next_gtfs_stop=False)
    t_fsm = (time.perf_counter() - t0_fsm) / n_fsm_iters
    _, peak_fsm_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print("\n[1. ON-DEVICE / CELULAR - FSM CINEMATICA V3]")
    print(f"  - Decisao na trajetoria de desistencia: {decision}")
    print(f"  - Tempo medio por inferencia ({n_fsm_iters}x): {t_fsm * 1e6:.2f} us ({t_fsm * 1e3:.4f} ms)")
    print(f"  - Pico de heap Python por ciclo (tracemalloc): {peak_fsm_bytes / 1024:.2f} KB")
    print("  - Estimativa no flx.md: 14,29 us (passo unico) e 8,92 KB de RAM (validar_cinematica_parada.py)")

    # --------------------------------------------------------------------------
    # 2. MEDICAO SERVIDOR / BACKEND: STGCN PYTORCH (20 NOS DA PE-60)
    # --------------------------------------------------------------------------
    num_nodes = 20
    adj = np.zeros((num_nodes, num_nodes), dtype=np.float32)
    for i in range(num_nodes - 1):
        adj[i, i + 1] = 1.0
        adj[i + 1, i] = 1.0
    l_norm = compute_normalized_laplacian(adj)

    # Gera 64 janelas sinteticas de corredor normal + ondas suaves para treinar 25 epocas
    n_train = 64
    x_raw = rng.normal(loc=10.0, scale=2.5, size=(n_train, 1, 12, num_nodes)).astype(np.float32)
    for s in range(n_train):
        if s % 2 == 0:
            wave_center = int(rng.integers(4, 15))
            amp = float(rng.uniform(4.0, 12.0))
            for k in range(-2, 3):
                idx = max(0, min(num_nodes - 1, wave_center + k))
                x_raw[s, 0, 8:, idx] += amp * max(0.2, 1.0 - 0.25 * abs(k))
    y_raw = np.stack([
        x_raw[:, 0, -1, :] * 0.9 + 1.0,
        x_raw[:, 0, -1, :] * 0.92 + 0.8,
        x_raw[:, 0, -1, :] * 0.95 + 0.5,
    ], axis=1).astype(np.float32)

    mean_v = float(x_raw.mean())
    std_v = float(x_raw.std()) + 1e-5
    x_train_t = torch.tensor((x_raw - mean_v) / std_v, dtype=torch.float32)
    y_train_t = torch.tensor((y_raw - mean_v) / std_v, dtype=torch.float32)

    model = STGCN(num_nodes=num_nodes, in_channels=1, out_horizon=3)
    num_params = sum(p.numel() for p in model.parameters())
    opt = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    t0_train = time.perf_counter()
    model.train()
    for _ in range(25):
        opt.zero_grad()
        pred_tr = model(x_train_t, l_norm)
        loss = loss_fn(pred_tr, y_train_t)
        loss.backward()
        opt.step()
    t_train_25 = time.perf_counter() - t0_train

    model.eval()
    x_in = torch.zeros(1, 1, 12, num_nodes, dtype=torch.float32)
    with torch.no_grad():
        _ = model(x_in, l_norm)

    tracemalloc.start()
    t0_infer = time.perf_counter()
    n_stgcn_iters = 200
    with torch.no_grad():
        for _ in range(n_stgcn_iters):
            out = model(x_in, l_norm)
    t_infer_stgcn = (time.perf_counter() - t0_infer) / n_stgcn_iters
    _, peak_stgcn_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rss_peak_mb = get_process_rss_mb()

    print("\n[2. SERVIDOR / STGCN 20 NOS PE-60 (CPU PYTORCH)]")
    print(f"  - Parametros treinaveis: {num_params:,}")
    print(f"  - Saida predita (horizontes t+10, t+20, t+30): shape {list(out.shape)}")
    print(f"  - Tempo de treino (25 epocas, {n_train} amostras): {t_train_25:.2f} s")
    print(f"  - Tempo medio por inferencia completa em CPU ({n_stgcn_iters}x): {t_infer_stgcn * 1e3:.2f} ms")
    print(f"  - Heap Python na inferencia (tracemalloc): {peak_stgcn_bytes / 1024:.2f} KB ({peak_stgcn_bytes / (1024 * 1024):.3f} MB)")
    print(f"  - Pico de Working Set fisico total (C++/LibTorch + Python): {rss_peak_mb:.1f} MB")
    print("  - Estimado no flx.md: < 10 s (treino 25 epocas + inferencia); < 0,5 s (inferencia) e ~300 MB de RAM")

    # --------------------------------------------------------------------------
    # 3. CASO DE FALHA REAL: CHOQUE PONTUAL DE 45 MIN NO NO 10 (TREVO IPOJUCA)
    # --------------------------------------------------------------------------
    base_corridor = np.full((1, 1, 12, num_nodes), 10.0, dtype=np.float32)
    shock_corridor = base_corridor.copy()
    atraso_real_gps = 45.0
    shock_corridor[0, 0, -1, 10] = atraso_real_gps  # Bloqueio abrupto apenas no no 10

    x_base_t = torch.tensor((base_corridor - mean_v) / std_v, dtype=torch.float32)
    x_shock_t = torch.tensor((shock_corridor - mean_v) / std_v, dtype=torch.float32)

    with torch.no_grad():
        pred_base_min = model(x_base_t, l_norm)[0, 0, :].numpy() * std_v + mean_v
        pred_shock_min = model(x_shock_t, l_norm)[0, 0, :].numpy() * std_v + mean_v

    pred_n10 = float(pred_shock_min[10])
    spill_n9 = float(pred_shock_min[9] - pred_base_min[9])
    spill_n11 = float(pred_shock_min[11] - pred_base_min[11])
    trava = avaliar_trava_hibrida_defensiva(tempo_gps_min=atraso_real_gps, tempo_stgcn_min=pred_n10)

    print("\n[3. CASO DE FALHA REAL · SLIDE 3 DO SEM2]")
    print(f"  - Entrada Real: Bloqueio pontual no No 10 (Trevo de Ipojuca / PE-60) com GPS = {atraso_real_gps:.1f} min.")
    print(f"  - Saida da STGCN (como saiu): {pred_n10:.1f} min no No 10 (espalhou {spill_n9:+.1f} min no No 9 e {spill_n11:+.1f} min no No 11).")
    print(f"  - O que devia sair: {atraso_real_gps:.1f} min (alerta critico de interdicacao [?]).")
    print(f"  - Quem sofre: O trabalhador/estudante na parada que confia no {pred_n10:.1f} min, espera sem alternativa e perde o turno.")
    print(
        f"  - Trava Hibrida (|GPS - STGCN| > 15 min): "
        f"delta={trava['discrepancy_delta']:.1f} min | acionada={trava['trava_acionada']} | status={trava['status']} | exibido={trava['tempo_exibido_min']:.1f} min"
    )
    print("=" * 80)


if __name__ == "__main__":
    main()
