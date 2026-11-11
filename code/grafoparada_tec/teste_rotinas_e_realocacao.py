# -*- coding: utf-8 -*-
"""
Bateria de Testes Automatizados · Rodada de Usabilidade, Rotinas Pendulares e Realocação CTM
Projeto GrafoParada · Tópicos Avançados em Inteligência Artificial (AI4Good / UFRPE)
Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)
"""

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

html_path = Path("code/grafoparada_web/index.html")
if not html_path.exists():
    html_path = Path("code/grafoparada_tec/prototipo_grafoparada.html")

assert html_path.exists(), f"Arquivo não encontrado: {html_path}"
html = html_path.read_text(encoding="utf-8")

print(f"[*] Auditando artefato: {html_path} ({len(html):,} caracteres / {html_path.stat().st_size:,} bytes)")

testes = [
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
for nome, fragmento in testes:
    if fragmento in html:
        print(f"  [PASS] {nome}")
        aprovados += 1
    else:
        print(f"  [FAIL] {nome} - Fragmento ausente: '{fragmento}'")

total = len(testes)
taxa = (aprovados / total) * 100
print(f"\n[RESULTADO DA AUDITORIA] {aprovados}/{total} testes aprovados ({taxa:.1f}% de conformidade).")

if aprovados == total:
    print("[STATUS] 100% APROVADO! Todos os requisitos de rotina, usabilidade universal e mitigação de frota no vazio validados.")
    sys.exit(0)
else:
    print("[STATUS] FALHA: Alguns requisitos não foram encontrados.")
    sys.exit(1)
