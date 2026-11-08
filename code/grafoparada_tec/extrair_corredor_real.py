import csv
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

gtfs_dir = os.path.join("code", "grafoparada_tec", "data", "gtfs_granderecife")

# 1. Localizar Linhas 191 (Recife/Porto de Galinhas) e 178 (Porto de Suape/TI Cabo)
with open(os.path.join(gtfs_dir, "routes.txt"), encoding="utf-8") as f:
    routes = [r for r in csv.DictReader(f) if r.get("route_short_name") in ["191", "178", "195"]]

route_ids = {r["route_id"]: f"{r['route_short_name']} - {r['route_long_name']}" for r in routes}
print("Rotas analisadas:", route_ids)

# 2. Localizar viagens representativas
with open(os.path.join(gtfs_dir, "trips.txt"), encoding="utf-8") as f:
    trips = [t for t in csv.DictReader(f) if t["route_id"] in route_ids]

print(f"Total de viagens cadastradas: {len(trips)}")
sample_trip = trips[0]["trip_id"]
sample_route = route_ids[trips[0]["route_id"]]
print(f"\nViagem Selecionada: {sample_trip} ({sample_route})")

# 3. Sequência de paradas
with open(os.path.join(gtfs_dir, "stop_times.txt"), encoding="utf-8") as f:
    stop_times = [st for st in csv.DictReader(f) if st["trip_id"] == sample_trip]

stop_times.sort(key=lambda x: int(x["stop_sequence"]))
print(f"Total de paradas nessa viagem: {len(stop_times)}")

with open(os.path.join(gtfs_dir, "stops.txt"), encoding="utf-8") as f:
    stops_dict = {s["stop_id"]: s for s in csv.DictReader(f)}

# Salvar um CSV limpo com o corredor real
output_corredor_csv = os.path.join("code", "grafoparada_tec", "data", "corredor_real_linha178_191.csv")
with open(output_corredor_csv, mode="w", encoding="utf-8", newline="") as out_f:
    writer = csv.writer(out_f)
    writer.writerow(["seq", "stop_id", "stop_name", "lat", "lon", "scheduled_time"])
    for st in stop_times:
        s = stops_dict.get(st["stop_id"], {})
        writer.writerow([
            st["stop_sequence"],
            st["stop_id"],
            s.get("stop_name", ""),
            s.get("stop_lat", ""),
            s.get("stop_lon", ""),
            st["arrival_time"]
        ])

print(f"[+] Corredor real exportado com sucesso: {output_corredor_csv}")
print("\n--- Amostra das primeiras 10 paradas reais do corredor ---")
for st in stop_times[:10]:
    s = stops_dict.get(st["stop_id"], {})
    print(f"Passo {st['stop_sequence']:>2} [{st['arrival_time']}] - Parada {st['stop_id']}: {s.get('stop_name')}")
