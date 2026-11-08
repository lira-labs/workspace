import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

gtfs_dir = os.path.join("code", "grafoparada_tec", "data", "gtfs_granderecife")

stops_file = os.path.join(gtfs_dir, "stops.txt")
routes_file = os.path.join(gtfs_dir, "routes.txt")
trips_file = os.path.join(gtfs_dir, "trips.txt")

with open(stops_file, mode="r", encoding="utf-8") as f:
    stops = list(csv.DictReader(f))

print(f"[*] Total de paradas cadastradas no Grande Recife: {len(stops):,}")

# Filtrar paradas no corredor de Ipojuca / Cabo / PE-60 / Suape / Camela / Porto de Galinhas
termos = ["ipojuca", "pe-60", "camela", "suape", "gaibu", "porto de galinhas", "cabo"]
paradas_corredor = []
for s in stops:
    nome = s.get("stop_name", "").lower()
    desc = s.get("stop_desc", "").lower()
    if any(t in nome or t in desc for t in termos):
        paradas_corredor.append(s)

print(f"[*] Paradas encontradas na região de interesse: {len(paradas_corredor):,}")

print("\n--- Exemplos de Paradas Reais no Corredor ---")
for p in paradas_corredor[:10]:
    print(f"ID: {p['stop_id']:<6} | Nome: {p['stop_name']:<45} | Coord: ({p['stop_lat']}, {p['stop_lon']})")

with open(routes_file, mode="r", encoding="utf-8") as f:
    routes = list(csv.DictReader(f))

print(f"\n[*] Total de linhas cadastradas: {len(routes):,}")
rotas_corredor = [
    r for r in routes
    if any(t in r.get("route_long_name", "").lower() or t in r.get("route_short_name", "").lower() for t in termos)
]
print(f"[*] Linhas metropolitanas na região: {len(rotas_corredor):,}")
for r in rotas_corredor[:12]:
    print(f"Linha {r.get('route_short_name', 'S/N'):<6} - {r.get('route_long_name', '')}")
