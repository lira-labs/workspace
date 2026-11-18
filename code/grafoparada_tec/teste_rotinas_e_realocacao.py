# -*- coding: utf-8 -*-
"""
Bateria de Testes Automatizados · Conformidade Operacional, Científica e Usabilidade
Projeto GrafoParada · Tópicos Avançados em Inteligência Artificial (AI4Good / UFRPE)
Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)

Validações cobertas:
1. Interface v3 Zero Hardcoding, Cadastro Obrigatório e Fluxo Guiado em Cascata RMR
2. Integridade Física da Apresentação Oficial da Banca (GrafoParada_Seminario2_CauaLira.pptx)
3. Cômputo da Penalidade de Percepção de Tempo (1,68x · Yap & Cats, 2021)
4. Modelo Logístico de Abandono de Passageiros (Passenger Reneging · Kim et al., 2026)
5. Mecanismo de Trava Híbrida Defensiva Anti-Oversmoothing (Δ > 15 min) & Despacho CTM
6. Banco SQLite (`db_manager.py`) em arquivo temporário + Catálogo GTFS Horários (`gtfs_schedules.json`)
7. Fluxo Progressivo de Telas & Inteligência GTFS da Laya IA em Node.js
"""
from __future__ import annotations

import http.server
import json
import os
import socketserver
import subprocess
import sys
import tempfile
import threading
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
TEC_DIR = ROOT / "code" / "grafoparada_tec"
WEB_DIR = ROOT / "code" / "grafoparada_web"
if str(TEC_DIR) not in sys.path:
    sys.path.insert(0, str(TEC_DIR))

from db_manager import (  # noqa: E402
    get_training_dataset,
    init_db,
    record_observation,
    register_user,
    save_routine,
    sync_cloud_observations,
)
from modelo_predicao_e_abandono import (  # noqa: E402
    avaliar_gatilho_despacho_emergencial,
    avaliar_trava_hibrida_defensiva,
    calcular_probabilidade_reneging,
    calcular_tempo_percebido,
)

HTML_PATH = WEB_DIR / "index.html"
ROTEIRO_PATH = WEB_DIR / "roteiro.html"
ENGINE_JS = WEB_DIR / "real_transit_engine.js"
GTFS_JSON = WEB_DIR / "data" / "gtfs_real_network.json"
GTFS_SCHEDULES_JSON = WEB_DIR / "data" / "gtfs_schedules.json"
MODEL_STATUS_JSON = WEB_DIR / "data" / "model_training_status.json"
DECK_PATH = WEB_DIR / "GrafoParada_Seminario2_CauaLira.pptx"

FORBIDDEN_HARDCODED_TOKENS = [
    "UFRPE-TESTE-2026",
    "Derby / Rui Barbosa",
    "Praça do Derby (Parada 180412)",
    "enterAsQuickGuest",
    "setQuickDest",
    "Cauã Cunha",
    "07:30",
    "17:30",
]

REQUIRED_GUIDED_UI_TOKENS = [
    ("Modal de Onboarding Obrigatório", "modal-onboarding"),
    ("Passo 1: Cadastro Leve LGPD", "onboarding-step-register"),
    ("Passo 2: Rotina em Cascata RMR", "onboarding-step-routine"),
    ("Autocomplete Origem RMR", "onb-origin-place"),
    ("Autocomplete Destino RMR", "onb-dest-place"),
    ("Caixa de Linhas Sugeridas GTFS", "onb-suggested-lines-box"),
    ("Modal de Edição de Rotina Diária", "modal-routine"),
    ("Controlador Compartilhado em Cascata", "createCascadeRoutineController"),
    ("Badge de Proveniência Programada GTFS", "Horário Programado · GTFS"),
    ("Mapeador de Rotina Pendular (Card Inicial)", "routine-commute-card"),
    ("Pill de Rotina Superior", "label-routine-pill"),
    ("Letreiro de LED Idêntico ao Coletivo", "bus-led-sign-box"),
    ("Visor Frontal Comparável ao Ônibus", "Confira este letreiro com a frente do ônibus"),
    ("Botão Gigante de Leitura em Voz Alta Sênior", "btn-senior-voice-big"),
    ("Modo Bolso Seguro Anti-Assalto (0 Nits)", "pocket-shield-screen"),
    ("Modo Offline Inercial na PE-60 (Dead Reckoning)", "offline-inertial-banner"),
    ("Realocação por Horário de Pico vs Fora de Pico", "Fora de Pico"),
    ("Rotina Completa Ida + Volta e Parada Base", "inp-custom-return-origin"),
    ("Botão Global de Voz Laya (Mutar / Ativar)", "top-voice-toggle-pill"),
    ("Guia de Perdido Conversacional", "lost-dest-input"),
    ("Alerta de Alagamento PE-60 Km 14 (Desvio UPA)", "flood-alert-banner"),
    ("Lei Estadual 15.878/2016 (Parada Segura)", "modal-safe-disembark"),
    ("Farol Noturno de Embarque (Anti-Queima)", "night-beacon-screen"),
    ("Sensor Forense de Queima de Parada", "modal-queima-parada"),
    ("Guardião da Integração Temporal VEM (120 min)", "modal-vem"),
    ("Tela 1 Início Contextual", "app-screen-home"),
    ("Pergunta Contextual Direta", "Está indo trabalhar ou estudar hoje?"),
    ("Tela 2 Localização Guiada", "app-screen-locate"),
    ("Tela 5 Central CTM & Pesquisa", "app-screen-central"),
    ("Controlador de Transição Suave (navigateToScreen)", "function navigateToScreen("),
    ("WebMCP Declarativo na Busca de Rotas", 'toolname="grafoparada_plan_from_locate"'),
    ("Detecção Dinâmica sem Parada Fixa", "Detectando linha próxima..."),
    ("Normalização Fonética de Voz PT-BR", "formatSpeechPortuguese"),
    ("Opções de Rota Multi-Leg", "locate-route-options"),
    ("Seleção de Opção no Mapa", "selectGoogleMapsOption"),
    ("Check-in Cidadão na Parada (v3.1)", "stop-checkin-box"),
    ("Status Banco & Modelo no Perfil (v3.1)", "prof-cloud-status"),
    ("Status Neon na Central CTM (v3.1)", "ctm-neon-sync-line"),
    ("Status Neon em Pesquisa & Banca (v3.1)", "lab-neon-live-status"),
    ("Função submitStopTelemetryCheckin (v3.1)", "submitStopTelemetryCheckin"),
    ("Função refreshCloudTelemetryUI (v3.1)", "refreshCloudTelemetryUI"),
]


def _load_html() -> str:
    assert HTML_PATH.is_file(), f"Arquivo não encontrado: {HTML_PATH}"
    return HTML_PATH.read_text(encoding="utf-8")


def _run_laya_node_suite() -> dict:
    node_eval = """
const fs = require('fs');
const registeredWebMcp = [];
global.window = {};
global.document = { getElementById: () => null };
global.localStorage = { getItem: () => null, setItem: () => {} };
Object.defineProperty(global, 'navigator', {
  value: {
    modelContext: {
      registerTool: (def) => registeredWebMcp.push(def && def.name)
    }
  },
  configurable: true
});
eval(fs.readFileSync(process.argv[1], 'utf8'));
window.RealTransit.networkData = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
window.RealTransit.schedulesData = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
window.RealTransit.modelTrainingStatus = JSON.parse(fs.readFileSync(process.argv[4], 'utf8'));

// Evita dependencia do Leaflet DOM ao validar adaptToUserLocation em Node
window.RealTransit.loadRoute = () => {};
window.RealTransit.selectStop = () => {};

const tripCamelaIpojuca = window.RealTransit.answerLayaQuery('Gostaria de sair de Camela até Ipojuca. Vamos lá?');
const tripRecifeOlinda = window.RealTransit.answerLayaQuery('Quero ir do Recife Antigo pra Olinda');
const tripCamelaOlinda = window.RealTransit.answerLayaQuery('Quero ir de Camela até Olinda');
const nextCamela = window.RealTransit.answerLayaQuery('Qual o horário do próximo ônibus de Camela');
const nextLine199 = window.RealTransit.answerLayaQuery('Qual o horário da linha 199?');
const aiKnow = window.RealTransit.answerLayaQuery('Como funciona a IA ST-GCN?');

const adaptRecife = window.RealTransit.adaptToUserLocation(-8.0631, -34.8711, 'Recife Antigo');
const tripImplicitFromRecife = window.RealTransit.answerLayaQuery('Quero ir para Casa Caiada');
const planIburaShopping = window.RealTransit.planSmartTrip('Ibura', 'Shopping Recife');
const adaptCamela = window.RealTransit.adaptToUserLocation(-8.5149, -35.1235, 'Camela');
const adaptSp = window.RealTransit.adaptToUserLocation(-23.5505, -46.6333, 'SP');
window.RealTransit.adaptToUserLocation(-8.0631, -34.8711, 'Recife Antigo');
const lostDecision = window.RealTransit.classifyLayaDecision('Estou perdido, quero chegar na Madalena');
const lostRes = window.RealTransit.answerLayaQuery('Estou perdido, quero chegar na Madalena');
const dirIdaTest = window.RealTransit.pickBestDirection(
  window.RealTransit.networkData.popular_lines['199'],
  [-8.514931, -35.123469],
  [-8.285065, -35.032398]
);
const dirVoltaTest = window.RealTransit.pickBestDirection(
  window.RealTransit.networkData.popular_lines['199'],
  [-8.285065, -35.032398],
  [-8.514931, -35.123469]
);
const arbitraryNeighborhood = window.RealTransit.RoutePlanner.plan('Torrões', 'Santo Amaro');
window.RealTransit.registerWebMCPTools();

console.log(JSON.stringify({
  tripCamelaIpojuca,
  tripRecifeOlinda,
  tripCamelaOlinda,
  nextCamela,
  nextLine199,
  aiKnow,
  tripImplicitFromRecife,
  planIburaShopping,
  adaptRecife,
  adaptCamela,
  adaptSp,
  lostDecision,
  lostRes,
  dirIdaTest,
  dirVoltaTest,
  arbitraryNeighborhood,
  registeredWebMcp
}));
"""
    res = subprocess.run(
        [
            "node",
            "-e",
            node_eval,
            str(ENGINE_JS),
            str(GTFS_JSON),
            str(GTFS_SCHEDULES_JSON),
            str(MODEL_STATUS_JSON),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    assert res.returncode == 0, f"Erro Node.js executando Laya IA: {res.stderr}"
    json_line = [ln for ln in res.stdout.strip().splitlines() if ln.strip().startswith("{")][-1]
    return json.loads(json_line)


# ------------------------------------------------------------------------------
# TESTES PYTEST COMPATÍVEIS & SUITE AUDITADA PELO PRE-FLIGHT CHECK
# ------------------------------------------------------------------------------

def test_interface_zero_hardcoded_e_fluxo_guiado():
    html = _load_html()
    for bad in FORBIDDEN_HARDCODED_TOKENS:
        assert bad not in html, f"Token hardcoded legado ainda presente em index.html: {bad!r}"

    for label, fragment in REQUIRED_GUIDED_UI_TOKENS:
        assert fragment in html, f"{label} ausente em index.html: {fragment!r}"

    assert "Terminal de Dois Irmãos (UFRPE / Rui Barbosa)" not in html
    assert "CÓD 100035" not in html
    assert 'id="top-line-label">522<' not in html

    assert ROTEIRO_PATH.is_file(), f"roteiro.html ausente: {ROTEIRO_PATH}"
    roteiro = ROTEIRO_PATH.read_text(encoding="utf-8")
    for token in ("Neon Postgres", "stop_times.txt", "14,3 min", "0,96 ms", "324,7 MB", "56,68 µs", "393"):
        assert token in roteiro, f"Token esperado ausente em roteiro.html: {token!r}"


def test_deck_oficial_banca():
    deck = DECK_PATH if DECK_PATH.is_file() else (ROOT / "va2" / "GrafoParada_Seminario2_CauaLira.pptx")
    assert deck.is_file() and deck.stat().st_size >= 1_000_000, f"Deck Oficial ausente ou corrompido: {deck}"


def test_modelos_cientificos_yap_kim_trava_ctm():
    t_regular = calcular_tempo_percebido(10.0, denied_boarding=False)
    t_denied = calcular_tempo_percebido(10.0, denied_boarding=True)
    assert t_regular == 10.0 and abs(t_denied - 16.8) < 1e-4

    t_crowded = calcular_tempo_percebido(15.0, crowd_critical=True)
    assert abs(t_crowded - 25.2) < 1e-4

    p_tau = calcular_probabilidade_reneging(15.0, tau=15.0)
    assert abs(p_tau - 0.50) < 1e-3

    p_prolongado = calcular_probabilidade_reneging(
        15.0, usar_tempo_percebido=True, denied_boarding=True, tau=15.0
    )
    assert p_prolongado > 0.90

    r_nom = avaliar_trava_hibrida_defensiva(tempo_gps_min=10.0, tempo_stgcn_min=12.0)
    assert not r_nom["trava_acionada"] and r_nom["status"] == "NOMINAL_STGCN"

    r_bloq = avaliar_trava_hibrida_defensiva(tempo_gps_min=45.0, tempo_stgcn_min=17.0)
    assert (
        r_bloq["trava_acionada"]
        and r_bloq["status"] == "ALERTA_AMARELO_OVER_SMOOTHING"
        and r_bloq["tempo_exibido_min"] == 45.0
    )

    despacho = avaliar_gatilho_despacho_emergencial(
        tempo_espera_min=16.0,
        ocupacao_concorrente_pct=10.0,
        denied_boarding=True,
    )
    assert despacho["despacho_autorizado"] and despacho["probabilidade_reneging_pct"] >= 80.0


def test_db_manager_sqlite_temporario_e_gtfs_schedules():
    with tempfile.TemporaryDirectory(prefix="gp_db_test_") as tmp_dir:
        tmp_db = Path(tmp_dir) / "test_grafoparada.db"
        resolved = init_db(tmp_db)
        assert resolved == tmp_db and tmp_db.is_file()

        user = register_user(
            name="Maria Silva",
            contact_hint="maria@recife.pe",
            db_path=tmp_db,
        )
        assert user["id"].startswith("usr_")
        assert user["name"] == "Maria Silva"
        assert user["contact_hint"] == "maria@recife.pe"

        routine = save_routine(
            {
                "user_id": user["id"],
                "origin_city": "Ipojuca",
                "origin_neighborhood": "Camela",
                "origin_stop_id": "030613",
                "origin_stop_name": "Parada 030613",
                "origin_lat": -8.514931,
                "origin_lon": -35.123469,
                "dest_city": "Cabo de Santo Agostinho",
                "dest_neighborhood": "Cabo",
                "dest_stop_id": "030901",
                "dest_stop_name": "Ti Cabo - Embarque 01 - 030901",
                "dest_lat": -8.2851,
                "dest_lon": -35.0321,
                "departure_time": "06:15",
                "return_time": "18:10",
                "preferred_line": "199",
                "frequency": "Seg a Sex",
            },
            db_path=tmp_db,
        )
        assert routine["user_id"] == user["id"]
        assert routine["preferred_line"] == "199"
        assert routine["origin_city"] == "Ipojuca"
        assert routine["dest_city"] == "Cabo de Santo Agostinho"

        obs = record_observation(
            {
                "user_id": user["id"],
                "stop_id": "030613",
                "route_code": "199",
                "direction": "ida",
                "observed_wait_min": 11.4,
                "predicted_wait_min": 10.2,
                "occupancy_est": 28,
                "source": "teste_rotinas_unitario",
            },
            db_path=tmp_db,
        )
        assert obs["route_code"] == "199"
        assert obs["observed_wait_min"] == 11.4

        dataset = get_training_dataset(db_path=tmp_db)
        assert dataset["total_observations"] == 1
        assert dataset["total_routines"] == 1
        assert "199" in dataset["lines_covered"]

    sched = json.loads(GTFS_SCHEDULES_JSON.read_text(encoding="utf-8"))
    lines = sched.get("lines") or {}
    rmr_places = sched.get("rmr_places") or []
    cities = {str(p.get("city")).strip() for p in rmr_places if isinstance(p, dict) and p.get("city")}
    assert sched.get("total_lines") == 393
    assert len(lines) == 393
    assert len(rmr_places) == 236
    assert len(cities) == 14

    status = json.loads(MODEL_STATUS_JSON.read_text(encoding="utf-8"))
    assert status.get("validation_393_passed") is True
    assert status.get("lines_covered") == 393


def test_gtfs_schedules_ti_hubs_checkpoints_e_chegadas():
    sched = json.loads(GTFS_SCHEDULES_JSON.read_text(encoding="utf-8"))
    ti_hubs = sched.get("ti_hubs") or []
    assert isinstance(ti_hubs, list) and len(ti_hubs) == 133, (
        f"Esperado 133 ti_hubs em gtfs_schedules.json, obtido {len(ti_hubs)}"
    )
    for hub in ti_hubs:
        hub_lines = hub.get("lines") or []
        distinct_codes = {str(item.get("code") or "").strip() for item in hub_lines if item.get("code")}
        assert len(distinct_codes) >= 2, f"Hub {hub.get('name')} não é multi-linha: {distinct_codes}"

    lines = sched.get("lines") or {}
    assert len(lines) == 393
    dirs_with_checkpoints = 0
    non_empty_ti_checkpoints = 0
    for code, line_obj in lines.items():
        has_any_dir = False
        for dir_key in ("ida", "volta"):
            dir_obj = line_obj.get(dir_key)
            if not isinstance(dir_obj, dict):
                continue
            has_any_dir = True
            if "ti_checkpoints" in dir_obj:
                cps = dir_obj.get("ti_checkpoints")
                assert isinstance(cps, list), f"Linha {code} ({dir_key}) sem lista ti_checkpoints"
                dirs_with_checkpoints += 1
                if cps:
                    non_empty_ti_checkpoints += 1
                    assert any(cp.get("stop_id") and cp.get("stop_name") for cp in cps), (
                        f"Linha {code} ({dir_key}) com ti_checkpoints malformados"
                    )
            for day_key in ("DUT", "SAB", "DOM"):
                day_obj = dir_obj.get(day_key)
                if isinstance(day_obj, dict) and day_obj.get("dep_mins"):
                    assert day_obj.get("first_arr"), f"Linha {code} ({dir_key}/{day_key}) sem first_arr"
                    assert day_obj.get("last_arr"), f"Linha {code} ({dir_key}/{day_key}) sem last_arr"
        assert has_any_dir, f"Linha {code} sem direções ida/volta"

    assert dirs_with_checkpoints >= 393
    assert non_empty_ti_checkpoints >= 100

    status = json.loads(MODEL_STATUS_JSON.read_text(encoding="utf-8"))
    assert int(status.get("ti_hubs_indexed") or 0) == 133
    assert status.get("gtfs_schedule_prior_enabled") is True


def test_db_manager_sync_cloud_observations_offline_e_http_mock():
    with tempfile.TemporaryDirectory(prefix="gp_db_sync_") as tmp_dir:
        tmp_db = Path(tmp_dir) / "sync_test.db"
        init_db(tmp_db)

        prev_env = os.environ.pop("GRAFOPARADA_API_BASE", None)
        try:
            offline_res = sync_cloud_observations(api_base=None, db_path=tmp_db)
            assert offline_res["synced"] is False
            assert offline_res["reason"] == "no_api_base_or_offline"
            assert offline_res["observations_added"] == 0
            assert offline_res["routines_added"] == 0
        finally:
            if prev_env is not None:
                os.environ["GRAFOPARADA_API_BASE"] = prev_env

        class MockCloudHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

            def do_GET(self):
                path = self.path.split("?")[0]
                if path == "/api/telemetry":
                    payload = {
                        "ok": True,
                        "available": True,
                        "storage": "neon_postgres",
                        "recent_observations": [
                            {
                                "user_id": "usr_cloud_01",
                                "stop_id": "030207",
                                "route_code": "195",
                                "direction": "ida",
                                "observed_wait_min": 9.5,
                                "predicted_wait_min": 10.0,
                                "occupancy_est": 15,
                                "source": "passenger_checkin",
                                "created_at": "2026-11-16T08:00:00Z",
                            }
                        ],
                    }
                    code = 200
                elif path == "/api/routine":
                    payload = {
                        "ok": True,
                        "available": True,
                        "storage": "neon_postgres",
                        "routines": [
                            {
                                "id": "rtn_cloud_01",
                                "user_id": "usr_cloud_01",
                                "origin_city": "Ipojuca",
                                "origin_neighborhood": "Nossa Senhora do Ó",
                                "origin_stop_id": "030207",
                                "origin_stop_name": "Parada 030207",
                                "origin_lat": -8.399694,
                                "origin_lon": -35.062944,
                                "dest_city": "Recife",
                                "dest_neighborhood": "São José",
                                "dest_stop_id": "180001",
                                "dest_stop_name": "Cais de Santa Rita",
                                "dest_lat": -8.067,
                                "dest_lon": -34.878,
                                "departure_time": "06:30",
                                "return_time": "17:45",
                                "preferred_line": "195",
                                "frequency": "Seg a Sex",
                                "created_at": "2026-11-16T07:55:00Z",
                            }
                        ],
                    }
                    code = 200
                else:
                    payload = {"ok": False}
                    code = 404

                raw = json.dumps(payload).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

        server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), MockCloudHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            res1 = sync_cloud_observations(api_base=f"http://127.0.0.1:{port}", db_path=tmp_db)
            assert res1["synced"] is True
            assert res1["reason"] == "ok"
            assert res1["observations_added"] == 1
            assert res1["routines_added"] == 1

            dataset = get_training_dataset(db_path=tmp_db)
            assert dataset["total_observations"] == 1
            assert dataset["total_routines"] == 1
            assert "195" in dataset["lines_covered"]
            assert dataset["routines"][0]["id"] == "rtn_cloud_01"
            assert dataset["observations"][0]["source"] == "passenger_checkin"

            res2 = sync_cloud_observations(api_base=f"http://127.0.0.1:{port}", db_path=tmp_db)
            assert res2["synced"] is True
            assert res2["observations_added"] == 0
            assert res2["routines_added"] == 0
        finally:
            server.shutdown()
            server.server_close()


def test_laya_ia_gtfs_gps_e_webmcp():
    out = _run_laya_node_suite()
    t1 = out["tripCamelaIpojuca"]
    t_rec_ol = out["tripRecifeOlinda"]
    t_cam_ol = out["tripCamelaOlinda"]
    t2 = out["nextCamela"]
    t2_199 = out["nextLine199"]
    t3 = out["aiKnow"]
    t_imp = out.get("tripImplicitFromRecife") or {}
    p_ibu = out.get("planIburaShopping") or {}

    assert (t1.get("routeCode") == "199") and ("199" in t1.get("html", "")) and ("Ipojuca" in t1.get("html", "")) and ("522" not in t1.get("html", ""))
    assert (t_rec_ol.get("routeCode") in ["1967", "1971", "1983", "1100", "1992", "1973", "1913", "914"]) and ("Olinda" in t_rec_ol.get("html", "")) and ("522" not in t_rec_ol.get("html", ""))

    cam_ol_legs = t_cam_ol.get("legs") or []
    cam_ol_hubs = t_cam_ol.get("hubs") or []
    cam_ol_opts = t_cam_ol.get("routeOptions") or []
    assert (t_cam_ol.get("intent") == "trip_transfer") and (len(cam_ol_legs) >= 3) and (cam_ol_legs[0] == "199")
    assert any("Cabo" in h for h in cam_ol_hubs) and (len(cam_ol_opts) >= 1) and ("522" not in t_cam_ol.get("html", ""))

    assert t2.get("provenanceLabel") == "Horário Programado · GTFS" and t2.get("routeCode") in ("199", "178", "191", "195", "196") and ("522" not in t2.get("html", ""))
    assert t2_199.get("routeCode") == "199" and t2_199.get("provenanceLabel") == "Horário Programado · GTFS" and ("522" not in t2_199.get("html", ""))
    ai_html = t3.get("html", "")
    status = json.loads(MODEL_STATUS_JSON.read_text(encoding="utf-8"))
    expected_mae_br = str(status["stgcn_mae"]).replace(".", ",") + " min"
    assert (expected_mae_br in ai_html) and ("393" in ai_html) and ("Kim et al." in ai_html)
    assert (t_imp.get("intent") in ("trip_plan", "trip_direct", "trip_transfer")) and (len(t_imp.get("routeOptions") or []) >= 1) and ("Casa Caiada" in t_imp.get("html", ""))
    assert bool(p_ibu.get("origCorridor")) and bool(p_ibu.get("destCorridor")) and (len(p_ibu.get("routeOptions") or []) >= 1)

    a_rec = out.get("adaptRecife") or {}
    a_cam = out.get("adaptCamela") or {}
    a_sp = out.get("adaptSp") or {}
    wmcp = out.get("registeredWebMcp") or []
    assert (not a_rec.get("outOfCoverage")) and a_rec.get("best", {}).get("code") not in (None, "522") and a_rec.get("best", {}).get("distanceKm", 99) < 1.5
    assert (not a_cam.get("outOfCoverage")) and a_cam.get("best", {}).get("code") == "199"
    assert bool(a_sp.get("outOfCoverage"))
    assert ("grafoparada_plan_route" in wmcp) and ("grafoparada_find_nearest_stop" in wmcp)

    lost_dec = out.get("lostDecision") or {}
    lost_res = out.get("lostRes") or {}
    dir_ida = out.get("dirIdaTest") or {}
    dir_volta = out.get("dirVoltaTest") or {}
    arb_plan = out.get("arbitraryNeighborhood") or {}
    assert (lost_dec.get("laya_role") == "semantic_intent_and_lost_guide") and (lost_res.get("intent") in ("trip_plan", "trip_transfer")) and (len(lost_res.get("routeOptions") or []) >= 1)
    assert (dir_ida.get("dir") in ("ida", "volta")) and (dir_volta.get("dir") in ("ida", "volta")) and (dir_ida.get("dir") != dir_volta.get("dir"))
    assert bool(arb_plan.get("origCorridor")) and bool(arb_plan.get("destCorridor")) and (len(arb_plan.get("routeOptions") or []) >= 1)


def run_cli_audit() -> int:
    html = _load_html()
    print("=" * 70)
    print("[*] AUDITORIA DA SUÍTE GRAFOPARADA · TECNOLOGIA & CIÊNCIA (v3)")
    print(f"[*] Artefato Web: {HTML_PATH.name} ({len(html):,} caracteres / {HTML_PATH.stat().st_size:,} bytes)")
    print("=" * 70)

    checks = [
        ("Bloco 1: Zero Hardcoding & Fluxo Guiado Cascata RMR", test_interface_zero_hardcoded_e_fluxo_guiado),
        ("Bloco 2: Deck Oficial da Banca (.pptx >= 1 MB)", test_deck_oficial_banca),
        ("Bloco 3/4: Modelos Yap & Cats, Kim et al., Trava Híbrida e Despacho CTM", test_modelos_cientificos_yap_kim_trava_ctm),
        ("Bloco 5: Persistência SQLite Temporária & Horários GTFS (393/14/236)", test_db_manager_sqlite_temporario_e_gtfs_schedules),
        ("Bloco 5b: GTFS TIs Multi-Linha (133), Checkpoints & Chegadas", test_gtfs_schedules_ti_hubs_checkpoints_e_chegadas),
        ("Bloco 6: Sincronização Cloud/Neon -> SQLite (Offline + Mock HTTP)", test_db_manager_sync_cloud_observations_offline_e_http_mock),
        ("Bloco 7: Laya IA GTFS, Adaptação GPS, Ida/Volta & WebMCP", test_laya_ia_gtfs_gps_e_webmcp),
    ]

    aprovados = 0
    for label, fn in checks:
        try:
            fn()
            print(f"  [PASS] {label}")
            aprovados += 1
        except Exception as exc:
            print(f"  [FAIL] {label} -> {exc}")

    total_testes = len(checks)
    taxa = (aprovados / total_testes) * 100.0
    print("\n" + "=" * 70)
    print(f"[RESULTADO DA AUDITORIA] {aprovados}/{total_testes} blocos aprovados ({taxa:.1f}% de conformidade).")
    print("=" * 70)

    if aprovados == total_testes:
        print("[STATUS] 100% APROVADO! Todos os critérios v3 (zero hardcoding, GTFS 393 linhas, SQLite e ciência A1) validados.")
        return 0
    print("[STATUS] FALHA: Alguns requisitos não foram atendidos.")
    return 1


if __name__ == "__main__":
    sys.exit(run_cli_audit())
