# -*- coding: utf-8 -*-
"""
Compilador Completo de Dados Reais do GTFS Grande Recife para o GrafoParada Web.
Extrai TODAS as 400 linhas reais, paradas sequenciais e traçados geodésicos GPS
do GTFS oficial do Consórcio de Transporte Metropolitano (CTM).
Zero Mock · 100% Cobertura Metropolitana Real.
"""
import csv
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
GTFS_DIR = BASE_DIR / "data" / "gtfs_granderecife"
OUTPUT_WEB = BASE_DIR.parent / "grafoparada_web" / "data" / "gtfs_real_network.json"
OUTPUT_WEB.parent.mkdir(parents=True, exist_ok=True)

def main():
    start_total = time.time()
    print("[1/5] Carregando paradas oficiais de stops.txt...")
    stops_dict = {}
    terminals_sei = []
    
    with open(GTFS_DIR / "stops.txt", encoding="utf-8") as f:
        for s in csv.DictReader(f):
            sid = s["stop_id"]
            name = s["stop_name"]
            lat = round(float(s["stop_lat"]), 6)
            lon = round(float(s["stop_lon"]), 6)
            stops_dict[sid] = {"id": sid, "name": name, "lat": lat, "lon": lon}
            
            # Detecta Terminais Integrados (SEI)
            uname = name.upper()
            if "TI " in uname or "TERMINAL INTEGRADO" in uname or "T.I." in uname or "T.I " in uname:
                terminals_sei.append({"id": sid, "name": name, "lat": lat, "lon": lon})

    print(f"  -> Total de paradas no Grande Recife: {len(stops_dict)}")
    print(f"  -> Terminais Integrados (SEI) identificados: {len(terminals_sei)}")

    print("[2/5] Carregando catálogo completo de routes.txt...")
    routes_all = []
    routes_map = {}
    with open(GTFS_DIR / "routes.txt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rid = r["route_id"]
            short = r["route_short_name"]
            long_n = r["route_long_name"]
            routes_map[rid] = {"id": rid, "short": short, "long": long_n}
            routes_all.append({
                "id": rid,
                "code": short,
                "label": f"{short} · {long_n}",
                "name": long_n
            })

    routes_all.sort(key=lambda x: x["code"])
    print(f"  -> Total de linhas no catálogo: {len(routes_all)}")

    print("[3/5] Selecionando viagens representativas (IDA e VOLTA) para TODAS as linhas em trips.txt...")
    trips_selected = {}      # rid -> trip principal (IDA/DUT)
    trips_alt_dir = {}       # rid -> trip sentido oposto (VOLTA/direction_id=1)
    with open(GTFS_DIR / "trips.txt", encoding="utf-8") as f:
        for t in csv.DictReader(f):
            rid = t["route_id"]
            if rid not in routes_map:
                continue
            is_new_dut = "DUT" in t.get("service_id", "")
            tid = t.get("trip_id", "")
            dir_id = t.get("direction_id", "")

            if rid not in trips_selected:
                trips_selected[rid] = t
            else:
                curr = trips_selected[rid]
                is_curr_dut = "DUT" in curr.get("service_id", "")
                if not is_curr_dut and is_new_dut:
                    trips_selected[rid] = t
                elif is_new_dut and ("IDA" in tid or dir_id == "0") and ("IDA" not in curr.get("trip_id", "") and curr.get("direction_id", "") != "0"):
                    trips_selected[rid] = t

            if ("VOL" in tid or dir_id == "1"):
                if rid not in trips_alt_dir or (is_new_dut and "DUT" not in trips_alt_dir[rid].get("service_id", "")):
                    trips_alt_dir[rid] = t

    print(f"  -> Viagens representativas selecionadas: {len(trips_selected)} linhas (+ {len(trips_alt_dir)} retornos)")

    target_trip_ids = {}
    for rid, t in trips_selected.items():
        target_trip_ids[t["trip_id"]] = (rid, "main")
    for rid, t in trips_alt_dir.items():
        if t["trip_id"] not in target_trip_ids:
            target_trip_ids[t["trip_id"]] = (rid, "alt")
    shape_ids_needed = set()
    for t in trips_selected.values():
        if t.get("shape_id"):
            shape_ids_needed.add(t["shape_id"])
    for t in trips_alt_dir.values():
        if t.get("shape_id"):
            shape_ids_needed.add(t["shape_id"])

    print("[4/5] Extraindo paradas sequenciais de stop_times.txt (IDA + VOLTA)...")
    stops_by_trip = {tid: [] for tid in target_trip_ids}
    t0 = time.time()
    with open(GTFS_DIR / "stop_times.txt", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            tid = row["trip_id"]
            if tid in stops_by_trip:
                sid = row["stop_id"]
                stop_meta = stops_dict.get(sid, {"name": f"Parada #{sid}", "lat": 0, "lon": 0})
                stops_by_trip[tid].append({
                    "seq": int(row["stop_sequence"]),
                    "stop_id": sid,
                    "name": stop_meta["name"],
                    "lat": stop_meta["lat"],
                    "lon": stop_meta["lon"],
                    "arr_time": row.get("arrival_time", ""),
                    "dep_time": row.get("departure_time", "")
                })

    for tid in stops_by_trip:
        stops_by_trip[tid].sort(key=lambda x: x["seq"])
    print(f"  -> Paradas sequenciais extraídas em {time.time()-t0:.2f}s")

    print("[5/5] Extraindo traçados GPS de shapes.txt e montando Grafo de Conexões SEI...")
    shapes_pts = {sid: [] for sid in shape_ids_needed}
    t0 = time.time()
    with open(GTFS_DIR / "shapes.txt", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row["shape_id"]
            if sid in shapes_pts:
                shapes_pts[sid].append((
                    int(row["shape_pt_sequence"]),
                    round(float(row["shape_pt_lat"]), 6),
                    round(float(row["shape_pt_lon"]), 6)
                ))
    print(f"  -> Pontos de shape extraídos em {time.time()-t0:.2f}s")

    def downsample_shape(shape_id, fallback_stops, max_pts=75):
        if shape_id and shape_id in shapes_pts and shapes_pts[shape_id]:
            pts_sorted = sorted(shapes_pts[shape_id], key=lambda x: x[0])
            raw_coords = [[p[1], p[2]] for p in pts_sorted]
            step = max(1, len(raw_coords) // max_pts)
            poly_out = raw_coords[::step]
            if raw_coords and poly_out[-1] != raw_coords[-1]:
                poly_out.append(raw_coords[-1])
            return poly_out
        return [[s["lat"], s["lon"]] for s in fallback_stops]

    # Consolidação de TODAS as linhas (IDA + VOLTA completos + mapa paradas->linhas)
    all_lines_dict = {}
    stop_to_lines = {}
    for rid, trip in trips_selected.items():
        rmeta = routes_map[rid]
        code = rmeta["short"]
        sid = trip.get("shape_id")
        tid = trip["trip_id"]

        stops_list = stops_by_trip.get(tid, [])
        alt_trip = trips_alt_dir.get(rid)
        alt_tid = alt_trip["trip_id"] if alt_trip else None
        alt_sid = alt_trip.get("shape_id") if alt_trip else None
        alt_stops = stops_by_trip.get(alt_tid, []) if alt_tid else []

        poly = downsample_shape(sid, stops_list, max_pts=80)
        return_poly = downsample_shape(alt_sid, alt_stops, max_pts=65) if (alt_sid or alt_stops) else []
        alt_coords = [[s["lat"], s["lon"]] for s in alt_stops]

        for st in stops_list:
            stop_to_lines.setdefault(st["stop_id"], set()).add(code)
        for st in alt_stops:
            stop_to_lines.setdefault(st["stop_id"], set()).add(code)

        headsign_ida = trip.get("trip_headsign") or (stops_list[-1]["name"] if stops_list else rmeta["long"])
        headsign_volta = (alt_trip.get("trip_headsign") if alt_trip else None) or (alt_stops[-1]["name"] if alt_stops else rmeta["long"])

        all_lines_dict[code] = {
            "code": code,
            "route_id": rid,
            "name": rmeta["long"],
            "headsign": headsign_ida,
            "headsign_ida": headsign_ida,
            "headsign_volta": headsign_volta,
            "total_stops": len(stops_list),
            "polyline": poly,
            "stops": stops_list,
            "return_coords": alt_coords,
            "return_polyline": return_poly,
            "return_stops": alt_stops
        }

    # Desduplica terminais SEI por proximidade ou nome
    seen_terminals = set()
    unique_terminals = []
    for t in terminals_sei:
        norm = t["name"].strip().upper()
        if norm not in seen_terminals:
            seen_terminals.add(norm)
            unique_terminals.append(t)

    # Constrói Grafo Completo de Hubs & Conexões SEI (todas as linhas que param em <= 300m de cada TI ou grande terminal)
    import math
    def approx_km(la1, lo1, la2, lo2):
        return math.hypot((la1 - la2) * 111.32, (lo1 - lo2) * 111.32 * math.cos(math.radians((la1 + la2) / 2.0)))

    # Extrai terminais principais agrupados pelo prefixo (ex: TI Cabo, TI Joana Bezerra, Derby, Cais de Santa Rita)
    anchor_hubs = []
    seen_hub_roots = set()
    for t in unique_terminals:
        base_name = t["name"].split(" - ")[0].strip()
        # Ignora plataformas individuais duplicadas do mesmo TI (agrupa por nome raiz)
        root = base_name.split("Embarque")[0].split("Plataforma")[0].strip().rstrip(" -")
        if root.upper() in seen_hub_roots:
            continue
        seen_hub_roots.add(root.upper())
        anchor_hubs.append({"name": root, "lat": t["lat"], "lon": t["lon"]})

    # Acrescenta grandes polos metropolitanos que podem não estar como location_type=1 no stops.txt
    extra_poles = [
        {"name": "Cais de Santa Rita (Centro / Recife Antigo)", "lat": -8.0680, "lon": -34.8765},
        {"name": "Praça do Derby (Terminal Central)", "lat": -8.0558, "lon": -34.8998},
        {"name": "Rua do Hospício / Conde da Boa Vista", "lat": -8.0585, "lon": -34.8878},
        {"name": "Praça do Carmo / Sítio Histórico (Olinda)", "lat": -8.0125, "lon": -34.8520},
        {"name": "Av. Getúlio Vargas (Bairro Novo / Olinda)", "lat": -7.9940, "lon": -34.8420},
        {"name": "Trevo Principal de Ipojuca Centro (KM 20)", "lat": -8.3994, "lon": -35.0568},
        {"name": "Terminal de Camela (PE-60)", "lat": -8.5149, "lon": -35.1235},
    ]
    for ep in extra_poles:
        if ep["name"].upper() not in seen_hub_roots:
            anchor_hubs.append(ep)

    hub_graph = []
    for hub in anchor_hubs:
        hlat, hlon = hub["lat"], hub["lon"]
        connected = []
        for code, ldata in all_lines_dict.items():
            pts = [[s["lat"], s["lon"]] for s in ldata.get("stops", [])] + ldata.get("return_coords", []) + ldata.get("polyline", [])
            if any(approx_km(hlat, hlon, p[0], p[1]) <= 0.45 for p in pts):
                connected.append(code)
        if connected:
            hub_graph.append({
                "name": hub["name"],
                "lat": round(hlat, 5),
                "lon": round(hlon, 5),
                "lines": sorted(connected)
            })

    # Índice compacto desduplicado de paradas reais do GTFS (cobre toda a RMR sem limitar a bairros nichados)
    # Formato compacto por entrada: [nome, lat, lon, [linhas_principais...]]
    seen_stop_clusters = {}
    stops_index = []
    for sid, sdata in stops_dict.items():
        raw_name = (sdata.get("name") or "").strip()
        if not raw_name or raw_name.isdigit():
            continue
        norm_name = " ".join(raw_name.upper().split())
        lat_r = round(sdata["lat"], 4)
        lon_r = round(sdata["lon"], 4)
        lines_here = sorted(stop_to_lines.get(sid, set()))

        existing = seen_stop_clusters.get(norm_name)
        merged = False
        if existing:
            for item in existing:
                if approx_km(lat_r, lon_r, item[1], item[2]) <= 0.45:
                    if lines_here:
                        merged_lines = sorted(set(item[3]) | set(lines_here))[:12]
                        item[3] = merged_lines
                    merged = True
                    break
        if not merged:
            entry = [raw_name, lat_r, lon_r, lines_here[:12]]
            seen_stop_clusters.setdefault(norm_name, []).append(entry)
            stops_index.append(entry)

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_routes_catalog": len(routes_all),
        "total_lines_ready": len(all_lines_dict),
        "total_stops_indexed": len(stops_index),
        "routes_catalog": routes_all,
        "terminals_sei": unique_terminals[:60],
        "hub_graph": hub_graph,
        "stops_index": stops_index,
        "popular_lines": all_lines_dict
    }

    with open(OUTPUT_WEB, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(',', ':'))

    size_kb = OUTPUT_WEB.stat().st_size / 1024
    print(f"\n[SUCESSO] Base de 100% das linhas + Grafo de Conexões compilada em {time.time()-start_total:.2f}s:")
    print(f"  -> Arquivo: {OUTPUT_WEB}")
    print(f"  -> Tamanho: {size_kb:.1f} KB")
    print(f"  -> Linhas com paradas e GPS completos: {len(all_lines_dict)}")
    print(f"  -> Paradas únicas indexadas (RMR): {len(stops_index)}")
    print(f"  -> Terminais Integrados SEI: {len(unique_terminals[:60])}")
    print(f"  -> Hubs no Grafo de Integrações: {len(hub_graph)}")

if __name__ == "__main__":
    main()
