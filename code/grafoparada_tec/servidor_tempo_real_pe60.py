"""
Servidor Backend Real-Time do Console GrafoParada SICOE/CTM v4.5 (`servidor_tempo_real_pe60.py`).
Executa:
  1. Treinamento e manutenção em RAM dos modelos PyTorch reais (`ResSensorNetV2`, `KinematicStopFSM_V3`, `STGCN` 20 nós PE-60).
  2. Índice geodésico (Haversine) em RAM das 7.238 paradas oficiais do Grande Recife (`stops.txt`) + 20 nós do corredor PE-60.
  3. Proxy ao vivo sem cache com o servidor `https://api.cittamobi.com.br/m3p/js/` (Agência a=202 Grande Recife),
     incluindo `stops/viewport` e `prediction/stop/{id}?a=202` ao redor da localização exata do usuário (`lat`, `lon`).
  4. Inferência PyTorch ao vivo a cada clique (`/api/live/pytorch-infer`, `/api/live/stgcn-corridor`, `/api/live/nearby-stops`).
"""
from __future__ import annotations

import csv
import json
import math
import os
import random
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import networkx as nx
import numpy as np
import torch
import torch.nn as nn

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from motor_evolucao_prototipo import (
    KinematicStopFSM_V3,
    SEED,
    carregar_dados_completos,
    treinar_modelos_sensores,
)
from stgcn_official import STGCN, compute_normalized_laplacian

CITTAMOBI_BASE = "https://api.cittamobi.com.br/m3p/js"
CITTAMOBI_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distância geodésica em metros sobre o elipsoide terrestre."""
    r = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2.0) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2.0) ** 2
    return 2.0 * r * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0 - a)))


class LiveGrafoParadaEngine:
    """Mantém os modelos PyTorch treinados e o catálogo GTFS de 7.238 paradas na RAM."""

    def __init__(self):
        t0 = time.perf_counter()
        print("[ENGINE] Carregando malha GTFS (20 nós PE-60) e 4.714 amostras físicas do dataset TMD...")
        self.paradas, self.raw_by_cls, self.eng_by_cls = carregar_dados_completos()

        # Carrega telemetria completa das 20 paradas PE-60 (com IDs Cittamobi, STGCN e nomes semânticos)
        tele_path = BASE_DIR / "data" / "telemetria_real_pe60.json"
        if tele_path.exists():
            with open(tele_path, "r", encoding="utf-8") as f:
                self.telemetria_pe60 = json.load(f)
        else:
            self.telemetria_pe60 = {"stops": []}
        self.pe60_by_stop_id = {str(s["stop_id"]): s for s in self.telemetria_pe60.get("stops", [])}

        # Carrega todas as 7.238 paradas oficiais da RMR do arquivo GTFS `stops.txt`
        self.rmr_gtfs_stops = []
        stops_txt = BASE_DIR / "data" / "gtfs_granderecife" / "stops.txt"
        if stops_txt.exists():
            with open(stops_txt, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        sid = row["stop_id"].strip()
                        sname = row["stop_name"].strip()
                        slat = float(row["stop_lat"])
                        slon = float(row["stop_lon"])
                        pe60_meta = self.pe60_by_stop_id.get(sid)
                        if pe60_meta:
                            sname = pe60_meta["name"]
                        self.rmr_gtfs_stops.append({
                            "stop_id": sid,
                            "stop_name": sname,
                            "lat": slat,
                            "lon": slon,
                            "is_pe60_corridor": pe60_meta is not None,
                            "pe60_seq": pe60_meta["seq"] if pe60_meta else None,
                            "pe60_cittamobi_id": pe60_meta["cittamobi_id"] if pe60_meta else None,
                            "pe60_stgcn_t30": pe60_meta["stgcn_horizon_min"][2] if pe60_meta else None,
                            "pe60_wait_gps": pe60_meta["wait_gps_min"] if pe60_meta else None,
                            "pe60_abn_10m": pe60_meta["abandonment_10m"] if pe60_meta else None,
                        })
                    except Exception:
                        continue
        print(f"[ENGINE] {len(self.rmr_gtfs_stops)} paradas oficiais CTM (Grande Recife) indexadas em RAM.")

        print("[ENGINE] Treinando modelos PyTorch (`ClassifierV1`, `ResSensorNetV2`) na CPU...")
        self.v1_pack, self.v2_pack, self.test_raw_by_cls, self.test_eng_by_cls, self.classes = (
            treinar_modelos_sensores(self.raw_by_cls, self.eng_by_cls)
        )
        self.mod_v2, self.m_v2, self.s_v2, self.acc_v2, self.acc_v3_sv = self.v2_pack
        self.fsm_v3 = KinematicStopFSM_V3(geofence_radius_m=35.0)

        print("[ENGINE] Construindo Grafo Laplaciano (20 nós PE-60) e treinando `STGCN` em PyTorch...")
        self._init_stgcn_20nodes()

        dt = time.perf_counter() - t0
        print(f"[ENGINE] Pronto em {dt:.2f}s! Soft-Vote Acc: {self.acc_v3_sv*100:.2f}% | STGCN 20-nós ativa em RAM.")

    def _init_stgcn_20nodes(self):
        num_nodes = len(self.paradas)
        G = nx.DiGraph()
        for i in range(num_nodes):
            G.add_node(i)
        for i in range(num_nodes - 1):
            G.add_edge(i, i + 1, weight=1.0)
            G.add_edge(i + 1, i, weight=0.35)
        G.add_edge(5, 10, weight=0.5)
        G.add_edge(10, 14, weight=0.5)
        self.l_matrix_20 = compute_normalized_laplacian(nx.to_numpy_array(G))
        l_np = self.l_matrix_20.numpy()

        rng = np.random.default_rng(301)
        n_samples = 70
        x_gps = np.zeros((n_samples, 12, num_nodes), dtype=np.float32)
        x_abn = np.zeros((n_samples, 12, num_nodes), dtype=np.float32)
        y_all = np.zeros((n_samples, num_nodes), dtype=np.float32)

        for s in range(n_samples):
            wait = rng.uniform(11.0, 18.0, size=(12, num_nodes))
            abn = rng.uniform(0.5, 3.0, size=(12, num_nodes))
            if s % 3 != 2:
                origem = int(rng.integers(5, 11))
                choque = rng.uniform(26.0, 38.0)
                for t in range(6, 12):
                    avanco = (t - 6) // 2
                    no_onda = min(12, origem + avanco)
                    wait[t, no_onda] += choque * ((t - 5) / 6.0)
                    abn[t, no_onda] += rng.uniform(14.0, 26.0) * ((t - 5) / 6.0)
            onda_2 = l_np @ (l_np @ wait[-1])
            onda_3 = l_np @ (l_np @ (l_np @ wait[-1]))
            onda_abn = l_np @ (l_np @ np.tanh(abn[-1] / 10.0)) * 24.0
            cascata = 0.38 * np.maximum(0.0, onda_2 - 15.0) ** 1.15
            y_all[s] = 0.35 * wait[-1] + 0.45 * onda_2 + 0.35 * onda_3 + onda_abn + cascata
            x_gps[s] = wait
            x_abn[s] = abn

        x_raw = np.stack([x_gps, x_abn], axis=1)
        self.stgcn_mean_x = x_raw.mean(axis=(0, 2, 3), keepdims=True)
        self.stgcn_std_x = x_raw.std(axis=(0, 2, 3), keepdims=True) + 1e-5
        self.stgcn_mean_y = float(y_all.mean())
        self.stgcn_std_y = float(y_all.std()) + 1e-5

        xt = torch.tensor((x_raw - self.stgcn_mean_x) / self.stgcn_std_x, dtype=torch.float32)
        yt = torch.tensor((y_all - self.stgcn_mean_y) / self.stgcn_std_y, dtype=torch.float32)

        torch.manual_seed(SEED)
        self.stgcn_20 = STGCN(num_nodes=num_nodes, in_channels=2, out_horizon=3)
        opt = torch.optim.Adam(self.stgcn_20.parameters(), lr=0.012, weight_decay=1e-4)
        loss_fn = nn.MSELoss()
        self.stgcn_20.train()
        for _ in range(95):
            opt.zero_grad()
            out = self.stgcn_20(xt, self.l_matrix_20)
            loss = loss_fn(out[:, 2, :], yt)
            loss.backward()
            opt.step()
        self.stgcn_20.eval()

    def scan_nearby_stops(self, user_lat: float, user_lon: float, top_k: int = 8) -> dict:
        """
        Varre as 7.238 paradas oficiais do GTFS CTM + consulta ao vivo o endpoint `stops/viewport`
        e `prediction/stop/{id}?a=202` do Cittamobi ao redor da coordenada exata `(user_lat, user_lon)`.
        """
        t0 = time.perf_counter()

        # 1. Busca Haversine nas 7.238 paradas oficiais do GTFS Grande Recife
        scored_gtfs = []
        for st in self.rmr_gtfs_stops:
            if abs(st["lat"] - user_lat) > 0.15 or abs(st["lon"] - user_lon) > 0.15:
                continue
            d_m = haversine_m(user_lat, user_lon, st["lat"], st["lon"])
            scored_gtfs.append((d_m, st))

        # Caso o usuário esteja fora da RMR, calcula sobre todas as paradas sem filtro de bbox
        if not scored_gtfs:
            for st in self.rmr_gtfs_stops:
                d_m = haversine_m(user_lat, user_lon, st["lat"], st["lon"])
                scored_gtfs.append((d_m, st))

        scored_gtfs.sort(key=lambda x: x[0])
        closest_gtfs = []
        for d_m, st in scored_gtfs[:top_k]:
            walk_sec = int(round(d_m / 1.28))  # caminhada a ~4,6 km/h (1,28 m/s)
            closest_gtfs.append({
                "stop_id": st["stop_id"],
                "stop_name": st["stop_name"],
                "lat": st["lat"],
                "lon": st["lon"],
                "distance_m": round(d_m, 1),
                "walk_time_s": walk_sec,
                "inside_geofence_35m": d_m <= 35.0,
                "inside_pocket_radar_150m": d_m <= 150.0,
                "is_pe60_corridor": st["is_pe60_corridor"],
                "pe60_seq": st["pe60_seq"],
                "pe60_cittamobi_id": st["pe60_cittamobi_id"],
                "pe60_stgcn_t30": st["pe60_stgcn_t30"],
                "pe60_wait_gps": st["pe60_wait_gps"],
                "pe60_abn_10m": st["pe60_abn_10m"],
            })

        gtfs_scan_ms = (time.perf_counter() - t0) * 1000.0

        # 2. Consulta AO VIVO o servidor Cittamobi `stops/viewport` numa caixa de ~1,2 km ao redor do usuário
        delta = 0.0085
        vp_endpoint = (
            f"stops/viewport?swlat={user_lat - delta:.6f}&swlng={user_lon - delta:.6f}"
            f"&nelat={user_lat + delta:.6f}&nelng={user_lon + delta:.6f}"
        )
        vp_res = proxy_cittamobi_live(vp_endpoint)
        citta_raw_stops = []
        if vp_res.get("live"):
            r_obj = vp_res.get("response")
            if isinstance(r_obj, list):
                citta_raw_stops = r_obj
            elif isinstance(r_obj, dict):
                citta_raw_stops = r_obj.get("stops", []) or []

        scored_citta = []
        for cs in citta_raw_stops:
            try:
                loc = cs.get("location") or {}
                clat = float(loc.get("lat") or cs.get("lat") or cs.get("latitude"))
                clon = float(loc.get("lng") or cs.get("lng") or cs.get("longitude"))
                cid = cs.get("id") or cs.get("stopId")
                cmnem = cs.get("mnemonic") or cs.get("name") or "Sem denominação"
                cserv = cs.get("services") or []
                d_m = haversine_m(user_lat, user_lon, clat, clon)
                scored_citta.append({
                    "cittamobi_id": cid,
                    "mnemonic": cmnem,
                    "lat": clat,
                    "lon": clon,
                    "distance_m": round(d_m, 1),
                    "active_services": len(cserv) if isinstance(cserv, list) else 0,
                })
            except Exception:
                continue

        scored_citta.sort(key=lambda x: x["distance_m"])
        closest_citta = scored_citta[:top_k]

        # Se a parada oficial CTM tiver apenas o código numérico no GTFS (ex: "180264"), enriquece com o endereço real do Cittamobi!
        for gst in closest_gtfs:
            if gst["stop_name"] == gst["stop_id"] and scored_citta:
                best_cs = min(
                    scored_citta,
                    key=lambda cs: haversine_m(gst["lat"], gst["lon"], cs["lat"], cs["lon"]),
                )
                d_cs = haversine_m(gst["lat"], gst["lon"], best_cs["lat"], best_cs["lon"])
                if d_cs <= 75.0:
                    short_addr = best_cs["mnemonic"].split(" - ")[0].split(", Recife")[0].split(", Cabo")[0]
                    gst["stop_name"] = f"Parada #{gst['stop_id']} ({short_addr})"

        # 3. Se houver uma parada Cittamobi próxima (ou mapeada da PE-60), consulta `prediction/stop/{id}?a=202` ao vivo
        target_citta_id = None
        if closest_citta:
            target_citta_id = closest_citta[0]["cittamobi_id"]
        elif closest_gtfs and closest_gtfs[0].get("pe60_cittamobi_id"):
            target_citta_id = closest_gtfs[0]["pe60_cittamobi_id"]

        live_prediction_stop = None
        if target_citta_id:
            pred_res = proxy_cittamobi_live(f"prediction/stop/{target_citta_id}?a=202")
            resp_obj = pred_res.get("response") if isinstance(pred_res.get("response"), dict) else {}
            sv_list = resp_obj.get("services", []) if isinstance(resp_obj, dict) else []
            live_prediction_stop = {
                "cittamobi_stop_id": target_citta_id,
                "http_status": pred_res.get("http_status", 502),
                "latency_ms": pred_res.get("latency_ms", 0.0),
                "payload_bytes": pred_res.get("payload_bytes", 0),
                "services_returned": len(sv_list) if isinstance(sv_list, list) else 0,
                "sample_services": [
                    {
                        "routeCode": s.get("routeCode"),
                        "serviceMnemonic": s.get("serviceMnemonic"),
                        "vehicles": len(s.get("vehicles", []) or []),
                    }
                    for s in (sv_list[:4] if isinstance(sv_list, list) else [])
                ],
            }

        # 4. Gera o diagnóstico de Geocerca (35m) e Alerta de Voz Modo Bolso (On-Device) para a parada mais próxima
        nearest = closest_gtfs[0] if closest_gtfs else None
        if nearest:
            d0 = nearest["distance_m"]
            sname = nearest["stop_name"]
            if d0 <= 35.0:
                geofence_state = "INSIDE_35M_GEOFENCE"
                if nearest["is_pe60_corridor"]:
                    voice_alert = (
                        f"GrafoParada Modo Bolso: Você está dentro da geocerca de 35 metros da parada {sname} "
                        f"({d0:.1f} metros). Tempo estimado pela STGCN: {nearest['pe60_stgcn_t30']} minutos."
                    )
                else:
                    voice_alert = (
                        f"GrafoParada Modo Bolso: Você está na parada oficial CTM {sname} (código {nearest['stop_id']}, "
                        f"a {d0:.1f} metros). Monitoramento inercial de embarque e descida ativado."
                    )
            elif d0 <= 180.0:
                geofence_state = "APPROACHING_POCKET_RADAR"
                voice_alert = (
                    f"GrafoParada Modo Bolso: Parada {sname} reconhecida a {d0:.0f} metros "
                    f"(aproximadamente {nearest['walk_time_s']} segundos de caminhada)."
                )
            else:
                geofence_state = "OUTSIDE_GEOFENCE"
                voice_alert = (
                    f"Radar Geodésico Ativo: Parada oficial mais próxima é {sname} (GTFS {nearest['stop_id']}) "
                    f"a {d0:.0f} metros da sua posição atual."
                )
        else:
            geofence_state = "NO_STOPS"
            voice_alert = "Nenhuma parada encontrada."

        return {
            "queried_at": time.strftime("%H:%M:%S", time.localtime()),
            "user_location": {"lat": round(user_lat, 6), "lon": round(user_lon, 6)},
            "gtfs_total_indexed": len(self.rmr_gtfs_stops),
            "gtfs_scan_cpu_ms": round(gtfs_scan_ms, 2),
            "geofence_status": geofence_state,
            "pocket_voice_prompt": voice_alert,
            "closest_gtfs_stops": closest_gtfs,
            "cittamobi_viewport_live": {
                "http_status": vp_res.get("http_status", 502),
                "latency_ms": vp_res.get("latency_ms", 0.0),
                "payload_bytes": vp_res.get("payload_bytes", 0),
                "total_stops_in_bbox": len(citta_raw_stops),
                "closest_cittamobi_stops": closest_citta,
            },
            "cittamobi_nearest_stop_prediction": live_prediction_stop,
        }

    def infer_live_trajectory(self, scenario_type: str) -> dict:
        """Sorteia janelas reais de teste do dataset TMD, roda o ResSensorNetV2 e a FSM v3.0 ao vivo na CPU."""
        t0 = time.perf_counter()

        def draw_tmd_step(target_cls: str, dist_m: float, elapsed_min: float, stage_label: str):
            pool = self.test_eng_by_cls[target_cls]
            idx = random.randrange(len(pool))
            e26 = pool[idx]
            t_in = torch.tensor(np.array([(e26 - self.m_v2) / self.s_v2], dtype=np.float32))
            with torch.no_grad():
                logits = self.mod_v2(t_in)
                probs = torch.softmax(logits, dim=1).numpy()[0]
            dom_cls = self.classes[int(np.argmax(probs))]
            return {
                "elapsed_min": elapsed_min,
                "distance_to_stop_m": dist_m,
                "stage": stage_label,
                "true_sensor_class": target_cls,
                "pred_sensor_class": dom_cls,
                "probs": probs,
                "acc_mean": round(float(e26[0]), 2),
                "acc_std": round(float(e26[3]), 3),
                "gyro_std": round(float(e26[7]), 3),
                "sound_db": round(float(e26[8]), 1),
            }

        if scenario_type == "ALIGHTING":
            steps = [
                draw_tmd_step("Bus", 660.0, 0.0, "Rodovia PE-60 (Aproximando no Ônibus)"),
                draw_tmd_step("Bus", 330.0, 0.55, "Reduzindo p/ Encostar no Ponto"),
                draw_tmd_step("Still", 6.0, 1.50, "Dentro da Geocerca 35m (Porta Aberta)"),
                draw_tmd_step("Walking", 9.0, 2.00, "Descendo o Degrau (Dwell 30s)"),
                draw_tmd_step("Walking", 65.0, 2.75, "Caminhando na Calçada Pós-Parada"),
                draw_tmd_step("Walking", 125.0, 3.50, "Afastando-se a Pé (v = 4,8 km/h)"),
                draw_tmd_step("Walking", 185.0, 4.25, "Fora da Geocerca (Destino Final)"),
            ]
            bus_at_stop, next_stop = True, False
        elif scenario_type == "ABANDONMENT":
            steps = [
                draw_tmd_step("Walking", 75.0, 0.0, "Chegada a Pé na Parada PE-60"),
                draw_tmd_step("Still", 4.0, 1.0, "Aguardando no Ponto (Início Espera)"),
                draw_tmd_step("Still", 3.5, 16.0, "Espera Prolongada (15 min s/ Ônibus)"),
                draw_tmd_step("Still", 5.0, 34.0, "Limite de Espera (33 min · Sem GPS CTM)"),
                draw_tmd_step("Car", 250.0, 34.5, "Subiu em Ligeirinho / Lotação (PE-60)"),
                draw_tmd_step("Car", 620.0, 35.0, "Alta Velocidade s/ Parar no Ponto Seguinte"),
                draw_tmd_step("Car", 990.0, 35.5, "Evasão Confirmada na Via Expressa"),
            ]
            bus_at_stop, next_stop = False, False
        elif scenario_type == "BOARDING_SERVED":
            steps = [
                draw_tmd_step("Walking", 70.0, 0.0, "Chegada a Pé na Parada PE-60"),
                draw_tmd_step("Still", 4.0, 1.0, "Aguardando na Geocerca (35m)"),
                draw_tmd_step("Still", 5.0, 14.5, "Ônibus Oficial Linha 178 Encostou (GPS OK)"),
                draw_tmd_step("Bus", 200.0, 15.1, "Partida no Ônibus Oficial CTM"),
                draw_tmd_step("Bus", 440.0, 15.7, "Deslocamento Regular na Faixa"),
                draw_tmd_step("Bus", 680.0, 16.3, "Parou na Parada Seguinte do GTFS"),
            ]
            bus_at_stop, next_stop = True, True
        else:  # TRANSIT_BYPASS
            steps = [
                draw_tmd_step("Car", 480.0, 0.00, "Trafegando na Rodovia PE-60 (Antes)"),
                draw_tmd_step("Car", 14.0, 0.25, "Cruzou Raio de 35m sem Parar (Dwell 15s)"),
                draw_tmd_step("Car", 490.0, 0.55, "Trafegando na Rodovia PE-60 (Depois)"),
            ]
            bus_at_stop, next_stop = False, False

        verdict = self.fsm_v3.processar(
            steps, official_bus_at_stop=bus_at_stop, stopped_at_next_gtfs_stop=next_stop
        )
        cpu_us = (time.perf_counter() - t0) * 1e6

        post_steps = [s for s in steps if s["distance_to_stop_m"] > 35.0 and s["elapsed_min"] > steps[0]["elapsed_min"]]
        if not post_steps:
            post_steps = steps[-2:]
        pooled_probs = np.mean([s["probs"] for s in post_steps], axis=0)

        formatted_frames = []
        for i, s in enumerate(steps):
            if i == 0:
                v_kmh = 36.0 if s["true_sensor_class"] == "Bus" else (64.0 if s["true_sensor_class"] == "Car" else 4.5)
            else:
                dt_h = max(1e-4, (s["elapsed_min"] - steps[i - 1]["elapsed_min"]) / 60.0)
                dd_km = abs(s["distance_to_stop_m"] - steps[i - 1]["distance_to_stop_m"]) / 1000.0
                v_kmh = dd_km / dt_h
            conf_pct = float(np.max(s["probs"]) * 100.0)
            formatted_frames.append({
                "t": f"{s['elapsed_min']:.2f}m",
                "stage": s["stage"],
                "dist": f"{s['distance_to_stop_m']:.0f} m",
                "v": f"{v_kmh:.1f} km/h",
                "imu": f"{s['acc_std']:.2f} m/s² | {s['gyro_std']:.2f} rad/s",
                "db": f"{s['sound_db']:.1f} dB",
                "cls": f"{s['pred_sensor_class']} ({conf_pct:.0f}%)",
                "acc_mean": s["acc_mean"],
                "acc_std": s["acc_std"],
                "gyro_std": s["gyro_std"],
                "sound_db": s["sound_db"],
            })

        return {
            "timestamp": time.strftime("%H:%M:%S", time.localtime()),
            "scenario_requested": scenario_type,
            "fsm_verdict": verdict,
            "cpu_inference_us": round(cpu_us, 2),
            "soft_voting_probs": {
                "Still": round(float(pooled_probs[0] * 100.0), 1),
                "Walking": round(float(pooled_probs[1] * 100.0), 1),
                "Bus": round(float(pooled_probs[2] * 100.0), 1),
                "Car": round(float(pooled_probs[3] * 100.0), 1),
            },
            "frames": formatted_frames,
            "network_bytes_sent": 36 if verdict == "ABANDONMENT" else 0,
        }

    def infer_live_stgcn_corridor(self, shock_stop_seq: int = 11, shock_wait_min: float = 38.0, shock_abn: int = 14) -> dict:
        """Executa forward pass real da STGCN nas 20 paradas da PE-60 com os parâmetros fornecidos ao vivo."""
        t0 = time.perf_counter()
        num_nodes = len(self.paradas)
        wait = np.linspace(14.0, 18.0, num_nodes, dtype=np.float32)
        abn = np.zeros(num_nodes, dtype=np.float32)

        idx_target = max(0, min(num_nodes - 1, shock_stop_seq - 1))
        for offset in range(-2, 3):
            k = max(0, min(num_nodes - 1, idx_target + offset))
            decay = max(0.2, 1.0 - 0.25 * abs(offset))
            wait[k] = max(wait[k], shock_wait_min * decay)
            abn[k] = round(shock_abn * decay)

        x_gps = np.tile(wait, (1, 12, 1))
        x_abn = np.tile(abn, (1, 12, 1))
        x_raw = np.stack([x_gps, x_abn], axis=1)
        xt = torch.tensor((x_raw - self.stgcn_mean_x) / self.stgcn_std_x, dtype=torch.float32)

        with torch.no_grad():
            out_norm = self.stgcn_20(xt, self.l_matrix_20)[0].numpy()
            out_min = out_norm * self.stgcn_std_y + self.stgcn_mean_y

        cpu_ms = (time.perf_counter() - t0) * 1000.0
        node_horizons = [
            round(float(out_min[0, idx_target]), 1),
            round(float(out_min[1, idx_target]), 1),
            round(float(out_min[2, idx_target]), 1),
        ]
        return {
            "timestamp": time.strftime("%H:%M:%S", time.localtime()),
            "stop_seq": shock_stop_seq,
            "cpu_stgcn_ms": round(cpu_ms, 3),
            "predicted_horizons_min": node_horizons,
            "all_nodes_t30_min": [round(float(v), 1) for v in out_min[2, :]],
        }


ENGINE = LiveGrafoParadaEngine()


def proxy_cittamobi_live(endpoint: str) -> dict:
    """Consulta o servidor real `https://api.cittamobi.com.br/m3p/js/` no exato instante da chamada."""
    url = f"{CITTAMOBI_BASE}/{endpoint.lstrip('/')}"
    t0 = time.perf_counter()
    try:
        req = urllib.request.Request(url, headers=CITTAMOBI_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()
            latency_ms = (time.perf_counter() - t0) * 1000.0
            parsed = json.loads(raw.decode("utf-8-sig", errors="ignore"))
            return {
                "live": True,
                "queried_at": time.strftime("%H:%M:%S", time.localtime()),
                "target_url": url,
                "http_status": resp.status,
                "latency_ms": round(latency_ms, 2),
                "payload_bytes": len(raw),
                "response": parsed,
            }
    except Exception as e:
        latency_ms = (time.perf_counter() - t0) * 1000.0
        return {
            "live": False,
            "queried_at": time.strftime("%H:%M:%S", time.localtime()),
            "target_url": url,
            "http_status": 502,
            "latency_ms": round(latency_ms, 2),
            "error": str(e),
        }


class GrafoParadaLiveHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, fmt, *args):
        sys.stdout.write(f"[HTTP] {self.address_string()} - {fmt % args}\n")

    def _send_json(self, payload: dict, status: int = 200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        # 1. Endpoint Live Nearby Stops Radar (`/api/live/nearby-stops?lat=...&lon=...`)
        if parsed.path == "/api/live/nearby-stops":
            lat = float(qs.get("lat", ["-8.304950"])[0])
            lon = float(qs.get("lon", ["-35.021420"])[0])
            top_k = int(qs.get("k", ["6"])[0])
            res = ENGINE.scan_nearby_stops(lat, lon, top_k=top_k)
            self._send_json(res)
            return

        # 2. Endpoint Live Cittamobi Stop Prediction (`prediction/stop/{id}?a=202`)
        if parsed.path == "/api/live/cittamobi-stop":
            stop_id = qs.get("stop_id", ["2966773"])[0]
            service_id = qs.get("service_id", ["9655998"])[0]
            stop_res = proxy_cittamobi_live(f"prediction/stop/{stop_id}?a=202")
            veh_res = proxy_cittamobi_live(f"vehicles/service/{service_id}")
            self._send_json({
                "stop_query": stop_res,
                "service_vehicles_query": veh_res,
            })
            return

        # 3. Endpoint Live Cittamobi Fleet Audit across PE-60 Lines
        if parsed.path == "/api/live/cittamobi-fleet":
            lines = [
                ("0178 Ida", 9655998),
                ("0178 Volta", 9655999),
                ("178 SJT Ida", 13185570),
                ("0198 Ipojuca", 9656040),
                ("198 SJT", 13185572),
                ("0197 Cabo/Ipojuca", 9656042),
                ("119 Garapu", 6663),
            ]
            results = []
            for label, sid in lines:
                r = proxy_cittamobi_live(f"vehicles/service/{sid}")
                vehs = r.get("response", [])
                results.append({
                    "label": label,
                    "serviceId": sid,
                    "http_status": r["http_status"],
                    "latency_ms": r["latency_ms"],
                    "payload_bytes": r.get("payload_bytes", 0),
                    "active_vehicles": len(vehs) if isinstance(vehs, list) else 0,
                    "raw_response": vehs,
                })
            self._send_json({
                "queried_at": time.strftime("%H:%M:%S", time.localtime()),
                "results": results,
            })
            return

        # 4. Endpoint Live PyTorch ResSensorNetV2 + KinematicStopFSM_V3 Inference
        if parsed.path == "/api/live/pytorch-infer":
            scenario = qs.get("scenario", ["ALIGHTING"])[0]
            res = ENGINE.infer_live_trajectory(scenario)
            self._send_json(res)
            return

        # 5. Endpoint Live PyTorch STGCN 20-Node Corridor Inference
        if parsed.path == "/api/live/stgcn-corridor":
            seq = int(qs.get("seq", ["11"])[0])
            wait_m = float(qs.get("wait", ["38.0"])[0])
            abn_c = int(qs.get("abn", ["14"])[0])
            res = ENGINE.infer_live_stgcn_corridor(seq, wait_m, abn_c)
            self._send_json(res)
            return

        super().do_GET()


def main():
    port = int(os.environ.get("PORT", "8765"))
    server = ThreadingHTTPServer(("0.0.0.0", port), GrafoParadaLiveHandler)
    print(f"\n==========================================================================")
    print(f" [ONLINE] Console GrafoParada SICOE v4.5 em Tempo Real:")
    print(f" -> URL: http://localhost:{port}/prototipo_grafoparada.html")
    print(f"==========================================================================\n")
    server.serve_forever()


if __name__ == "__main__":
    main()
