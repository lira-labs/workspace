# -*- coding: utf-8 -*-
"""
Pipeline de Treino Continuo Conectado ao Banco · GrafoParada
============================================================
1. Conecta ao `db_manager.py` (init_db, get_training_dataset, log_training_run)
   com fallback seguro caso o modulo ainda esteja indisponivel.
2. Carrega `gtfs_real_network.json` + `gtfs_schedules.json` + observacoes/rotinas reais do banco.
3. Valida cobertura integral das 393 linhas (trajetos IDA/VOLTA, paradas e horarios publicos).
4. Treina e avalia ST-GCN (`stgcn_official.py`) vs OLS vs Persistencia em split temporal estrito
   (sem vazamento temporal entre treino e teste).
5. Grava `code/grafoparada_web/data/model_training_status.json` e registra execucao em `training_runs`.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn as nn

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from stgcn_official import STGCN, compute_normalized_laplacian  # noqa: E402

try:
    from db_manager import (
        get_training_dataset,
        init_db,
        log_training_run,
        sync_cloud_observations,
    )

    DB_MANAGER_AVAILABLE = True
    DB_IMPORT_ERROR = None
except Exception as exc:  # pragma: no cover - fallback defensivo
    DB_MANAGER_AVAILABLE = False
    DB_IMPORT_ERROR = str(exc)

    def init_db(*args: Any, **kwargs: Any) -> None:
        return None

    def get_training_dataset(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            "observations": [],
            "routines": [],
            "total_observations": 0,
            "total_routines": 0,
            "lines_covered": [],
        }

    def log_training_run(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return {}

    def sync_cloud_observations(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            "synced": False,
            "reason": "no_api_base_or_offline",
            "observations_added": 0,
            "routines_added": 0,
        }


WEB_DATA_DIR = BASE_DIR.parent / "grafoparada_web" / "data"
NETWORK_JSON = WEB_DATA_DIR / "gtfs_real_network.json"
SCHEDULES_JSON = WEB_DATA_DIR / "gtfs_schedules.json"
STATUS_JSON = WEB_DATA_DIR / "model_training_status.json"

EXPECTED_LINES = 393
HISTORY_LEN = 12
HORIZON = 3
TRAVA_HIBRIDA_LIMIAR_MIN = 15.0


def approx_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return math.hypot(
        (lat1 - lat2) * 111.32,
        (lon1 - lon2) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2.0)),
    )


def band_for_minute(minute_of_day: int) -> str:
    m = minute_of_day % 1440
    if m < 300:
        return "madrugada"
    if m < 540:
        return "pico_manha"
    if m < 960:
        return "entre_picos"
    if m < 1200:
        return "pico_tarde"
    return "noite"


def validate_full_mesh(network: dict[str, Any], schedules: dict[str, Any]) -> dict[str, Any]:
    """Valida integridade e cobertura de 100% das 393 linhas (trajetos, paradas e horarios)."""
    net_lines = network.get("popular_lines", {})
    sched_lines = schedules.get("lines", {})

    if len(net_lines) != EXPECTED_LINES:
        raise RuntimeError(f"gtfs_real_network.json tem {len(net_lines)} linhas; esperado {EXPECTED_LINES}.")
    if len(sched_lines) != EXPECTED_LINES:
        raise RuntimeError(f"gtfs_schedules.json tem {len(sched_lines)} linhas; esperado {EXPECTED_LINES}.")
    if set(net_lines.keys()) != set(sched_lines.keys()):
        missing = sorted(set(net_lines.keys()) ^ set(sched_lines.keys()))
        raise RuntimeError(f"Divergencia de chaves entre rede e horarios: {missing[:10]}")

    ida_ok = 0
    volta_ok = 0
    dut_ok = 0
    sab_ok = 0
    dom_ok = 0
    stops_aligned = 0

    for code, nl in net_lines.items():
        sl = sched_lines[code]
        stops_ida = nl.get("stops", [])
        poly_ida = nl.get("polyline", [])
        if not stops_ida or not poly_ida:
            raise RuntimeError(f"Linha {code} sem paradas ou polyline IDA.")

        ida_sched = sl.get("ida", {})
        if "DUT" not in ida_sched or not ida_sched["DUT"].get("dep_mins"):
            raise RuntimeError(f"Linha {code} sem horarios DUT em IDA.")
        ida_ok += 1
        dut_ok += 1
        if "SAB" in ida_sched and ida_sched["SAB"].get("dep_mins"):
            sab_ok += 1
        if "DOM" in ida_sched and ida_sched["DOM"].get("dep_mins"):
            dom_ok += 1

        offsets_ida = ida_sched.get("stop_offsets_min", [])
        if len(offsets_ida) == len(stops_ida):
            stops_aligned += 1
        else:
            raise RuntimeError(
                f"Linha {code} com offsets IDA ({len(offsets_ida)}) != paradas ({len(stops_ida)})."
            )

        ret_stops = nl.get("return_stops", [])
        volta_sched = sl.get("volta", {})
        if ret_stops and volta_sched:
            if len(volta_sched.get("stop_offsets_min", [])) != len(ret_stops):
                raise RuntimeError(f"Linha {code} com offsets VOLTA desalinhados.")
            volta_ok += 1

    rmr_places = schedules.get("rmr_places", [])
    rmr_cities = [p for p in rmr_places if p.get("type") == "city"]
    if len(rmr_cities) != 14:
        raise RuntimeError(f"Esperadas 14 cidades oficiais da RMR em rmr_places; encontradas {len(rmr_cities)}.")

    ti_hubs = schedules.get("ti_hubs", [])
    ti_checkpoints_total = sum(
        len(sl.get("ida", {}).get("ti_checkpoints", [])) + len(sl.get("volta", {}).get("ti_checkpoints", []))
        for sl in sched_lines.values()
    )

    return {
        "lines_covered": len(net_lines),
        "schedules_indexed": len(sched_lines),
        "ida_with_schedules": ida_ok,
        "volta_with_schedules": volta_ok,
        "dut_lines": dut_ok,
        "sab_lines": sab_ok,
        "dom_lines": dom_ok,
        "stops_aligned_393": stops_aligned,
        "rmr_cities": len(rmr_cities),
        "rmr_places_total": len(rmr_places),
        "ti_hubs_indexed": len(ti_hubs),
        "ti_checkpoints_total": ti_checkpoints_total,
    }


def _normalize_hub_name(name: str) -> str:
    """Normaliza nome de hub/terminal para deduplicacao robusta (sem acentos, maiusculas)."""
    nfkd = unicodedata.normalize("NFKD", str(name or ""))
    ascii_str = "".join(ch for ch in nfkd if not unicodedata.combining(ch))
    return " ".join(ascii_str.upper().strip().split())


def build_metropolitan_hub_graph(
    network: dict[str, Any],
    max_nodes: int = 24,
    schedules: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], np.ndarray, torch.Tensor]:
    """Constroi grafo espacial dos principais hubs/terminais metropolitanos reais do GTFS."""
    candidates: list[dict[str, Any]] = []
    for h in network.get("hub_graph", []):
        lines = [str(c).strip() for c in h.get("lines", []) if str(c).strip()]
        if lines and h.get("lat") is not None and h.get("lon") is not None:
            candidates.append({
                "name": str(h.get("name") or "").strip(),
                "lat": float(h["lat"]),
                "lon": float(h["lon"]),
                "lines": sorted(set(lines)),
            })

    if schedules:
        for th in schedules.get("ti_hubs", []):
            codes = sorted({
                str(entry.get("code") or "").strip()
                for entry in th.get("lines", [])
                if isinstance(entry, dict) and str(entry.get("code") or "").strip()
            })
            if codes and th.get("lat") is not None and th.get("lon") is not None:
                candidates.append({
                    "name": str(th.get("name") or "").strip(),
                    "lat": float(th["lat"]),
                    "lon": float(th["lon"]),
                    "lines": codes,
                })

    # Dedup por nome normalizado e proximidade < 0.35 km, mantendo hub mais conectado
    dedup_hubs: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for h in sorted(candidates, key=lambda x: len(x.get("lines", [])), reverse=True):
        norm_name = _normalize_hub_name(h["name"])
        if norm_name and norm_name in seen_names:
            continue
        if any(approx_km(h["lat"], h["lon"], u["lat"], u["lon"]) < 0.35 for u in dedup_hubs):
            continue
        if norm_name:
            seen_names.add(norm_name)
        dedup_hubs.append(h)
        if len(dedup_hubs) >= max_nodes:
            break

    n = len(dedup_hubs)
    adj = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        lines_i = set(dedup_hubs[i]["lines"])
        for j in range(i + 1, n):
            lines_j = set(dedup_hubs[j]["lines"])
            shared = len(lines_i & lines_j)
            if shared > 0:
                dist = approx_km(
                    dedup_hubs[i]["lat"], dedup_hubs[i]["lon"],
                    dedup_hubs[j]["lat"], dedup_hubs[j]["lon"],
                )
                weight = float(shared) / (1.0 + 0.15 * dist)
                adj[i, j] = weight
                adj[j, i] = weight

    # Normaliza pesos fora da diagonal para [0, 1]
    max_w = float(np.max(adj))
    if max_w > 0:
        adj = adj / max_w

    l_matrix = compute_normalized_laplacian(adj)
    return dedup_hubs, adj, l_matrix


def _parse_hhmm_to_min(hhmm: str | None) -> int | None:
    if not hhmm or ":" not in str(hhmm):
        return None
    try:
        parts = str(hhmm).strip().split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except Exception:
        return None


def build_spatiotemporal_series(
    hubs: list[dict[str, Any]],
    adj: np.ndarray,
    schedules: dict[str, Any],
    observations: list[dict[str, Any]],
    routines: list[dict[str, Any]],
    total_steps: int = 432,
    step_min: int = 10,
) -> tuple[np.ndarray, int]:
    """
    Gera serie cronologica [total_steps, 6, num_nodes] cobrindo 72h+ (DUT -> SAB -> DOM):
      - Canal 0: tempo de espera na parada/hub (min) combinado de headways GTFS (IDA/VOLTA) + propagacao no grafo + observacoes reais do banco
      - Canal 1: pressao de demanda (partidas/10min GTFS IDA/VOLTA + rotinas/observacoes persistidas)
      - Canal 2: sin(2 * pi * minuto_do_dia / 1440)
      - Canal 3: cos(2 * pi * minuto_do_dia / 1440)
      - Canal 4: is_peak (1.0 em pico_manha/pico_tarde, 0.0 caso contrario)
      - Canal 5: is_weekend (1.0 em SAB/DOM, 0.0 em DUT)
    """
    rng = np.random.default_rng(2026)
    num_nodes = len(hubs)
    sched_lines = schedules.get("lines", {})

    # Mapeia linha -> indices de hubs servidos
    line_to_hubs: dict[str, list[int]] = {}
    for idx, hub in enumerate(hubs):
        for code in hub.get("lines", []):
            line_to_hubs.setdefault(code, []).append(idx)

    # Mapeia cada hub do grafo para seu TI correspondente em ti_hubs (e checkpoints GTFS)
    ti_hubs = schedules.get("ti_hubs", [])
    hub_ti_entries: dict[int, list[dict[str, Any]]] = {}
    for idx, hub in enumerate(hubs):
        h_name = str(hub.get("name") or "").strip().upper()
        matched = None
        for th in ti_hubs:
            th_name = str(th.get("name") or "").strip().upper()
            if th_name == h_name or approx_km(hub["lat"], hub["lon"], th["lat"], th["lon"]) <= 0.45:
                matched = th
                break
        if matched:
            hub_ti_entries[idx] = matched.get("lines", [])
        else:
            # Fallback via ti_checkpoints das linhas que servem este hub
            cps_fallback: list[dict[str, Any]] = []
            for code in hub.get("lines", []):
                for dkey in ("ida", "volta"):
                    for cp in sched_lines.get(code, {}).get(dkey, {}).get("ti_checkpoints", []):
                        cp_name = str(cp.get("stop_name") or "").strip().upper()
                        if cp_name and (cp_name in h_name or h_name in cp_name):
                            cps_fallback.append({
                                "code": code,
                                "direction": dkey,
                                "offset_min": cp.get("offset_min", 0.0),
                            })
            hub_ti_entries[idx] = cps_fallback

    # Pre-calcula headway medio por (hub, servico, faixa) e histograma de partidas/chegadas por slot de 10 min (144 slots)
    hub_band_wait: dict[tuple[int, str, str], float] = {}
    hub_slot_deps: dict[str, np.ndarray] = {
        svc: np.zeros((num_nodes, 144), dtype=np.float32) for svc in ("DUT", "SAB", "DOM")
    }

    for svc in ("DUT", "SAB", "DOM"):
        for idx, hub in enumerate(hubs):
            ti_lines = hub_ti_entries.get(idx, [])
            ti_passages_by_band: dict[str, list[int]] = {
                b: [] for b in ("madrugada", "pico_manha", "entre_picos", "pico_tarde", "noite")
            }
            for entry in ti_lines:
                code = entry["code"]
                dkey = entry.get("direction", "ida")
                off_m = float(entry.get("offset_min", 0.0))
                svc_data = sched_lines.get(code, {}).get(dkey, {}).get(svc)
                if not svc_data:
                    svc_data = sched_lines.get(code, {}).get(dkey, {}).get("DUT", {})
                for dm in svc_data.get("dep_mins", []):
                    pass_min = int(round(dm + off_m)) % 1440
                    slot = pass_min // step_min
                    hub_slot_deps[svc][idx, slot] += 0.65
                    ti_passages_by_band[band_for_minute(pass_min)].append(pass_min)

            for band_name in ("madrugada", "pico_manha", "entre_picos", "pico_tarde", "noite"):
                hws = []
                for code in hub.get("lines", []):
                    line_sched = sched_lines.get(code, {})
                    for dkey in ("ida", "volta"):
                        dir_sched = line_sched.get(dkey, {})
                        if not dir_sched:
                            continue
                        svc_data = dir_sched.get(svc) or dir_sched.get("DUT", {})
                        hw = svc_data.get("headways_min", {}).get(band_name)
                        if hw is not None and hw > 0:
                            hws.append(float(hw))
                base_hw = float(np.median(hws)) if hws else 35.0
                base_wait = min(45.0, max(5.0, 0.5 * base_hw))

                # Prior programado GTFS no TI: densidade de chegadas/saidas reais na faixa
                band_pass = sorted(ti_passages_by_band[band_name])
                if len(band_pass) >= 2:
                    gaps = [
                        band_pass[k + 1] - band_pass[k]
                        for k in range(len(band_pass) - 1)
                        if 0 < (band_pass[k + 1] - band_pass[k]) <= 120
                    ]
                    if gaps:
                        ti_prior_wait = min(45.0, max(3.5, 0.5 * float(np.median(gaps))))
                        base_wait = 0.65 * base_wait + 0.35 * ti_prior_wait
                hub_band_wait[(idx, svc, band_name)] = base_wait

            for code in hub.get("lines", []):
                line_sched = sched_lines.get(code, {})
                for dkey in ("ida", "volta"):
                    dir_sched = line_sched.get(dkey, {})
                    if not dir_sched:
                        continue
                    svc_data = dir_sched.get(svc) or dir_sched.get("DUT", {})
                    for dm in svc_data.get("dep_mins", []):
                        slot = (int(dm) % 1440) // step_min
                        hub_slot_deps[svc][idx, slot] += 0.65 if dkey == "volta" else 1.0

        hub_slot_deps[svc] = np.clip(hub_slot_deps[svc] * 0.40, 0.5, 45.0)

    # Matriz de propagacao espacial linha-normalizada
    row_sum = adj.sum(axis=1, keepdims=True)
    row_sum[row_sum == 0] = 1.0
    adj_norm = adj / row_sum

    series = np.zeros((total_steps, 6, num_nodes), dtype=np.float32)
    congestion_state = np.zeros(num_nodes, dtype=np.float32)

    # Pre-indexa observacoes reais e rotinas do banco por slot/hub
    obs_residuals: dict[tuple[int, int], list[float]] = {}
    obs_pressure: dict[tuple[int, int], float] = {}
    db_rows_used = 0

    for obs in observations:
        code = str(obs.get("route_code") or "").strip()
        wait_obs = obs.get("observed_wait_min")
        delay_obs = obs.get("delay_min")
        pred_wait = obs.get("predicted_wait_min")
        eff_wait: float | None = None
        try:
            if wait_obs is not None:
                eff_wait = float(wait_obs)
            elif delay_obs is not None:
                delay_val = float(delay_obs)
                if pred_wait is not None:
                    eff_wait = max(2.0, float(pred_wait) + delay_val)
                else:
                    eff_wait = max(2.0, delay_val)
        except (TypeError, ValueError):
            eff_wait = None
        if eff_wait is None:
            continue
        target_hubs = line_to_hubs.get(code) or [0]
        created_str = str(obs.get("created_at") or "")
        slot_mod = 48
        if "T" in created_str:
            try:
                hh_mm = created_str.split("T")[1][:5]
                m_day = _parse_hhmm_to_min(hh_mm)
                if m_day is not None:
                    slot_mod = (m_day % 1440) // step_min
            except Exception:
                pass
        try:
            occ = float(obs.get("occupancy_est") or 2)
        except (TypeError, ValueError):
            occ = 2.0
        for h_idx in target_hubs:
            obs_residuals.setdefault((slot_mod, h_idx), []).append(eff_wait)
            obs_pressure[(slot_mod, h_idx)] = obs_pressure.get((slot_mod, h_idx), 0.0) + occ * 1.5
        db_rows_used += 1

    for rtn in routines:
        pref = str(rtn.get("preferred_line") or "").strip()
        dep_m = _parse_hhmm_to_min(rtn.get("departure_time"))
        slot_mod = (dep_m % 1440) // step_min if dep_m is not None else 42
        target_hubs = line_to_hubs.get(pref, [])
        if not target_hubs and rtn.get("origin_lat") is not None and rtn.get("origin_lon") is not None:
            ola, olo = float(rtn["origin_lat"]), float(rtn["origin_lon"])
            nearest = min(range(num_nodes), key=lambda i: approx_km(ola, olo, hubs[i]["lat"], hubs[i]["lon"]))
            target_hubs = [nearest]
        for h_idx in target_hubs:
            obs_pressure[(slot_mod, h_idx)] = obs_pressure.get((slot_mod, h_idx), 0.0) + 3.0
        db_rows_used += 1

    services_cycle = ("DUT", "SAB", "DOM", "DUT")

    # Constroi serie cronologica de espera & pressao com dinamica de pico e propagacao no grafo
    for t in range(total_steps):
        day_idx = ((t * step_min) // 1440) % len(services_cycle)
        svc = services_cycle[day_idx]
        minute_of_day = (t * step_min + 240) % 1440  # inicia as 04:00
        slot_day = minute_of_day // step_min
        band = band_for_minute(minute_of_day)

        base_wait = np.array([hub_band_wait[(i, svc, band)] for i in range(num_nodes)], dtype=np.float32)
        demand = hub_slot_deps[svc][:, slot_day].copy()

        peak_factor = 1.0
        if band == "pico_manha":
            peak_factor = 1.32
        elif band == "pico_tarde":
            peak_factor = 1.38

        # Choque localizado em um hub que se propaga pelos vizinhos do grafo
        shock = np.zeros(num_nodes, dtype=np.float32)
        if t % 19 == 7:
            shock_node = (t // 19) % num_nodes
            shock[shock_node] = rng.uniform(10.0, 22.0)

        propagated = adj_norm @ congestion_state
        congestion_state = np.clip(
            0.48 * congestion_state + 0.42 * propagated + 0.22 * (demand * 0.25) + shock + rng.normal(0.0, 1.0, num_nodes),
            0.0,
            45.0,
        ).astype(np.float32)

        wait_t = base_wait * peak_factor + 0.65 * congestion_state + rng.normal(0.0, 0.7, num_nodes)

        for i in range(num_nodes):
            real_waits = obs_residuals.get((slot_day, i))
            if real_waits:
                wait_t[i] = 0.65 * float(np.mean(real_waits)) + 0.35 * wait_t[i]
            extra_p = obs_pressure.get((slot_day, i), 0.0)
            if extra_p > 0:
                demand[i] += extra_p

        series[t, 0, :] = np.clip(wait_t, 2.0, 90.0)
        series[t, 1, :] = np.clip(demand, 0.5, 60.0)
        angle = 2.0 * math.pi * (minute_of_day / 1440.0)
        series[t, 2, :] = math.sin(angle)
        series[t, 3, :] = math.cos(angle)
        series[t, 4, :] = 1.0 if band in ("pico_manha", "pico_tarde") else 0.0
        series[t, 5, :] = 1.0 if svc in ("SAB", "DOM") else 0.0

    return series, db_rows_used


def make_sliding_windows(
    series: np.ndarray, history_len: int = HISTORY_LEN, horizon: int = HORIZON
) -> tuple[np.ndarray, np.ndarray]:
    """Converte [T, C, N] em janelas X=[W, C, history_len, N] e Y=[W, horizon, N]."""
    total_t = series.shape[0]
    xs, ys = [], []
    for t in range(history_len, total_t - horizon + 1):
        # X: [C, history_len, N]
        xs.append(np.transpose(series[t - history_len : t], (1, 0, 2)))
        # Y: [horizon, N] (espera futura no canal 0)
        ys.append(series[t : t + horizon, 0, :])
    return np.asarray(xs, dtype=np.float32), np.asarray(ys, dtype=np.float32)


def train_and_evaluate_models(
    series: np.ndarray, l_matrix: torch.Tensor, adj: np.ndarray | None = None
) -> dict[str, Any]:
    """Executa split temporal estrito (70% treino / purge gap / 30% teste) e avalia ST-GCN vs OLS vs Persistencia."""
    torch.manual_seed(42)
    np.random.seed(42)

    x_all, y_all = make_sliding_windows(series, HISTORY_LEN, HORIZON)
    total_w = len(x_all)
    purge_gap = HISTORY_LEN + HORIZON
    split_idx = int(total_w * 0.70)
    test_start = min(total_w - 10, split_idx + purge_gap)

    x_train = x_all[:split_idx]
    y_train = y_all[:split_idx]
    x_test = x_all[test_start:]
    y_test = y_all[test_start:]

    if len(x_train) < 20 or len(x_test) < 10:
        raise RuntimeError(f"Janelas insuficientes para split temporal estrito: train={len(x_train)}, test={len(x_test)}")

    # 1. Persistencia (repete a ultima espera observada em t-1 para todo horizonte)
    last_wait_test = x_test[:, 0, -1, :]  # [W_test, N]
    pred_pers = np.repeat(last_wait_test[:, None, :], HORIZON, axis=1)
    persistence_mae = float(np.mean(np.abs(y_test - pred_pers)))

    # 2. OLS (regressao linear tabular por no sobre ultimos 4 lags dos 2 canais endogenos)
    num_nodes = x_train.shape[3]
    in_channels = x_train.shape[1]
    pred_ols = np.zeros_like(y_test)
    for node_i in range(num_nodes):
        feat_tr = np.column_stack([
            x_train[:, 0, -4:, node_i],
            x_train[:, 1, -4:, node_i],
            np.ones(len(x_train), dtype=np.float32),
        ])
        feat_te = np.column_stack([
            x_test[:, 0, -4:, node_i],
            x_test[:, 1, -4:, node_i],
            np.ones(len(x_test), dtype=np.float32),
        ])
        for h_i in range(HORIZON):
            coef, _, _, _ = np.linalg.lstsq(feat_tr, y_train[:, h_i, node_i], rcond=None)
            pred_ols[:, h_i, node_i] = feat_te @ coef
    ols_mae = float(np.mean(np.abs(y_test - pred_ols)))

    # 3. ST-GCN residual (normalizacao Z-score estritamente ajustada no conjunto de treino)
    mean_x = x_train.mean(axis=(0, 2, 3), keepdims=True)
    std_x = x_train.std(axis=(0, 2, 3), keepdims=True) + 1e-5
    last_wait_train = np.repeat(x_train[:, 0, -1:, :], HORIZON, axis=1)
    dy_train = y_train - last_wait_train
    mean_dy = float(dy_train.mean())
    std_dy = float(dy_train.std()) + 1e-5

    x_tr_t = torch.tensor((x_train - mean_x) / std_x, dtype=torch.float32)
    y_tr_t = torch.tensor((dy_train - mean_dy) / std_dy, dtype=torch.float32)
    x_te_t = torch.tensor((x_test - mean_x) / std_x, dtype=torch.float32)

    epochs = 72
    model = STGCN(num_nodes=num_nodes, in_channels=in_channels, out_horizon=HORIZON)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=5e-5)
    criterion = nn.L1Loss()

    train_gen = torch.Generator().manual_seed(42)
    train_ds = torch.utils.data.TensorDataset(x_tr_t, y_tr_t)
    train_loader = torch.utils.data.DataLoader(train_ds, batch_size=64, shuffle=True, generator=train_gen)

    best_train_loss = float("inf")
    best_state: dict[str, torch.Tensor] | None = None

    for _epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        n_batches = 0
        for x_batch, y_batch in train_loader:
            optimizer.zero_grad()
            out = model(x_batch, l_matrix)
            loss = criterion(out, y_batch)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 2.0)
            optimizer.step()
            epoch_loss += float(loss.item())
            n_batches += 1
        scheduler.step()
        avg_loss = epoch_loss / max(1, n_batches)
        if avg_loss < best_train_loss:
            best_train_loss = avg_loss
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

    if best_state is not None:
        model.load_state_dict(best_state)

    model.eval()
    with torch.no_grad():
        pred_dy_norm = model(x_te_t, l_matrix).numpy()
    pred_stgcn = np.repeat(last_wait_test[:, None, :], HORIZON, axis=1) + (pred_dy_norm * std_dy + mean_dy)
    stgcn_mae = float(np.mean(np.abs(y_test - pred_stgcn)))

    # Metricas estratificadas por horizonte (+10, +20, +30 min) e regime (pico vs vale)
    mae_h10 = float(np.mean(np.abs(y_test[:, 0, :] - pred_stgcn[:, 0, :])))
    mae_h20 = float(np.mean(np.abs(y_test[:, 1, :] - pred_stgcn[:, 1, :])))
    mae_h30 = float(np.mean(np.abs(y_test[:, 2, :] - pred_stgcn[:, 2, :])))
    peak_mask = x_test[:, 4, -1, 0] > 0.5
    mae_pico = float(np.mean(np.abs(y_test[peak_mask] - pred_stgcn[peak_mask]))) if np.any(peak_mask) else stgcn_mae
    mae_vale = float(np.mean(np.abs(y_test[~peak_mask] - pred_stgcn[~peak_mask]))) if np.any(~peak_mask) else stgcn_mae

    # Avaliacao controlada de choque severo (> 40 min) e auditoria da Trava Hibrida Defensiva
    # Trava Hibrida: aciona quando |y_true - y_pred_stgcn| > TRAVA_HIBRIDA_LIMIAR_MIN (15.0 min)
    trava_triggers_normal = int(
        np.sum(np.abs(y_test[:, -1, :] - pred_stgcn[:, -1, :]) > TRAVA_HIBRIDA_LIMIAR_MIN)
    )
    stress_rng = np.random.default_rng(1337)
    x_stress = x_test.copy()
    y_stress = y_test.copy()
    stress_indices = list(range(0, len(x_stress), 8))
    if adj is not None and adj.shape[0] == num_nodes:
        row_s = adj.sum(axis=1, keepdims=True)
        row_s[row_s == 0] = 1.0
        adj_n = adj / row_s
    else:
        adj_n = np.eye(num_nodes, dtype=np.float32)

    for idx in stress_indices:
        s_node = idx % num_nodes
        # Bloqueio subito realista (40-75 min) no horizonte futuro com precursor leve em t-1
        shock_mag = float(stress_rng.uniform(40.0, 75.0))
        precursor = float(stress_rng.uniform(2.0, 6.0))
        x_stress[idx, 0, -1, s_node] = float(np.clip(x_stress[idx, 0, -1, s_node] + precursor, 2.0, 90.0))

        shock_vec = np.zeros(num_nodes, dtype=np.float32)
        shock_vec[s_node] = shock_mag
        neighbor_spill = adj_n @ shock_vec
        for h_i, growth in enumerate((0.85, 0.95, 1.00)):
            y_stress[idx, h_i, :] = np.clip(
                y_stress[idx, h_i, :] + growth * (0.85 * shock_vec + 0.15 * neighbor_spill),
                2.0,
                90.0,
            )

    last_wait_stress = x_stress[:, 0, -1, :]
    x_stress_t = torch.tensor((x_stress - mean_x) / std_x, dtype=torch.float32)
    with torch.no_grad():
        pred_stress_dy_norm = model(x_stress_t, l_matrix).numpy()
    pred_stress = np.repeat(last_wait_stress[:, None, :], HORIZON, axis=1) + (pred_stress_dy_norm * std_dy + mean_dy)
    abs_err_stress = np.abs(y_stress[stress_indices, :, :] - pred_stress[stress_indices, :, :])
    mae_choque_severo = float(np.mean(abs_err_stress))
    trava_triggers_stress = int(
        np.sum(np.max(abs_err_stress, axis=1) > TRAVA_HIBRIDA_LIMIAR_MIN)
    )
    trava_triggers = trava_triggers_normal + trava_triggers_stress

    # Hash deterministico dos pesos treinados (sem gravar .pt pesado no Git)
    hasher = hashlib.sha256()
    for name in sorted(model.state_dict().keys()):
        tensor_bytes = model.state_dict()[name].detach().cpu().numpy().astype(np.float32).tobytes()
        hasher.update(name.encode("utf-8"))
        hasher.update(tensor_bytes)
    weights_hash = hasher.hexdigest()[:16]

    return {
        "dataset_rows": int(total_w),
        "train_windows": int(len(x_train)),
        "test_windows": int(len(x_test)),
        "purge_gap_windows": int(purge_gap),
        "stgcn_mae": round(stgcn_mae, 4),
        "ols_mae": round(ols_mae, 4),
        "persistence_mae": round(persistence_mae, 4),
        "mae_pico": round(mae_pico, 4),
        "mae_vale": round(mae_vale, 4),
        "mae_h10": round(mae_h10, 4),
        "mae_h20": round(mae_h20, 4),
        "mae_h30": round(mae_h30, 4),
        "mae_choque_severo": round(mae_choque_severo, 4),
        "trava_hibrida_triggers": trava_triggers,
        "weights_hash": weights_hash,
    }


def run_continuous_training() -> dict[str, Any]:
    t0 = time.time()
    print("[1/5] Inicializando conexao com db_manager e carregando dados reais do banco...")
    db_connected = False
    if DB_MANAGER_AVAILABLE:
        init_db()
        try:
            sync_report = sync_cloud_observations()
            if sync_report.get("synced"):
                print(
                    "  -> Sync nuvem concluido: "
                    f"+{sync_report.get('observations_added', 0)} observacoes, "
                    f"+{sync_report.get('routines_added', 0)} rotinas"
                )
        except Exception as exc:  # pragma: no cover - seguranca adicional
            print(f"  [AVISO] Falha nao-bloqueante no sync nuvem ({exc}); seguindo com SQLite local.")
        db_data = get_training_dataset()
        db_connected = True
    else:
        print(f"  [AVISO] db_manager indisponivel ({DB_IMPORT_ERROR}); operando com fallback seguro.")
        db_data = get_training_dataset()

    observations = db_data.get("observations", [])
    routines = db_data.get("routines", [])
    real_observations_count = int(db_data.get("total_observations", len(observations)))
    routines_count = int(db_data.get("total_routines", len(routines)))
    print(f"  -> Banco conectado={db_connected} | observacoes={real_observations_count} | rotinas={routines_count}")

    print("[2/5] Carregando gtfs_real_network.json e gtfs_schedules.json...")
    with open(NETWORK_JSON, encoding="utf-8") as f:
        network = json.load(f)
    with open(SCHEDULES_JSON, encoding="utf-8") as f:
        schedules = json.load(f)

    print("[3/5] Validando cobertura integral da malha metropolitana (393/393 linhas)...")
    mesh_report = validate_full_mesh(network, schedules)
    print(
        f"  -> Cobertura validada: {mesh_report['lines_covered']}/393 linhas | "
        f"IDA={mesh_report['ida_with_schedules']} | VOLTA={mesh_report['volta_with_schedules']} | "
        f"Cidades RMR={mesh_report['rmr_cities']}"
    )

    print("[4/5] Construindo grafo metropolitano e avaliando ST-GCN vs OLS vs Persistencia (split temporal estrito)...")
    hubs, adj, l_matrix = build_metropolitan_hub_graph(network, max_nodes=24, schedules=schedules)
    series, db_rows_used = build_spatiotemporal_series(
        hubs=hubs,
        adj=adj,
        schedules=schedules,
        observations=observations,
        routines=routines,
        total_steps=576,
        step_min=10,
    )
    metrics = train_and_evaluate_models(series, l_matrix, adj=adj)
    trained_at_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    ti_hubs_indexed = int(mesh_report.get("ti_hubs_indexed", 0))
    gtfs_prior_enabled = ti_hubs_indexed > 0

    status_payload = {
        "lines_covered": mesh_report["lines_covered"],
        "schedules_indexed": mesh_report["schedules_indexed"],
        "real_observations": real_observations_count,
        "routines_count": routines_count,
        "stgcn_mae": metrics["stgcn_mae"],
        "ols_mae": metrics["ols_mae"],
        "persistence_mae": metrics["persistence_mae"],
        "mae_pico": metrics["mae_pico"],
        "mae_vale": metrics["mae_vale"],
        "mae_h10": metrics["mae_h10"],
        "mae_h20": metrics["mae_h20"],
        "mae_h30": metrics["mae_h30"],
        "mae_choque_severo": metrics["mae_choque_severo"],
        "weights_hash": metrics["weights_hash"],
        "trained_at_utc": trained_at_utc,
        "dataset_rows": metrics["dataset_rows"],
        "train_windows": metrics["train_windows"],
        "test_windows": metrics["test_windows"],
        "temporal_split": "strict_70_30_purged",
        "graph_nodes": len(hubs),
        "rmr_places_indexed": mesh_report["rmr_places_total"],
        "ti_hubs_indexed": ti_hubs_indexed,
        "gtfs_schedule_prior_enabled": gtfs_prior_enabled,
        "trava_hibrida_triggers": metrics["trava_hibrida_triggers"],
        "db_connected": db_connected,
        "db_rows_integrated": db_rows_used,
        "validation_393_passed": True,
    }

    print(f"[5/5] Gravando {STATUS_JSON} e registrando execucao em training_runs...")
    with open(STATUS_JSON, "w", encoding="utf-8") as f:
        json.dump(status_payload, f, ensure_ascii=False, indent=2)

    if DB_MANAGER_AVAILABLE:
        run_record = log_training_run(
            {
                "dataset_rows": metrics["dataset_rows"],
                "real_observations": real_observations_count,
                "lines_covered": mesh_report["lines_covered"],
                "stgcn_mae": metrics["stgcn_mae"],
                "ols_mae": metrics["ols_mae"],
                "persistence_mae": metrics["persistence_mae"],
                "weights_hash": metrics["weights_hash"],
                "notes": (
                    f"strict_70_30_purged | hubs={len(hubs)} | ti_hubs={ti_hubs_indexed} | "
                    f"gtfs_prior={gtfs_prior_enabled} | routines={routines_count} | "
                    f"rmr_places={mesh_report['rmr_places_total']} | trava={metrics['trava_hibrida_triggers']}"
                ),
                "created_at": trained_at_utc,
            }
        )
        print(f"  -> training_runs ID={run_record.get('id')} registrado com sucesso.")

    print(f"\n[SUCESSO] Treino continuo concluido em {time.time() - t0:.2f}s:")
    print(f"  -> Cobertura: {status_payload['lines_covered']}/393 linhas | Horarios: {status_payload['schedules_indexed']}/393")
    print(f"  -> DB real: {real_observations_count} observacoes | {routines_count} rotinas")
    print(
        f"  -> MAE Teste (min): ST-GCN={metrics['stgcn_mae']:.4f} | "
        f"OLS={metrics['ols_mae']:.4f} | Persistencia={metrics['persistence_mae']:.4f}"
    )
    print(f"  -> Weights Hash: {metrics['weights_hash']} | Trava Hibrida: {metrics['trava_hibrida_triggers']} acionamentos")
    return status_payload


if __name__ == "__main__":
    run_continuous_training()
