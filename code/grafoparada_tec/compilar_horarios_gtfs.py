# -*- coding: utf-8 -*-
"""
Compilador Completo de Horarios Publicos GTFS & Catalogo RMR -> gtfs_schedules.json
Processa routes.txt, calendar.txt, trips.txt, stop_times.txt e stops.txt (CTM Grande Recife)
para todas as 393 linhas ativas (IDA/VOLTA x DUT/SAB/DOM), gerando:
  - first_dep, last_dep, trip_count, duration_min (mediana real)
  - headways_min por faixa horaria (madrugada, pico_manha, entre_picos, pico_tarde, noite)
  - dep_mins (array compacto de minutos inteiros desde 00:00 ordenados)
  - stop_offsets_min (deslocamento medio em min ao longo das paradas do trajeto)
  - rmr_places (14 cidades oficiais da RMR + terminais/estacoes/polos reais do GTFS)
"""

import csv
import json
import math
import re
import statistics
import time
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
GTFS_DIR = BASE_DIR / "data" / "gtfs_granderecife"
NETWORK_JSON = BASE_DIR.parent / "grafoparada_web" / "data" / "gtfs_real_network.json"
OUTPUT_JSON = BASE_DIR.parent / "grafoparada_web" / "data" / "gtfs_schedules.json"

TIME_BANDS = (
    ("madrugada", 0, 300),
    ("pico_manha", 300, 540),
    ("entre_picos", 540, 960),
    ("pico_tarde", 960, 1200),
    ("noite", 1200, 1440),
)

# 14 municipios oficiais da Regiao Metropolitana do Recife (RMR) com ancoras reais
# para classificacao geografica precisa de paradas e terminais (zero dados ficticios).
RMR_CITIES_META = [
    {
        "city": "Recife",
        "lat": -8.05428,
        "lon": -34.88130,
        "neighborhood": "Centro / Boa Vista",
        "anchors": [
            (-8.05428, -34.88130),  # Centro / Boa Vista
            (-8.12201, -34.91246),  # Tancredo Neves / Imbiribeira
            (-8.11800, -34.89600),  # Boa Viagem
            (-8.08817, -34.94586),  # Barro
            (-8.03121, -34.95494),  # Caxanga / Varzea
            (-8.00824, -34.93833),  # Macaxeira / Casa Amarela
            (-8.07800, -34.91800),  # Afogados / Joana Bezerra
            (-8.13414, -34.91512),  # Aeroporto / Ibura
        ],
    },
    {
        "city": "Olinda",
        "lat": -8.00889,
        "lon": -34.85528,
        "neighborhood": "Carmo / Bairro Novo",
        "anchors": [
            (-8.00889, -34.85528),  # Carmo / Varadouro
            (-7.98272, -34.85632),  # PE-15 / Ouro Preto
            (-7.97300, -34.84100),  # Rio Doce / Casa Caiada
            (-8.00120, -34.89263),  # Xamba / Aguas Compridas
        ],
    },
    {
        "city": "Jaboatão dos Guararapes",
        "lat": -8.11278,
        "lon": -35.01472,
        "neighborhood": "Jaboatão Centro / Prazeres",
        "anchors": [
            (-8.11278, -35.01472),  # Jaboatao Centro
            (-8.16142, -34.92656),  # Prazeres / Cajueiro Seco
            (-8.18000, -34.92000),  # Piedade / Candeias / Barra de Jangada
            (-8.09452, -34.97291),  # Cavaleiro
            (-8.06429, -34.98207),  # Curado / TIP
        ],
    },
    {
        "city": "Cabo de Santo Agostinho",
        "lat": -8.28694,
        "lon": -35.03472,
        "neighborhood": "Centro / Ponte dos Carvalhos",
        "anchors": [
            (-8.28694, -35.03472),  # Cabo Centro
            (-8.22700, -34.97800),  # Ponte dos Carvalhos
            (-8.33000, -34.96000),  # Gaibu / Suape Norte
        ],
    },
    {
        "city": "Ipojuca",
        "lat": -8.39944,
        "lon": -35.06361,
        "neighborhood": "Ipojuca Centro / Camela",
        "anchors": [
            (-8.39944, -35.06361),  # Ipojuca Centro
            (-8.51489, -35.12354),  # Camela
            (-8.50000, -35.00500),  # Porto de Galinhas / Maracaipe
            (-8.44500, -35.03500),  # Nossa Senhora do O
        ],
    },
    {
        "city": "Camaragibe",
        "lat": -8.02194,
        "lon": -34.98139,
        "neighborhood": "Centro / Aldeia",
        "anchors": [
            (-8.02479, -34.99606),  # TI Camaragibe / Centro
            (-7.96500, -34.98500),  # Aldeia
        ],
    },
    {
        "city": "Paulista",
        "lat": -7.94083,
        "lon": -34.87278,
        "neighborhood": "Centro / Janga / Maranguape",
        "anchors": [
            (-7.94677, -34.87786),  # Pelopidas / Centro
            (-7.93500, -34.84000),  # Janga / Pau Amarelo / Maria Farinha
            (-7.93000, -34.89000),  # Maranguape
        ],
    },
    {
        "city": "Abreu e Lima",
        "lat": -7.91139,
        "lon": -34.90278,
        "neighborhood": "Centro / Caetés",
        "anchors": [
            (-7.91139, -34.90278),
            (-7.91500, -34.92500),  # Caetes
        ],
    },
    {
        "city": "Igarassu",
        "lat": -7.83417,
        "lon": -34.90639,
        "neighborhood": "Centro / Cruz de Rebouças",
        "anchors": [
            (-7.83283, -34.91192),  # TI Igarassu / Centro
            (-7.86500, -34.90500),  # Cruz de Reboucas
        ],
    },
    {
        "city": "São Lourenço da Mata",
        "lat": -8.00222,
        "lon": -35.01833,
        "neighborhood": "Centro / Tiúma",
        "anchors": [
            (-8.00222, -35.01833),
            (-8.02800, -35.06000),  # Tiuma / Arena
        ],
    },
    {
        "city": "Moreno",
        "lat": -8.11861,
        "lon": -35.09194,
        "neighborhood": "Centro / Bonança",
        "anchors": [
            (-8.11861, -35.09194),
            (-8.09500, -35.06500),  # Bonanca
        ],
    },
    {
        "city": "Itamaracá",
        "lat": -7.74806,
        "lon": -34.82556,
        "neighborhood": "Pilar / Forte Orange",
        "anchors": [(-7.74806, -34.82556)],
    },
    {
        "city": "Itapissuma",
        "lat": -7.77639,
        "lon": -34.89417,
        "neighborhood": "Centro / Mangabeira",
        "anchors": [(-7.77639, -34.89417)],
    },
    {
        "city": "Araçoiaba",
        "lat": -7.79083,
        "lon": -35.09083,
        "neighborhood": "Centro",
        "anchors": [(-7.79083, -35.09083)],
    },
]

CITY_NAME_KEYWORDS = [
    ("JABOATÃO", "Jaboatão dos Guararapes"),
    ("JABOATAO", "Jaboatão dos Guararapes"),
    ("PRAZERES", "Jaboatão dos Guararapes"),
    ("PIEDADE", "Jaboatão dos Guararapes"),
    ("CAJUEIRO SECO", "Jaboatão dos Guararapes"),
    ("BARRA DE JANGADA", "Jaboatão dos Guararapes"),
    ("MURIBECA", "Jaboatão dos Guararapes"),
    ("CAVALEIRO", "Jaboatão dos Guararapes"),
    ("MARCOS FREIRE", "Jaboatão dos Guararapes"),
    ("CURADO", "Jaboatão dos Guararapes"),
    ("PONTE DOS CARVALHOS", "Cabo de Santo Agostinho"),
    ("TI CABO", "Cabo de Santo Agostinho"),
    ("TERMINAL DO CABO", "Cabo de Santo Agostinho"),
    ("ESTAÇÃO CABO", "Cabo de Santo Agostinho"),
    ("SUAPE", "Cabo de Santo Agostinho"),
    ("IPOJUCA", "Ipojuca"),
    ("CAMELA", "Ipojuca"),
    ("OLINDA", "Olinda"),
    ("XAMBÁ", "Olinda"),
    ("XAMBA", "Olinda"),
    ("PE-15", "Olinda"),
    ("PE 15", "Olinda"),
    ("RIO DOCE", "Olinda"),
    ("BAIRRO NOVO", "Olinda"),
    ("CARMO", "Olinda"),
    ("CAMARAGIBE", "Camaragibe"),
    ("ALDEIA", "Camaragibe"),
    ("PAULISTA", "Paulista"),
    ("PELÓPIDAS", "Paulista"),
    ("PELOPIDAS", "Paulista"),
    ("ABREU E LIMA", "Abreu e Lima"),
    ("IGARASSU", "Igarassu"),
    ("CRUZ DE REBOUÇAS", "Igarassu"),
    ("SÃO LOURENÇO", "São Lourenço da Mata"),
    ("MORENO", "Moreno"),
    ("BONANÇA", "Moreno"),
    ("ITAMARACÁ", "Itamaracá"),
    ("ITAPISSUMA", "Itapissuma"),
    ("ARAÇOIABA", "Araçoiaba"),
]


def approx_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    return math.hypot(
        (lat1 - lat2) * 111.32,
        (lon1 - lon2) * 111.32 * math.cos(math.radians((lat1 + lat2) / 2.0)),
    )


def assign_rmr_city(lat: float, lon: float, name: str = "") -> str:
    uname = (name or "").upper()
    for kw, cname in CITY_NAME_KEYWORDS:
        if kw in uname:
            return cname

    best_city = "Recife"
    best_dist = float("inf")
    for cmeta in RMR_CITIES_META:
        for alat, alon in cmeta["anchors"]:
            d = approx_km(lat, lon, alat, alon)
            if d < best_dist:
                best_dist = d
                best_city = cmeta["city"]
    return best_city


def parse_gtfs_seconds(tstr: str) -> int:
    h, m, s = tstr.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def format_hhmm(minutes_from_midnight: int) -> str:
    h = minutes_from_midnight // 60
    m = minutes_from_midnight % 60
    return f"{h:02d}:{m:02d}"


def resolve_service_buckets(cal_row: dict, service_id: str) -> list[str]:
    buckets = []
    if cal_row:
        if any(cal_row.get(d) == "1" for d in ("monday", "tuesday", "wednesday", "thursday", "friday")):
            buckets.append("DUT")
        if cal_row.get("saturday") == "1":
            buckets.append("SAB")
        if cal_row.get("sunday") == "1":
            buckets.append("DOM")
    if not buckets:
        sid_u = service_id.upper()
        for b in ("DUT", "SAB", "DOM"):
            if b in sid_u:
                buckets.append(b)
    return buckets


def compute_headways_by_band(dep_mins: list[int]) -> dict[str, float | None]:
    if not dep_mins:
        return {b[0]: None for b in TIME_BANDS}

    sorted_deps = sorted(dep_mins)
    headways: dict[str, float | None] = {}

    for band_name, start_m, end_m in TIME_BANDS:
        band_indices = [i for i, m in enumerate(sorted_deps) if start_m <= (m % 1440) < end_m]
        if not band_indices:
            headways[band_name] = None
            continue

        diffs = []
        for idx in band_indices:
            if idx + 1 < len(sorted_deps):
                gap = sorted_deps[idx + 1] - sorted_deps[idx]
                if 0 < gap <= 180:
                    # Prefer intervals whose next departure is in the same band, or nearby boundary (< 180 min)
                    next_mod = sorted_deps[idx + 1] % 1440
                    if start_m <= next_mod < end_m or len(band_indices) == 1:
                        diffs.append(gap)

        if not diffs and len(band_indices) >= 2:
            for j in range(len(band_indices) - 1):
                gap = sorted_deps[band_indices[j + 1]] - sorted_deps[band_indices[j]]
                if 0 < gap <= 240:
                    diffs.append(gap)

        headways[band_name] = round(float(statistics.median(diffs)), 1) if diffs else None

    return headways


def clean_stop_root_name(raw_name: str) -> str:
    name = " ".join((raw_name or "").strip().split())
    # Remove sufixo numerico padrao GTFS (" - 020000")
    if " - " in name and name.split(" - ")[-1].strip().isdigit():
        name = " - ".join(name.split(" - ")[:-1]).strip()
    # Normaliza variacoes de direcao/modulo/embarque
    name = re.sub(r"\s+(Ida|Volta|Retorno)\s*$", "", name, flags=re.IGNORECASE).strip()
    name = re.sub(r"\s+M[oó]dulo\s+[IVX0-9]+\s*$", "", name, flags=re.IGNORECASE).strip()
    name = re.sub(r"\s+(Embarque|Desembarque|Plataforma).*$", "", name, flags=re.IGNORECASE).strip()
    return name.rstrip(" -")


def infer_neighborhood(name: str, fallback_city: str) -> str:
    clean = clean_stop_root_name(name)
    for prefix in ("TI ", "Ti ", "Terminal Integrado ", "Terminal De ", "Terminal Do ", "Terminal Da ", "Terminal ", "Estação ", "Estacao ", "Pátio ", "Ponto De Retorno "):
        if clean.startswith(prefix):
            clean = clean[len(prefix):].strip()
            break
    clean = re.sub(r"^Linha\s+\d+\s*:?\s*", "", clean, flags=re.IGNORECASE).strip()
    return clean if clean else fallback_city


def build_schedules_and_places() -> dict:
    t_start = time.time()
    print("[1/5] Lendo routes.txt, calendar.txt, trips.txt e stops.txt (UTF-8)...")

    routes_meta = {}
    with open(GTFS_DIR / "routes.txt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            routes_meta[r["route_id"]] = {
                "route_id": r["route_id"],
                "code": r["route_short_name"],
                "name": r["route_long_name"],
            }

    calendar_map = {}
    with open(GTFS_DIR / "calendar.txt", encoding="utf-8") as f:
        for c in csv.DictReader(f):
            calendar_map[c["service_id"]] = c

    stops_dict = {}
    with open(GTFS_DIR / "stops.txt", encoding="utf-8") as f:
        for s in csv.DictReader(f):
            sid = s["stop_id"]
            stops_dict[sid] = {
                "id": sid,
                "name": (s["stop_name"] or "").strip(),
                "lat": float(s["stop_lat"]),
                "lon": float(s["stop_lon"]),
            }

    trip_info = {}  # trip_id -> (route_id, dir_key, [service_buckets])
    with open(GTFS_DIR / "trips.txt", encoding="utf-8") as f:
        for t in csv.DictReader(f):
            rid = t["route_id"]
            if rid not in routes_meta:
                continue
            tid = t["trip_id"]
            did = t.get("direction_id", "")
            tid_u = tid.upper()
            if did == "1" or ("VOL" in tid_u and did != "0"):
                dkey = "volta"
            else:
                dkey = "ida"
            svcs = resolve_service_buckets(calendar_map.get(t["service_id"]), t["service_id"])
            trip_info[tid] = (rid, dkey, svcs)

    print(f"  -> {len(routes_meta)} rotas no catalogo, {len(trip_info)} viagens mapeadas, {len(stops_dict)} paradas.")

    # Carrega sequencia canonica de paradas do gtfs_real_network.json (se disponivel) para alinhar stop_offsets_min 1:1
    canonical_stops_by_code = {}
    hub_graph_raw = []
    if NETWORK_JSON.is_file():
        with open(NETWORK_JSON, encoding="utf-8") as f:
            net_data = json.load(f)
        hub_graph_raw = net_data.get("hub_graph", [])
        for code, ldata in net_data.get("popular_lines", {}).items():
            canonical_stops_by_code[(code, "ida")] = [s["stop_id"] for s in ldata.get("stops", [])]
            canonical_stops_by_code[(code, "volta")] = [s["stop_id"] for s in ldata.get("return_stops", [])]

    print("[2/5] Processando stop_times.txt em streaming (3.1M+ registros)...")
    t0 = time.time()
    # Acumuladores por viagem (cada trip tem paradas sequenciais)
    trip_stops: dict[str, list[tuple[int, str, int, int]]] = defaultdict(list)
    stop_to_routes: dict[str, set[str]] = defaultdict(set)

    with open(GTFS_DIR / "stop_times.txt", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader, None)  # cabecalho
        for row in reader:
            if not row:
                continue
            tid = row[0]
            tmeta = trip_info.get(tid)
            if tmeta is None:
                continue
            arr_s = parse_gtfs_seconds(row[1])
            dep_s = parse_gtfs_seconds(row[2])
            sid = row[3]
            seq = int(row[4])
            trip_stops[tid].append((seq, sid, arr_s, dep_s))
            stop_to_routes[sid].add(routes_meta[tmeta[0]]["code"])

    print(f"  -> stop_times.txt lido em {time.time() - t0:.2f}s ({len(trip_stops)} viagens).")

    print("[3/5] Agregando horarios por linha, sentido (IDA/VOLTA), servico (DUT/SAB/DOM) e offsets...")
    # Estrutura: agg[(code, dkey, svc)] -> {"deps": [], "durs": []}
    agg_svc = defaultdict(lambda: {"deps": [], "durs": []})
    # Fallback de sequencia canonica caso alguma linha nao tenha no network_json
    fallback_seq: dict[tuple[str, str], list[str]] = {}
    fallback_seq_score: dict[tuple[str, str], tuple[int, int]] = {}

    # Primeiro passo: ordena paradas de cada trip e coleta partidas/duracoes + melhor sequencia canonica
    for tid, pts in trip_stops.items():
        pts.sort(key=lambda x: x[0])
        rid, dkey, svcs = trip_info[tid]
        code = routes_meta[rid]["code"]

        first_dep_sec = pts[0][3]
        last_arr_sec = pts[-1][2]
        dep_min = int(round(first_dep_sec / 60.0))
        dur_min = max(1.0, (last_arr_sec - first_dep_sec) / 60.0)

        for svc in svcs:
            agg_svc[(code, dkey, svc)]["deps"].append(dep_min)
            agg_svc[(code, dkey, svc)]["durs"].append(dur_min)

        is_dut = 1 if "DUT" in svcs else 0
        score = (is_dut, len(pts))
        if score > fallback_seq_score.get((code, dkey), (-1, -1)):
            fallback_seq_score[(code, dkey)] = score
            fallback_seq[(code, dkey)] = [p[1] for p in pts]

    # Segundo passo: calcula stop_offsets_min alinhados a sequencia canonica de paradas do trajeto
    offset_sum: dict[tuple[str, str], list[float]] = {}
    offset_cnt: dict[tuple[str, str], list[int]] = {}
    canon_index_map: dict[tuple[str, str], dict[str, list[int]]] = {}

    active_codes = sorted({routes_meta[tmeta[0]]["code"] for tmeta in trip_info.values()})
    for code in active_codes:
        for dkey in ("ida", "volta"):
            seq_ids = canonical_stops_by_code.get((code, dkey)) or fallback_seq.get((code, dkey)) or []
            if not seq_ids:
                continue
            n_stops = len(seq_ids)
            offset_sum[(code, dkey)] = [0.0] * n_stops
            offset_cnt[(code, dkey)] = [0] * n_stops
            idx_map: dict[str, list[int]] = defaultdict(list)
            for idx, sid in enumerate(seq_ids):
                idx_map[sid].append(idx)
            canon_index_map[(code, dkey)] = idx_map

    for tid, pts in trip_stops.items():
        rid, dkey, _ = trip_info[tid]
        code = routes_meta[rid]["code"]
        key = (code, dkey)
        sums = offset_sum.get(key)
        if not sums:
            continue
        cnts = offset_cnt[key]
        idx_map = canon_index_map[key]
        n_canon = len(sums)
        n_trip = len(pts)
        t0_sec = pts[0][3]

        if n_trip == n_canon and all(pts[i][1] in idx_map and i in idx_map[pts[i][1]] for i in range(n_trip)):
            for i, (_, _, arr_s, _) in enumerate(pts):
                sums[i] += max(0.0, (arr_s - t0_sec) / 60.0)
                cnts[i] += 1
        else:
            denom_trip = max(1, n_trip - 1)
            denom_canon = max(1, n_canon - 1)
            for ti, (_, sid, arr_s, _) in enumerate(pts):
                cands = idx_map.get(sid)
                if not cands:
                    continue
                if len(cands) == 1:
                    target_idx = cands[0]
                else:
                    rel_t = ti / denom_trip
                    target_idx = min(cands, key=lambda ci: abs((ci / denom_canon) - rel_t))
                sums[target_idx] += max(0.0, (arr_s - t0_sec) / 60.0)
                cnts[target_idx] += 1

    # Monta dicionario final por linha (todas as 393 linhas)
    lines_payload = {}
    code_to_meta = {m["code"]: m for m in routes_meta.values()}
    for code in active_codes:
        rm = code_to_meta[code]
        line_entry = {
            "route_id": rm["route_id"],
            "name": rm["name"],
            "ida": {},
            "volta": {},
        }
        for dkey in ("ida", "volta"):
            dir_obj = {}
            has_dir = False
            for svc in ("DUT", "SAB", "DOM"):
                bucket = agg_svc.get((code, dkey, svc))
                if not bucket or not bucket["deps"]:
                    continue
                has_dir = True
                deps_sorted = sorted(bucket["deps"])
                dur_med = round(float(statistics.median(bucket["durs"])), 1)
                dir_obj[svc] = {
                    "first_dep": format_hhmm(deps_sorted[0]),
                    "last_dep": format_hhmm(deps_sorted[-1]),
                    "trip_count": len(deps_sorted),
                    "duration_min": dur_med,
                    "headways_min": compute_headways_by_band(deps_sorted),
                    "dep_mins": deps_sorted,
                }

            sums = offset_sum.get((code, dkey))
            cnts = offset_cnt.get((code, dkey))
            if sums and cnts:
                offsets = []
                last_val = 0.0
                for s_val, c_val in zip(sums, cnts):
                    if c_val > 0:
                        val = round(s_val / c_val, 1)
                        last_val = max(last_val, val)
                    else:
                        val = round(last_val, 1)
                    offsets.append(val)
                dir_obj["stop_offsets_min"] = offsets
            elif has_dir:
                dir_obj["stop_offsets_min"] = []

            line_entry[dkey] = dir_obj

        lines_payload[code] = line_entry

    print(f"[4/5] Construindo catalogo real rmr_places (14 cidades RMR + terminais/estacoes/polos)...")
    # Mapeia todas as paradas reais para as 14 cidades oficiais da RMR
    city_stops: dict[str, list[dict]] = defaultdict(list)
    city_lines: dict[str, set[str]] = defaultdict(set)
    stop_city_cache: dict[str, str] = {}

    for sid, s in stops_dict.items():
        c = assign_rmr_city(s["lat"], s["lon"], s["name"])
        stop_city_cache[sid] = c
        city_stops[c].append(s)
        city_lines[c].update(stop_to_routes.get(sid, set()))

    rmr_places = []
    # 1. As 14 cidades oficiais da RMR
    for cmeta in RMR_CITIES_META:
        cname = cmeta["city"]
        slist = city_stops.get(cname, [])
        rmr_places.append({
            "name": cname,
            "type": "city",
            "city": cname,
            "neighborhood": cmeta["neighborhood"],
            "lat": round(cmeta["lat"], 5),
            "lon": round(cmeta["lon"], 5),
            "stop_count": len(slist),
            "lines": sorted(city_lines.get(cname, set())),
        })

    # 2. Terminais, Estacoes BRT/Metro e Polos reais de stops.txt e hub_graph
    place_clusters: dict[str, list[dict]] = defaultdict(list)

    for sid, s in stops_dict.items():
        raw_name = s["name"]
        if not raw_name or raw_name.isdigit():
            continue
        root = clean_stop_root_name(raw_name)
        if not root or root.isdigit():
            continue
        norm = root.upper()
        matched = None
        for existing in place_clusters.get(norm, []):
            if approx_km(s["lat"], s["lon"], existing["lat"], existing["lon"]) <= 0.45:
                matched = existing
                break
        if matched:
            matched["coords"].append((s["lat"], s["lon"]))
            matched["lines"].update(stop_to_routes.get(sid, set()))
            matched["stop_ids"].add(sid)
        else:
            place_clusters[norm].append({
                "name": root,
                "lat": s["lat"],
                "lon": s["lon"],
                "coords": [(s["lat"], s["lon"])],
                "lines": set(stop_to_routes.get(sid, set())),
                "stop_ids": {sid},
                "source": "stops",
            })

    # Inclui polos extras do hub_graph que nao estejam duplicados
    for hub in hub_graph_raw:
        hname = (hub.get("name") or "").strip()
        if not hname:
            continue
        hlat, hlon = float(hub["lat"]), float(hub["lon"])
        root = clean_stop_root_name(hname)
        norm = root.upper()
        already = False
        for cands in place_clusters.values():
            for ex in cands:
                if approx_km(hlat, hlon, ex["lat"], ex["lon"]) <= 0.25 and (
                    norm in ex["name"].upper() or ex["name"].upper() in norm
                ):
                    ex["lines"].update(hub.get("lines", []))
                    already = True
                    break
            if already:
                break
        if not already:
            place_clusters[norm].append({
                "name": hname,
                "lat": hlat,
                "lon": hlon,
                "coords": [(hlat, hlon)],
                "lines": set(hub.get("lines", [])),
                "stop_ids": set(),
                "source": "hub_graph",
            })

    # Calcula stop_count real no raio de 0.45km e linhas reais para cada lugar
    all_stops_list = list(stops_dict.values())
    named_places = []
    for cands in place_clusters.values():
        for p in cands:
            clat = sum(c[0] for c in p["coords"]) / len(p["coords"])
            clon = sum(c[1] for c in p["coords"]) / len(p["coords"])
            nearby_stops = [
                st for st in all_stops_list if approx_km(clat, clon, st["lat"], st["lon"]) <= 0.45
            ]
            lines_here = set(p["lines"])
            for st in nearby_stops:
                lines_here.update(stop_to_routes.get(st["id"], set()))
            if not lines_here:
                continue

            uname = p["name"].upper()
            if "ESTAÇÃO" in uname or "ESTACAO" in uname:
                ptype = "station"
            elif "TI " in uname or "TERMINAL" in uname or "PÁTIO" in uname or "PONTO DE RETORNO" in uname:
                ptype = "terminal"
            else:
                ptype = "pole"

            pcity = assign_rmr_city(clat, clon, p["name"])
            pneigh = infer_neighborhood(p["name"], pcity)
            named_places.append({
                "name": p["name"],
                "type": ptype,
                "city": pcity,
                "neighborhood": pneigh,
                "lat": round(clat, 5),
                "lon": round(clon, 5),
                "stop_count": max(len(nearby_stops), len(p["stop_ids"]), 1),
                "lines": sorted(lines_here),
            })

    named_places.sort(key=lambda x: (x["city"], -len(x["lines"]), x["name"]))
    rmr_places.extend(named_places)

    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "GTFS CTM Grande Recife",
        "schedule_label": "Horário Programado · GTFS",
        "total_lines": len(lines_payload),
        "total_rmr_cities": len(RMR_CITIES_META),
        "total_rmr_places": len(rmr_places),
        "time_bands": {b[0]: [b[1], b[2]] for b in TIME_BANDS},
        "lines": lines_payload,
        "rmr_places": rmr_places,
    }

    print(f"[5/5] Gravando JSON compacto em {OUTPUT_JSON}...")
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size_kb = OUTPUT_JSON.stat().st_size / 1024.0
    print(f"\n[SUCESSO] gtfs_schedules.json gerado em {time.time() - t_start:.2f}s")
    print(f"  -> Tamanho: {size_kb:.1f} KB ({OUTPUT_JSON.stat().st_size:,} bytes)")
    print(f"  -> Linhas compiladas: {len(lines_payload)}/393")
    print(f"  -> Lugares RMR indexados: {len(rmr_places)} ({len(RMR_CITIES_META)} cidades + {len(named_places)} terminais/estacoes/polos)")
    return payload


if __name__ == "__main__":
    build_schedules_and_places()
