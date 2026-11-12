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
