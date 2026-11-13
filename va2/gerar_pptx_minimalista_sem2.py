# -*- coding: utf-8 -*-
"""
Gerador do Deck Oficial Sem2 (Minimalista Suíço · 1 Ideia por Slide · Sem Parágrafos)
Alinhado estritamente aos 4 itens de verificação do Seminário 2 (AI4Good · UFRPE)
e às medições reais de `medir_custo_sem2.py` / `motor_evolucao_prototipo.py`.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

BG_WHITE = RGBColor(255, 255, 255)
CARD_BG = RGBColor(248, 249, 250)
TEXT_BLACK = RGBColor(17, 24, 39)
TEXT_DARK = RGBColor(55, 65, 81)
TEXT_MUTED = RGBColor(107, 114, 128)
LINE_BORDER = RGBColor(229, 231, 235)

KLEIN_BLUE = RGBColor(0, 47, 167)
BOTTEGA_GREEN = RGBColor(16, 124, 65)
CRIMSON_RED = RGBColor(192, 0, 0)

FONT_FAMILY = "Segoe UI"


def add_base_slide(tag_text: str, tag_color: RGBColor, title_text: str, subtitle_text: str, slide_num: int):
    slide = prs.slides.add_slide(blank_layout)

    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_WHITE
    bg.line.fill.background()

    rule_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(0.48), Inches(11.63), Inches(0.015))
    rule_top.fill.solid()
    rule_top.fill.fore_color.rgb = LINE_BORDER
    rule_top.line.fill.background()

    tb_tag = slide.shapes.add_textbox(Inches(0.85), Inches(0.58), Inches(11.63), Inches(0.32))
    tf = tb_tag.text_frame
    p = tf.paragraphs[0]
    p.text = tag_text.upper()
    p.font.name = FONT_FAMILY
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = tag_color

    tb_title = slide.shapes.add_textbox(Inches(0.85), Inches(0.95), Inches(11.63), Inches(0.85))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    pt = tf_t.paragraphs[0]
    pt.text = title_text
    pt.font.name = FONT_FAMILY
    pt.font.size = Pt(34)
    pt.font.bold = True
    pt.font.color.rgb = TEXT_BLACK

    tb_sub = slide.shapes.add_textbox(Inches(0.85), Inches(1.85), Inches(11.63), Inches(0.45))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    ps = tf_s.paragraphs[0]
    ps.text = subtitle_text
    ps.font.name = FONT_FAMILY
    ps.font.size = Pt(15)
    ps.font.color.rgb = TEXT_MUTED

    rule_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.85), Inches(6.82), Inches(11.63), Inches(0.015))
    rule_bot.fill.solid()
    rule_bot.fill.fore_color.rgb = LINE_BORDER
    rule_bot.line.fill.background()

    tb_foot = slide.shapes.add_textbox(Inches(0.85), Inches(6.9), Inches(11.63), Inches(0.35))
    pf = tb_foot.text_frame.paragraphs[0]
    pf.text = f"AI4Good (UFRPE) · Prof. Lucas Silva Figueiredo | Cauã da Cunha Lira · Slide {slide_num} de 5"
    pf.font.name = FONT_FAMILY
    pf.font.size = Pt(10)
    pf.font.color.rgb = TEXT_MUTED

    return slide


def add_kv_block(slide, left, top, width, label, value, label_color=KLEIN_BLUE, val_size=18):
    tb = slide.shapes.add_textbox(left, top, width, Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = label.upper()
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = label_color
    p1.space_after = Pt(2)

    p2 = tf.add_paragraph()
    p2.text = value
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(val_size)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_BLACK


# SLIDE 1 · PONTA A PONTA (AO VIVO)
s1 = add_base_slide(
    "01 / PONTA A PONTA · DEMO AO VIVO",
    KLEIN_BLUE,
    "GrafoParada ao vivo: do GPS atual à janela de saída",
    "393 linhas reais do GTFS CTM Grande Recife · Tag sem2",
    1,
)
s1_items = [
    ("Quem usa", "Passageiro ou trabalhador no Grande Recife"),
    ("Entrada real", "Localização GPS + destino (ex.: Camela -> Olinda ou linha GTFS)"),
    ("Saída na tela", "Rota com baldeações SEI, previsão de espera e voz PT-BR"),
    ("O que deixa fazer", "Escolher a linha certa e sair na hora segura sem esperar no vazio"),
]
for idx, (lbl, val) in enumerate(s1_items):
    add_kv_block(s1, Inches(0.85), Inches(2.55 + idx * 0.98), Inches(6.6), lbl, val, KLEIN_BLUE, 16.5)

box1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.9), Inches(2.6), Inches(4.55), Inches(3.2))
box1.fill.solid()
box1.fill.fore_color.rgb = CARD_BG
box1.line.color.rgb = LINE_BORDER
tb_b1 = s1.shapes.add_textbox(Inches(8.2), Inches(2.85), Inches(3.95), Inches(2.7))
tf_b1 = tb_b1.text_frame
tf_b1.word_wrap = True
pb1 = tf_b1.paragraphs[0]
pb1.text = "SISTEMA RODANDO AO VIVO"
pb1.font.name = FONT_FAMILY
pb1.font.size = Pt(11)
pb1.font.bold = True
pb1.font.color.rgb = KLEIN_BLUE
pb1.space_after = Pt(8)
pb2 = tf_b1.add_paragraph()
pb2.text = "grafoparadaweb.vercel.app"
pb2.font.name = FONT_FAMILY
pb2.font.size = Pt(22)
pb2.font.bold = True
pb2.font.color.rgb = TEXT_BLACK
pb2.space_after = Pt(12)
pb3 = tf_b1.add_paragraph()
pb3.text = "Demonstrado ao vivo no celular espelhado direto de github.com/lira-labs/workspace."
pb3.font.name = FONT_FAMILY
pb3.font.size = Pt(14)
pb3.font.color.rgb = TEXT_DARK


# SLIDE 2 · QUANTO CUSTA, MEDIDO VS FLX.MD
s2 = add_base_slide(
    "02 / QUANTO CUSTA, MEDIDO",
    KLEIN_BLUE,
    "Medido em execução real vs. estimado no flx.md",
    "medir_custo_sem2.py · AMD Ryzen 7 5700G · Windows 11 · Python 3.12.15 · PyTorch 2.14.1+cpu",
    2,
)

# Coluna esquerda: Medido
tb_m = s2.shapes.add_textbox(Inches(0.85), Inches(2.5), Inches(5.6), Inches(3.8))
tfm = tb_m.text_frame
tfm.word_wrap = True
for text, size, bold, color, after in [
    ("MEDIDO NO REPOSITÓRIO (EXECUÇÃO REAL)", 11, True, KLEIN_BLUE, 10),
    ("0,96 ms · 324,7 MB", 38, True, TEXT_BLACK, 4),
    ("STGCN 20 nós em CPU (0,86 s treino 25 épocas · 2,22 KB heap)", 13.5, False, TEXT_MUTED, 22),
    ("56,68 µs · 11,02 KB", 38, True, TEXT_BLACK, 4),
    ("FSM cinemática V3 on-device (trajetória de 15 passos)", 13.5, False, TEXT_MUTED, 0),
]:
    p = tfm.paragraphs[0] if len(tfm.paragraphs) == 1 and not tfm.paragraphs[0].text else tfm.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)

# Coluna direita: flx.md + diferença
tb_f = s2.shapes.add_textbox(Inches(6.95), Inches(2.5), Inches(5.5), Inches(3.9))
tff = tb_f.text_frame
tff.word_wrap = True
for text, size, bold, color, after in [
    ("ESTIMADO NO FLX.MD", 11, True, TEXT_MUTED, 10),
    ("< 500 ms · ~300 MB", 38, True, TEXT_MUTED, 4),
    ("STGCN em CPU (< 10 s com treino) · R$ 0,00 local", 13.5, False, TEXT_MUTED, 18),
    ("14,29 µs · 8,92 KB", 28, True, TEXT_MUTED, 4),
    ("App on-device no flx.md (passo único)", 13.5, False, TEXT_MUTED, 18),
    ("Causa: runtime LibTorch/Windows retém 324,7 MB (+8,2% vs ~300 MB); inferência foi ~520x menor que 500 ms.", 14, True, TEXT_BLACK, 0),
]:
    p = tff.paragraphs[0] if len(tff.paragraphs) == 1 and not tff.paragraphs[0].text else tff.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)


# SLIDE 3 · A FALHA MOSTRADA DE PROPÓSITO
s3 = add_base_slide(
    "03 / A FALHA MOSTRADA DE PROPÓSITO",
    CRIMSON_RED,
    "Choque no Trevo de Ipojuca (Nó 10 · PE-60): como saiu vs. o certo",
    "Entrada: retenção abrupta de 45,0 min no GPS enquanto o corredor estava em 10,0 min.",
    3,
)

tb_e1 = s3.shapes.add_textbox(Inches(0.85), Inches(2.55), Inches(5.6), Inches(3.8))
tfe1 = tb_e1.text_frame
tfe1.word_wrap = True
for text, size, bold, color, after in [
    ("SAÍDA DA STGCN (COMO SAIU)", 11, True, CRIMSON_RED, 8),
    ("14,3 min", 48, True, CRIMSON_RED, 4),
    ("Super-suavização apagou 30,7 min do choque súbito", 14, False, TEXT_MUTED, 28),
    ("QUEM SOFRE ESSE ERRO", 11, True, CRIMSON_RED, 6),
    ("Trabalhador na PE-60: confia nos 14,3 min, perde o alternativo e perde o turno.", 17, True, TEXT_BLACK, 0),
]:
    p = tfe1.paragraphs[0] if len(tfe1.paragraphs) == 1 and not tfe1.paragraphs[0].text else tfe1.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)

tb_e2 = s3.shapes.add_textbox(Inches(6.95), Inches(2.55), Inches(5.5), Inches(3.8))
tfe2 = tb_e2.text_frame
tfe2.word_wrap = True
for text, size, bold, color, after in [
    ("O CERTO (GPS BRUTO + TRAVA [?])", 11, True, BOTTEGA_GREEN, 8),
    ("45,0 min", 48, True, BOTTEGA_GREEN, 4),
    ("Alerta crítico de interdição [?] na tela", 14, False, TEXT_MUTED, 28),
    ("O QUE REVELA (REGRA HÍBRIDA)", 11, True, KLEIN_BLUE, 6),
    ("|GPS - STGCN| > 15 min corta a IA e exibe o GPS bruto.", 17, True, TEXT_BLACK, 0),
]:
    p = tfe2.paragraphs[0] if len(tfe2.paragraphs) == 1 and not tfe2.paragraphs[0].text else tfe2.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)


# SLIDE 4 · O QUE MUDOU DESDE O SEM1
s4 = add_base_slide(
    "04 / O QUE MUDOU DESDE O SEM1",
    KLEIN_BLUE,
    "Por que mantive a STGCN depois de perder no sem1",
    "avaliar_piloto.py (5 paradas) vs. motor_evolucao_prototipo.py (20 paradas · dados sintéticos)",
    4,
)

tb_4 = s4.shapes.add_textbox(Inches(0.85), Inches(2.6), Inches(11.6), Inches(3.8))
tf4 = tb_4.text_frame
tf4.word_wrap = True
for text, size, bold, color, after in [
    ("NO SEM1 · CORREDOR CURTO (5 PARADAS)", 11.5, True, TEXT_MUTED, 6),
    ("Conta linear simples venceu a STGCN: 2,46 min vs. 4,42 min (MAE)", 23, True, TEXT_BLACK, 34),
    ("AGORA NO SEM2 · MALHA EXPANDIDA (20 PARADAS PE-60 · SIMULAÇÃO SINTÉTICA)", 11.5, True, KLEIN_BLUE, 6),
    ("Mantida por escala: STGCN 1,51 min vs. Linear 1,93 min vs. Persistência 7,13 min", 23, True, KLEIN_BLUE, 10),
    ("A linear achata 121 colunas para 70 treinos; validação em campo real ainda requer GPS contínuo do CTM.", 15, False, TEXT_MUTED, 0),
]:
    p = tf4.paragraphs[0] if len(tf4.paragraphs) == 1 and not tf4.paragraphs[0].text else tf4.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)


# SLIDE 5 · FECHO E PONTE PARA O SEM3
s5 = add_base_slide(
    "05 / FECHO · PONTE PARA O SEM3",
    KLEIN_BLUE,
    "A falha mostrada hoje vira a medida do sem3",
    "25/11 · Experimento com a trava híbrida contra a STGCN pura",
    5,
)

tb_5 = s5.shapes.add_textbox(Inches(0.85), Inches(2.6), Inches(11.6), Inches(3.8))
tf5 = tb_5.text_frame
tf5.word_wrap = True
for text, size, bold, color, after in [
    ("HOJE NO REPOSITÓRIO", 11.5, True, KLEIN_BLUE, 6),
    ("393 linhas GTFS, 0,96 ms na CPU, R$ 0,00 local e trava [?] pronta para choques súbitos", 22, True, TEXT_BLACK, 34),
    ("NO SEM3 (25/11)", 11.5, True, KLEIN_BLUE, 6),
    ("Quantos choques de via a trava híbrida captura contra o erro silencioso da STGCN", 22, True, KLEIN_BLUE, 12),
    ("github.com/lira-labs/workspace · grafoparadaweb.vercel.app", 14.5, False, TEXT_MUTED, 0),
]:
    p = tf5.paragraphs[0] if len(tf5.paragraphs) == 1 and not tf5.paragraphs[0].text else tf5.add_paragraph()
    p.text = text
    p.font.name = FONT_FAMILY
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.space_after = Pt(after)


outputs = [
    Path("va2/GrafoParada_Sem2_Roteiro.pptx"),
    Path("code/grafoparada_web/GrafoParada_Sem2_Roteiro.pptx"),
]
drive_dir = Path(r"G:\Meu Drive\IA_Projetos")
if drive_dir.exists():
    outputs.append(drive_dir / "GrafoParada_Sem2_Roteiro.pptx")

for out in outputs:
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    print(f"[OK] PPTX 16:9 salvo: {out} ({out.stat().st_size:,} bytes)")
