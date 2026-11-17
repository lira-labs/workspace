# -*- coding: utf-8 -*-
"""
Protocolo Experimental Oficial · sem3 (GrafoParada)
===================================================
Experimento técnico pareado (sem participantes humanos) sobre corredor de 20 paradas
da PE-60 (topologia real), comparando 4 condições sob os mesmos cenários e seeds:
  - C1: Persistência (jeito de hoje)
  - C2: Regressão Tabular de Corredor (lags achatados, sem grafo)
  - C3: ST-GCN pura (20 nós, sem trava híbrida)
  - C4: ST-GCN + Trava Híbrida Defensiva [?] (|atraso_gps_min - stgcn| > 15.0 min)

Separação estrita de seeds:
  - Treino / ajuste: seeds 100..159 (nunca entram no conjunto de teste)
  - Teste oficial (25/11): 180 cenários (seeds 2000..2179):
      * 60 choques graves (> 40 min)
      * 60 intermediários (15 a 40 min)
      * 60 normais (<= 15 min)
  - Modo `--smoke` (Passo 4 antes de 18/11): roda 6 cenários (2 por grupo) para
    validar execução ponta a ponta, formato do CSV e métricas sem rodar o conjunto oficial.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from stgcn_official import STGCN, compute_normalized_laplacian  # noqa: E402

NUM_NODES = 20
HISTORY_LEN = 12
SHOCK_THRESHOLD_MIN = 40.0
HYBRID_LOCK_THRESHOLD_MIN = 15.0
OUT_DIR = BASE_DIR / "data" / "sem3"


def build_corridor_laplacian(n_nodes: int = NUM_NODES) -> np.ndarray:
    adj = np.zeros((n_nodes, n_nodes), dtype=np.float32)
    for i in range(n_nodes - 1):
        adj[i, i + 1] = 1.0
        adj[i + 1, i] = 1.0
    return compute_normalized_laplacian(adj)


def simulate_corridor_scenario(seed: int, group: str) -> dict:
    """Gera cenário determinístico de 20 paradas com gabarito independente."""
    rng = np.random.default_rng(seed)
    base_delay = rng.uniform(5.0, 11.0, size=(HISTORY_LEN, NUM_NODES)).astype(np.float32)
    noise = rng.normal(0.0, 0.9, size=(HISTORY_LEN, NUM_NODES)).astype(np.float32)
    x_seq = np.clip(base_delay + noise, 1.0, 60.0)

    # Propaga onda de tráfego leve ao longo do corredor
    for t in range(1, HISTORY_LEN):
        x_seq[t, 1:] = np.clip(0.65 * x_seq[t, 1:] + 0.35 * x_seq[t - 1, :-1], 1.0, 60.0)

    shock_node = int(rng.integers(2, NUM_NODES - 2))
    if group == "grave":
        true_delay = float(rng.uniform(41.0, 56.0))
        gps_obs = float(np.clip(true_delay + rng.normal(0.0, 1.5), 38.0, 62.0))
        # Choque súbito aparece na janela atual do GPS cinemático na parada
        x_seq[-1, shock_node] = max(x_seq[-1, shock_node], true_delay * 0.45)
    elif group == "intermediario":
        true_delay = float(rng.uniform(16.0, 38.0))
        gps_obs = float(np.clip(true_delay + rng.normal(0.0, 1.5), 14.0, 40.0))
        x_seq[-1, shock_node] = max(x_seq[-1, shock_node], true_delay * 0.70)
    else:
        true_delay = float(rng.uniform(4.0, 14.5))
        gps_obs = float(np.clip(true_delay + rng.normal(0.0, 1.0), 2.0, 15.0))

    # Gabarito único independente da previsão dos modelos
    is_grave = true_delay > SHOCK_THRESHOLD_MIN
    return {
        "seed": seed,
        "group": group,
        "shock_node": shock_node,
        "x_seq": x_seq,
        "gps_obs_min": round(gps_obs, 2),
        "true_delay_min": round(true_delay, 2),
        "is_grave": is_grave,
    }


def fit_frozen_models(l_mat: np.ndarray) -> tuple[np.ndarray, STGCN]:
    """Ajusta C2 (Tabular) e C3 (ST-GCN) apenas nas seeds de treino (100..159)."""
    torch.manual_seed(42)
    np.random.seed(42)

    train_scenarios = []
    for i in range(60):
        grp = ("normal", "intermediario", "grave")[i % 3]
        train_scenarios.append(simulate_corridor_scenario(100 + i, grp))

    # Matriz tabular achatada: lags do nó + vizinhos imediato
    X_tab = []
    y_tab = []
    X_graph = []
    y_graph = []
    for sc in train_scenarios:
        seq = sc["x_seq"]
        sn = sc["shock_node"]
        feat = np.concatenate([seq[:, sn], seq[:, max(0, sn - 1)], [1.0]])
        X_tab.append(feat)
        y_tab.append(sc["true_delay_min"])

        # Tensor (T, N) -> será empilhado como (B, 1, T=12, N=20)
        X_graph.append(seq)
        target_vec = seq[-1, :].copy()
        target_vec[sn] = sc["true_delay_min"]
        y_graph.append(target_vec)

    X_tab_np = np.asarray(X_tab, dtype=np.float64)
    y_tab_np = np.asarray(y_tab, dtype=np.float64)
    w_tab, *_ = np.linalg.lstsq(X_tab_np, y_tab_np, rcond=None)

    model = STGCN(num_nodes=NUM_NODES, in_channels=1, out_horizon=1)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
    loss_fn = nn.MSELoss()
    l_tensor = torch.tensor(l_mat, dtype=torch.float32)

    X_t = torch.tensor(np.asarray(X_graph), dtype=torch.float32).unsqueeze(1)  # (B, 1, 12, 20)
    Y_t = torch.tensor(np.asarray(y_graph), dtype=torch.float32)  # (B, 20)

    model.train()
    for _ in range(35):
        optimizer.zero_grad()
        out = model(X_t, l_tensor).squeeze(1)  # (B, 20)
        loss = loss_fn(out, Y_t)
        loss.backward()
        optimizer.step()
    model.eval()
    return w_tab, model


def clopper_pearson_95(k: int, n: int) -> tuple[float, float]:
    """Intervalo binomial exato 95% via busca binária simples (sem scipy)."""
    if n == 0:
        return (0.0, 1.0)

    def binom_cdf_upper(p: float, k_obs: int) -> float:
        total = 0.0
        for i in range(0, k_obs + 1):
            total += math.comb(n, i) * (p ** i) * ((1.0 - p) ** (n - i))
        return total

    def binom_cdf_lower(p: float, k_obs: int) -> float:
        total = 0.0
        for i in range(k_obs, n + 1):
            total += math.comb(n, i) * (p ** i) * ((1.0 - p) ** (n - i))
        return total

    alpha = 0.025
    lo = 0.0
    if k > 0:
        a, b = 0.0, 1.0
        for _ in range(40):
            m = 0.5 * (a + b)
            if binom_cdf_lower(m, k) < alpha:
                a = m
            else:
                b = m
        lo = 0.5 * (a + b)

    hi = 1.0
    if k < n:
        a, b = 0.0, 1.0
        for _ in range(40):
            m = 0.5 * (a + b)
            if binom_cdf_upper(m, k) < alpha:
                b = m
            else:
                a = m
        hi = 0.5 * (a + b)
    return (round(lo * 100.0, 2), round(hi * 100.0, 2))


def run_protocol(mode: str) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    l_mat = build_corridor_laplacian()
    w_tab, stgcn = fit_frozen_models(l_mat)
    l_tensor = torch.tensor(l_mat, dtype=torch.float32)

    if mode == "smoke":
        plan = [("grave", 2000), ("grave", 2001), ("intermediario", 2060), ("intermediario", 2061), ("normal", 2120), ("normal", 2121)]
    else:
        plan = (
            [("grave", 2000 + i) for i in range(60)]
            + [("intermediario", 2060 + i) for i in range(60)]
            + [("normal", 2120 + i) for i in range(60)]
        )

    rows = []
    for idx, (grp, seed) in enumerate(plan, 1):
        sc = simulate_corridor_scenario(seed, grp)
        seq = sc["x_seq"]
        sn = sc["shock_node"]
        gps = sc["gps_obs_min"]
        y_true = sc["true_delay_min"]
        is_grave = sc["is_grave"]

        # C1: Persistência (último valor observado na parada)
        pred_c1 = float(seq[-1, sn])
        alert_c1 = pred_c1 > SHOCK_THRESHOLD_MIN

        # C2: Regressão tabular de corredor
        feat = np.concatenate([seq[:, sn], seq[:, max(0, sn - 1)], [1.0]])
        pred_c2 = float(np.clip(feat @ w_tab, 1.0, 65.0))
        alert_c2 = pred_c2 > SHOCK_THRESHOLD_MIN

        # C3: ST-GCN pura
        with torch.no_grad():
            x_t = torch.tensor(seq, dtype=torch.float32).unsqueeze(0).unsqueeze(0)
            pred_vec = stgcn(x_t, l_tensor).squeeze().numpy()
        pred_c3 = float(np.clip(pred_vec[sn], 1.0, 65.0))
        alert_c3 = pred_c3 > SHOCK_THRESHOLD_MIN

        # C4: ST-GCN + Trava Híbrida Defensiva [?]
        diff_gps_stgcn = abs(gps - pred_c3)
        trava_triggered = diff_gps_stgcn > HYBRID_LOCK_THRESHOLD_MIN
        pred_c4 = gps if trava_triggered else pred_c3
        alert_c4 = alert_c3 or (trava_triggered and gps > SHOCK_THRESHOLD_MIN)

        rows.append(
            {
                "scenario_id": f"SCN-{idx:03d}",
                "seed": seed,
                "group": grp,
                "shock_node": sn,
                "true_delay_min": y_true,
                "gps_obs_min": gps,
                "is_grave": is_grave,
                "pred_c1_persist": round(pred_c1, 2),
                "alert_c1": alert_c1,
                "pred_c2_tabular": round(pred_c2, 2),
                "alert_c2": alert_c2,
                "pred_c3_stgcn": round(pred_c3, 2),
                "alert_c3": alert_c3,
                "diff_gps_stgcn": round(diff_gps_stgcn, 2),
                "trava_triggered": trava_triggered,
                "pred_c4_hybrid": round(pred_c4, 2),
                "alert_c4": alert_c4,
            }
        )

    suffix = "_smoke" if mode == "smoke" else "_official"
    csv_path = OUT_DIR / f"results_raw{suffix}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    graves = [r for r in rows if r["is_grave"]]
    non_graves = [r for r in rows if not r["is_grave"]]
    summary = {"mode": mode, "total_scenarios": len(rows), "graves": len(graves), "non_graves": len(non_graves), "conditions": {}}
    for key, pred_col, alert_col in [
        ("C1_Persistencia", "pred_c1_persist", "alert_c1"),
        ("C2_Tabular", "pred_c2_tabular", "alert_c2"),
        ("C3_STGCN_Pura", "pred_c3_stgcn", "alert_c3"),
        ("C4_STGCN_Trava_Hibrida", "pred_c4_hybrid", "alert_c4"),
    ]:
        fn = sum(1 for r in graves if not r[alert_col])
        fp = sum(1 for r in non_graves if r[alert_col])
        mae = sum(abs(r[pred_col] - r["true_delay_min"]) for r in rows) / len(rows)
        tcgns = (fn / len(graves) * 100.0) if graves else 0.0
        fpr = (fp / len(non_graves) * 100.0) if non_graves else 0.0
        summary["conditions"][key] = {
            "fn": fn,
            "tcgns_pct": round(tcgns, 2),
            "tcgns_ic95": list(clopper_pearson_95(fn, len(graves))),
            "fp": fp,
            "fpr_pct": round(fpr, 2),
            "fpr_ic95": list(clopper_pearson_95(fp, len(non_graves))),
            "mae_min": round(mae, 2),
        }

    report_path = OUT_DIR / f"evaluation_report{suffix}.json"
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Protocolo experimental sem3 (GrafoParada).")
    parser.add_argument("--mode", choices=["smoke", "full"], default="smoke")
    args = parser.parse_args()
    run_protocol(args.mode)
