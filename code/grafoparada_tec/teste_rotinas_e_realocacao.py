# -*- coding: utf-8 -*-
"""
Bateria de Testes Automatizados · Conformidade Operacional, Científica e Usabilidade
Projeto GrafoParada · Tópicos Avançados em Inteligência Artificial (AI4Good / UFRPE)
Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)

Validações cobertas:
1. Usabilidade Universal, Rotinas Pendulares e Modais de Interface
2. Integridade Física da Apresentação Oficial da Banca (GrafoParada_Seminario2_CauaLira.pptx)
3. Cômputo da Penalidade de Percepção de Tempo (1,68x · Yap & Cats, 2021)
4. Modelo Logístico de Abandono de Passageiros (Passenger Reneging · Kim et al., 2026)
5. Mecanismo de Trava Híbrida Defensiva Anti-Oversmoothing (Δ > 15 min)
6. Gatilho de Despacho Operacional CTM & Mitigação de Deadheading
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "code" / "grafoparada_tec"))

from modelo_predicao_e_abandono import (
    PENALIDADE_DENIED_BOARDING_YAP_CATS,
    calcular_tempo_percebido,
    calcular_probabilidade_reneging,
    avaliar_trava_hibrida_defensiva,
    avaliar_gatilho_despacho_emergencial,
)

# ------------------------------------------------------------------------------
# PARTE 1: AUDITORIA DO ARTEFATO DE INTERFACE (HTML)
# ------------------------------------------------------------------------------
html_path = ROOT / "code" / "grafoparada_web" / "index.html"
if not html_path.exists():
    html_path = ROOT / "code" / "grafoparada_tec" / "prototipo_grafoparada.html"

assert html_path.exists(), f"Arquivo não encontrado: {html_path}"
html = html_path.read_text(encoding="utf-8")

print("=" * 70)
print(f"[*] AUDITORIA DA SUÍTE GRAFOPARADA · TECNOLOGIA & CIÊNCIA")
print(f"[*] Artefato Web: {html_path.name} ({len(html):,} caracteres / {html_path.stat().st_size:,} bytes)")
print("=" * 70)

testes_html = [
    ("Mapeador de Rotina Pendular (Card Inicial)", "routine-commute-card"),
    ("Pill de Rotina Superior (05h45)", "label-routine-pill"),
    ("Modal de Rotinas com 4 Turnos", "modal-routine"),
    ("Turno 1: Indústria Suape (05h45)", "Turno Indústria Suape"),
    ("Turno 2: Comércio Centro (07h30)", "Turno Comércio / Centro"),
    ("Turno 3: Estudante Universitário (17h40)", "Estudante Universitário / Noite"),
    ("Turno 4: Plantão Saúde 12x36 (06h30)", "Turno Plantão Saúde (12x36)"),
    ("Cálculo da Janela Segura de Saída", "Janela de Saída"),
    ("Alimentação de Demanda na Central CTM", "48 trabalhadores"),
    ("Letreiro de LED Idêntico ao Coletivo (199)", "bus-led-sign-box"),
    ("Destaque LED Âmbar Linha 199", "CAMELA / TI CABO VIA PE-60"),
    ("Botão Gigante de Leitura em Voz Alta Sênior", "btn-senior-voice-big"),
    ("Modo Bolso Seguro Anti-Assalto (0 Nits)", "pocket-shield-screen"),
    ("Modo Offline Inercial na PE-60 (Dead Reckoning)", "offline-inertial-banner"),
    ("Mitigação de Deadheading na Frota 178", "14 L de diesel"),
    ("Alerta de Alagamento PE-60 Km 14 (Desvio UPA)", "flood-alert-banner"),
    ("Lei Estadual 15.878/2016 (Parada Segura)", "modal-safe-disembark"),
    ("Farol Noturno de Embarque (Anti-Queima)", "night-beacon-screen"),
    ("Sensor Forense de Queima de Parada", "modal-queima-parada"),
    ("Guardião da Integração Temporal VEM (120 min)", "modal-vem")
]

aprovados = 0
total_testes = 0

print("\n--- [BLOCO 1/4] Usabilidade Universal e Componentes da Interface ---")
for nome, fragmento in testes_html:
    total_testes += 1
    if fragmento in html:
        print(f"  [PASS] {nome}")
        aprovados += 1
    else:
        print(f"  [FAIL] {nome} - Fragmento ausente: '{fragmento}'")

# ------------------------------------------------------------------------------
# PARTE 2: AUDITORIA DO ARTEFATO OFICIAL DE BANCA (PPTX)
# ------------------------------------------------------------------------------
print("\n--- [BLOCO 2/4] Integridade Física do Deck Oficial da Banca (.pptx) ---")
deck_path = ROOT / "code" / "grafoparada_web" / "GrafoParada_Seminario2_CauaLira.pptx"
if not deck_path.exists():
    deck_path = ROOT / "va2" / "GrafoParada_Seminario2_CauaLira.pptx"

total_testes += 1
if deck_path.exists() and deck_path.stat().st_size >= 1_000_000:
    tamanho_mb = deck_path.stat().st_size / (1024 * 1024)
    print(f"  [PASS] Deck Oficial da Banca Preservado: {deck_path.name} ({tamanho_mb:.2f} MB)")
    aprovados += 1
else:
    print(f"  [FAIL] Deck Oficial Ausente ou Corrompido: {deck_path}")

# ------------------------------------------------------------------------------
# PARTE 3: RIGOR CIENTÍFICO QUALIS A1 (YAP & CATS 2021 + KIM ET AL. 2026)
# ------------------------------------------------------------------------------
print("\n--- [BLOCO 3/4] Validação Científica dos Modelos Comportamentais ---")

# Teste 3.1: Penalidade Yap & Cats (2021) 1.68x
total_testes += 1
t_regular = calcular_tempo_percebido(10.0, denied_boarding=False)
t_denied = calcular_tempo_percebido(10.0, denied_boarding=True)
if t_regular == 10.0 and abs(t_denied - 16.8) < 1e-4:
    print(f"  [PASS] Penalidade Yap & Cats (2021): Regular={t_regular}m | Denied Boarding (1.68x)={t_denied}m")
    aprovados += 1
else:
    print(f"  [FAIL] Inconsistência na penalidade Yap & Cats: reg={t_regular}, denied={t_denied}")

# Teste 3.2: Dilatação com Superlotação Crítica (15 min -> 25.2 min)
total_testes += 1
t_crowded = calcular_tempo_percebido(15.0, crowd_critical=True)
if abs(t_crowded - 25.2) < 1e-4:
    print(f"  [PASS] Percepção sob Superlotação Crítica: 15.0m -> {t_crowded}m (+68%)")
    aprovados += 1
else:
    print(f"  [FAIL] Inconsistência no cálculo de superlotação: obtido={t_crowded}")

# Teste 3.3: Modelo Logístico de Reneging de Kim et al. (2026) na Mediana
total_testes += 1
p_tau = calcular_probabilidade_reneging(15.0, tau=15.0)
if abs(p_tau - 0.50) < 1e-3:
    print(f"  [PASS] Kim et al. (2026) no limiar mediano tau=15m: P(Reneging) = {p_tau*100:.1f}%")
    aprovados += 1
else:
    print(f"  [FAIL] Inconsistência no limiar mediano de Kim et al.: obtido={p_tau}")

# Teste 3.4: Risco Crítico de Reneging sob Espera Prolongada com Yap & Cats
total_testes += 1
p_prolongado = calcular_probabilidade_reneging(15.0, usar_tempo_percebido=True, denied_boarding=True, tau=15.0)
if p_prolongado > 0.90:
    print(f"  [PASS] Risco de Reneging sob Denied Boarding: P(Reneging | 1.68x) = {p_prolongado*100:.1f}% (>90%)")
    aprovados += 1
else:
    print(f"  [FAIL] Probabilidade de abandono subestimada: obtido={p_prolongado}")

# ------------------------------------------------------------------------------
# PARTE 4: TRAVA HÍBRIDA DEFENSIVA & DESPACHO OPERACIONAL CTM
# ------------------------------------------------------------------------------
print("\n--- [BLOCO 4/4] Blindagem Operacional & Trava Anti-Oversmoothing ---")

# Teste 4.1: Trava Híbrida Não Acionada em Condição Nominal (Delta <= 15 min)
total_testes += 1
r_nom = avaliar_trava_hibrida_defensiva(tempo_gps_min=10.0, tempo_stgcn_min=12.0)
if not r_nom["trava_acionada"] and r_nom["status"] == "NOMINAL_STGCN":
    print(f"  [PASS] Trava Híbrida Nominal (Δ={r_nom['discrepancy_delta']}m <= 15m): status={r_nom['status']}")
    aprovados += 1
else:
    print(f"  [FAIL] Falso positivo na Trava Híbrida Nominal: {r_nom}")

# Teste 4.2: Trava Híbrida Acionada sob Over-Smoothing Brusco (Delta > 15 min)
total_testes += 1
r_bloq = avaliar_trava_hibrida_defensiva(tempo_gps_min=45.0, tempo_stgcn_min=17.0)
if r_bloq["trava_acionada"] and r_bloq["status"] == "ALERTA_AMARELO_OVER_SMOOTHING" and r_bloq["tempo_exibido_min"] == 45.0:
    print(f"  [PASS] Trava Híbrida Anti-Oversmoothing (Δ={r_bloq['discrepancy_delta']}m > 15m): Forçou fallback GPS={r_bloq['tempo_exibido_min']}m")
    aprovados += 1
else:
    print(f"  [FAIL] Falha no acionamento da Trava Híbrida sob bloqueio: {r_bloq}")

# Teste 4.3: Decisão de Despacho Operacional Preventivo CTM
total_testes += 1
despacho = avaliar_gatilho_despacho_emergencial(
    tempo_espera_min=16.0,
    ocupacao_concorrente_pct=10.0,
    denied_boarding=True
)
if despacho["despacho_autorizado"] and despacho["probabilidade_reneging_pct"] >= 80.0:
    print(f"  [PASS] Despacho Operacional CTM Aprovado: P(Reneging)={despacho['probabilidade_reneging_pct']}% >= 80% & Ociosidade={despacho['ocupacao_concorrente_pct']}% <= 15%")
    aprovados += 1
else:
    print(f"  [FAIL] Falha na autorização de despacho operacional CTM: {despacho}")

# ------------------------------------------------------------------------------
# PARTE 5: FLUXO DE TELAS PROGRESSIVO & INTELIGÊNCIA GTFS DA LAYA IA
# ------------------------------------------------------------------------------
print("\n--- [BLOCO 5/5] Fluxo de Telas Progressivo & Inteligência Laya IA (GTFS) ---")

ui_flow_checks = [
    ("Tela 1 Início Contextual ('Está indo trabalhar...')", "app-screen-home"),
    ("Pergunta Contextual Direta", "Está indo trabalhar ou estudar hoje?"),
    ("Tela 2 Localização Guiada ('Onde você está agora?')", "app-screen-locate"),
    ("Tela 5 Central CTM & Pesquisa", "app-screen-central"),
    ("Controlador de Transição Suave (navigateToScreen)", "function navigateToScreen("),
    ("WebMCP Declarativo na Busca de Rotas", 'toolname="grafoparada_plan_from_locate"'),
]
for nome, fragmento in ui_flow_checks:
    total_testes += 1
    if fragmento in html:
        print(f"  [PASS] {nome}")
        aprovados += 1
    else:
        print(f"  [FAIL] {nome} - Fragmento ausente: '{fragmento}'")

total_testes += 1
if ("Terminal de Dois Irmãos (UFRPE / Rui Barbosa)" not in html) and ("CÓD 100035" not in html):
    print("  [PASS] Zero Hardcoding Rural: HTML inicial neutro e 100% adaptativo ao GPS")
    aprovados += 1
else:
    print("  [FAIL] HTML inicial ainda contém parada fixa na UFRPE/Dois Irmãos")

import json
import subprocess

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

// Evita dependencia do Leaflet DOM ao validar adaptToUserLocation em Node
window.RealTransit.loadRoute = () => {};
window.RealTransit.selectStop = () => {};

const tripCamelaIpojuca = window.RealTransit.answerLayaQuery('Gostaria de sair de Camela até Ipojuca. Vamos lá?');
const tripRecifeOlinda = window.RealTransit.answerLayaQuery('Quero ir do Recife Antigo pra Olinda');
const tripCamelaOlinda = window.RealTransit.answerLayaQuery('Quero ir de Camela até Olinda');
const nextCamela = window.RealTransit.answerLayaQuery('Qual o horário do próximo ônibus de Camela');
const aiKnow = window.RealTransit.answerLayaQuery('Como funciona a IA ST-GCN?');

const adaptRecife = window.RealTransit.adaptToUserLocation(-8.0631, -34.8711, 'Recife Antigo');
const adaptCamela = window.RealTransit.adaptToUserLocation(-8.5149, -35.1235, 'Camela');
const adaptSp = window.RealTransit.adaptToUserLocation(-23.5505, -46.6333, 'SP');
window.RealTransit.registerWebMCPTools();

console.log(JSON.stringify({
  tripCamelaIpojuca,
  tripRecifeOlinda,
  tripCamelaOlinda,
  nextCamela,
  aiKnow,
  adaptRecife,
  adaptCamela,
  adaptSp,
  registeredWebMcp
}));
"""
engine_js = ROOT / "code" / "grafoparada_web" / "real_transit_engine.js"
gtfs_json = ROOT / "code" / "grafoparada_web" / "data" / "gtfs_real_network.json"
node_res = subprocess.run(["node", "-e", node_eval, str(engine_js), str(gtfs_json)], capture_output=True, text=True, encoding="utf-8")

total_testes += 1
if node_res.returncode == 0:
    json_line = [ln for ln in node_res.stdout.strip().splitlines() if ln.strip().startswith("{")][-1]
    out = json.loads(json_line)
    t1 = out["tripCamelaIpojuca"]
    t_rec_ol = out["tripRecifeOlinda"]
    t_cam_ol = out["tripCamelaOlinda"]
    t2 = out["nextCamela"]
    t3 = out["aiKnow"]
    ok_trip = (t1.get("routeCode") == "199") and ("199" in t1.get("html", "")) and ("Ipojuca" in t1.get("html", "")) and ("522" not in t1.get("html", ""))
    ok_rec_ol = (t_rec_ol.get("routeCode") in ["1967", "1971", "1983", "1100", "1992", "1973", "1913", "914"]) and ("Olinda" in t_rec_ol.get("html", "")) and ("522" not in t_rec_ol.get("html", ""))
    cam_ol_legs = t_cam_ol.get("legs") or []
    cam_ol_hubs = t_cam_ol.get("hubs") or []
    ok_cam_ol = (t_cam_ol.get("intent") == "trip_transfer") and (len(cam_ol_legs) == 3) and (cam_ol_legs[0] == "199") and any("Cabo" in h for h in cam_ol_hubs) and any("Cais" in h or "Recife" in h for h in cam_ol_hubs) and ("522" not in t_cam_ol.get("html", ""))
    ok_next = (t2.get("routeCode") == "199") and ("Camela" in t2.get("html", "")) and ("522" not in t2.get("html", ""))
    ok_ai = ("1,51 min" in t3.get("html", "")) and ("Kim et al." in t3.get("html", ""))
    if ok_trip and ok_rec_ol and ok_cam_ol and ok_next and ok_ai:
        print(f"  [PASS] Laya IA GTFS + Hub Graph Multi-Etapas: Camela->Ipojuca (199), Recife Antigo->Olinda ({t_rec_ol.get('routeCode')}), Camela->Olinda ({' -> '.join(cam_ol_legs)} via {' -> '.join(cam_ol_hubs)}) OK")
        aprovados += 1
    else:
        print(f"  [FAIL] Laya IA GTFS invalid: cam_ipo={ok_trip}, rec_ol={ok_rec_ol} ({t_rec_ol.get('routeCode')}), cam_ol={ok_cam_ol} ({t_cam_ol.get('intent')}), next={ok_next}, ai={ok_ai}")
else:
    print(f"  [FAIL] Erro Node.js executando Laya IA: {node_res.stderr}")

total_testes += 1
if node_res.returncode == 0:
    a_rec = out.get("adaptRecife") or {}
    a_cam = out.get("adaptCamela") or {}
    a_sp = out.get("adaptSp") or {}
    wmcp = out.get("registeredWebMcp") or []
    ok_rec_gps = (not a_rec.get("outOfCoverage")) and a_rec.get("best", {}).get("code") not in (None, "522") and a_rec.get("best", {}).get("distanceKm", 99) < 1.5
    ok_cam_gps = (not a_cam.get("outOfCoverage")) and a_cam.get("best", {}).get("code") == "199"
    ok_sp_gps = bool(a_sp.get("outOfCoverage"))
    ok_wmcp = ("grafoparada_plan_route" in wmcp) and ("grafoparada_find_nearest_stop" in wmcp)
    if ok_rec_gps and ok_cam_gps and ok_sp_gps and ok_wmcp:
        print(f"  [PASS] Adaptação GPS Dinâmica + WebMCP: Recife Antigo->{a_rec['best']['code']}, Camela->199, SP->Fora RMR, WebMCP={wmcp}")
        aprovados += 1
    else:
        print(f"  [FAIL] Adaptação GPS/WebMCP inválida: rec={ok_rec_gps} ({a_rec.get('best')}), cam={ok_cam_gps} ({a_cam.get('best')}), sp={ok_sp_gps}, wmcp={wmcp}")
else:
    print("  [FAIL] Adaptação GPS/WebMCP não executada por erro Node.js")

# ------------------------------------------------------------------------------
# RESUMO FINAL
# ------------------------------------------------------------------------------
taxa = (aprovados / total_testes) * 100.0
print("\n" + "=" * 70)
print(f"[RESULTADO DA AUDITORIA] {aprovados}/{total_testes} testes aprovados ({taxa:.1f}% de conformidade).")
print("=" * 70)

if aprovados == total_testes:
    print("[STATUS] 100% APROVADO! Todos os critérios de usabilidade, artefato de banca e rigor científico A1 validados com sucesso.")
    sys.exit(0)
else:
    print("[STATUS] FALHA: Alguns requisitos não foram atendidos.")
    sys.exit(1)
