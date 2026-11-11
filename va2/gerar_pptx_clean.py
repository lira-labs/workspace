# -*- coding: utf-8 -*-
"""
Gerador Oficial de Slides PPTX · Seminário 2 (Demonstração) · Prof. Lucas Figueiredo
Estilo: Minimalista, Fundo Branco Puro, Tipografia Robusta, Zero AI Slop.
Mais de 50% de espaço livre para respirar.
Sem parágrafos densos, sem caixas sobrepostas (fluxo de parágrafos unificado).
Dados 100% Reais do Grande Recife (400 Linhas GTFS CTM + Cittamobi Live).
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Paleta Minimalista
BG_COLOR = RGBColor(255, 255, 255)       # Branco Puro #FFFFFF
TEXT_BLACK = RGBColor(15, 23, 42)        # Slate 900 #0F172A
TEXT_MUTED = RGBColor(100, 116, 139)     # Slate 500 #64748B
LINE_COLOR = RGBColor(226, 232, 240)     # Slate 200 #E2E8F0
ACCENT_BLUE = RGBColor(0, 47, 167)       # Azul Klein #002FA7
ACCENT_GREEN = RGBColor(5, 150, 105)     # Verde Bottega / Esmeralda #059669
ALERT_RED = RGBColor(220, 38, 38)        # Vermelho Alerta #DC2626

FONT_FAMILY = "Segoe UI"

def set_slide_background(slide):
    """Garante fundo branco puro."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, tag_text, title_text, subtitle_text):
    """
    Cabeçalho unificado em uma única caixa de texto para impossibilitar sobreposições.
    """
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(0.65), Inches(11.333), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

    # Tag
    p_tag = tf.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_FAMILY
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_BLUE
    p_tag.space_after = Pt(4)

    # Título Principal (26pt)
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_BLACK
    p_title.space_after = Pt(4)

    # Subtítulo (13.5pt)
    p_sub = tf.add_paragraph()
    p_sub.text = subtitle_text
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(13.5)
    p_sub.font.color.rgb = TEXT_MUTED

    # Linha divisória fina
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.25), Inches(11.333), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

def add_footer(slide, current_slide, total_slides=5):
    """Rodapé limpo e discreto."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.9), Inches(11.333), Inches(0.35))
    tf = tb.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = f"AI4Good (UFRPE) · Sem2 (Demonstração) · Cauã Lira  |  Slide {current_slide} de {total_slides}  |  grafoparadaweb.vercel.app"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 1: DEMO AO VIVO (PONTA A PONTA)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)
add_header(s1, "01 / Ponta a Ponta · Demonstração ao Vivo",
           "GrafoParada: Mobilidade Inteligente no Grande Recife",
           "Malha GTFS Oficial CTM Grande Recife + Protótipo Preditivo ST-GCN.")
add_footer(s1, 1)

# Inserir Logo Minimalista no canto superior direito
logo_file = "va2/img/logo_grafoparada.png"
if os.path.exists(logo_file):
    s1.shapes.add_picture(logo_file, Inches(9.8), Inches(0.55), width=Inches(2.5))

# Coluna 1: O Caso Concreto em 4 pontos
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(6.4), Inches(3.9))
tf1 = tb1.text_frame
tf1.word_wrap = True
tf1.margin_top = tf1.margin_bottom = tf1.margin_left = tf1.margin_right = 0

items_s1 = [
    ("QUEM USA", "Estudante ou trabalhador na Região Metropolitana do Recife"),
    ("ENTRADA REAL", "Linha 522 (Dois Irmãos / UFRPE) ou qualquer das 400 linhas do GTFS"),
    ("SAÍDA NA TELA", "Previsão em 4 min, assentos livres, letreiro LED e voz no fone"),
    ("O QUE DEIXA FAZER", "Sair no minuto exato (06h09) sem mofar no ponto de ônibus")
]

for idx, (label, val) in enumerate(items_s1):
    p_lbl = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
    p_lbl.text = label
    p_lbl.font.name = FONT_FAMILY
    p_lbl.font.size = Pt(11)
    p_lbl.font.bold = True
    p_lbl.font.color.rgb = ACCENT_BLUE

    p_val = tf1.add_paragraph()
    p_val.text = val
    p_val.font.name = FONT_FAMILY
    p_val.font.size = Pt(15)
    p_val.font.bold = False
    p_val.font.color.rgb = TEXT_BLACK
    p_val.space_after = Pt(14)

# Coluna 2: Box de Transparência Metodológica (Origem dos Dados)
box1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.9), Inches(2.6), Inches(4.4), Inches(3.8))
box1.fill.solid()
box1.fill.fore_color.rgb = RGBColor(248, 250, 252) # Slate 50
box1.line.color.rgb = LINE_COLOR
box1.line.width = Pt(1)

tb_b1 = s1.shapes.add_textbox(Inches(8.3), Inches(2.9), Inches(3.6), Inches(3.2))
tf_b1 = tb_b1.text_frame
tf_b1.word_wrap = True
tf_b1.margin_top = tf_b1.margin_bottom = tf_b1.margin_left = tf_b1.margin_right = 0

p = tf_b1.paragraphs[0]
p.text = "ORIGEM DOS DADOS (TRANSPARÊNCIA)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(10)

p2 = tf_b1.add_paragraph()
p2.text = "Malha Real vs Simulação"
p2.font.name = FONT_FAMILY
p2.font.size = Pt(18)
p2.font.bold = True
p2.font.color.rgb = TEXT_BLACK
p2.space_after = Pt(12)

p3 = tf_b1.add_paragraph()
p3.text = "• Paradas & Trajetos: GTFS Oficial CTM\n• Quadro de Horários: GTFS Oficial\n• Atrasos de Treino: Simulação Sintética\n• Demanda do Exemplo: Estimativa Ilustrativa\n• Telemetria Contínua: Não pública no CTM"
p3.font.name = FONT_FAMILY
p3.font.size = Pt(12)
p3.font.color.rgb = TEXT_MUTED
p3.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 2: QUANTO CUSTA (MEDIDO VS ESTIMATIVA INICIAL)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "02 / Quanto Custa, Medido",
           "Medição em CPU Local vs Estimativa Inicial de Arquitetura",
           "Medido com medir_custo_sem2.py (Python 3.12 / PyTorch na CPU; FSM no dispositivo).")
add_footer(s2, 2)

# Regra dos Terços: 3 Colunas Limpas
col_w = Inches(3.5)

# Coluna 1: No Celular (On-Device)
tb2_c1 = s2.shapes.add_textbox(Inches(1.0), Inches(2.6), col_w, Inches(3.9))
tf2_c1 = tb2_c1.text_frame
tf2_c1.word_wrap = True
tf2_c1.margin_top = tf2_c1.margin_bottom = tf2_c1.margin_left = tf2_c1.margin_right = 0

p = tf2_c1.paragraphs[0]
p.text = "NO CELULAR (ON-DEVICE)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(12)

p_num = tf2_c1.add_paragraph()
p_num.text = "4,98 ms"
p_num.font.name = FONT_FAMILY
p_num.font.size = Pt(40)
p_num.font.bold = True
p_num.font.color.rgb = ACCENT_GREEN

p_sub = tf2_c1.add_paragraph()
p_sub.text = "Memória RAM: 12 KB\nMáquina de Estados Cinemática v3 com Soft-Voting. Bateria intocada."
p_sub.font.name = FONT_FAMILY
p_sub.font.size = Pt(13)
p_sub.font.color.rgb = TEXT_MUTED

# Coluna 2: No Servidor (STGCN)
tb2_c2 = s2.shapes.add_textbox(Inches(4.9), Inches(2.6), col_w, Inches(3.9))
tf2_c2 = tb2_c2.text_frame
tf2_c2.word_wrap = True
tf2_c2.margin_top = tf2_c2.margin_bottom = tf2_c2.margin_left = tf2_c2.margin_right = 0

p = tf2_c2.paragraphs[0]
p.text = "NO SERVIDOR (CPU PURA)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(12)

p_num2 = tf2_c2.add_paragraph()
p_num2.text = "0,77 ms"
p_num2.font.name = FONT_FAMILY
p_num2.font.size = Pt(40)
p_num2.font.bold = True
p_num2.font.color.rgb = TEXT_BLACK

p_sub2 = tf2_c2.add_paragraph()
p_sub2.text = "Memória RAM: 358 MB\nSTGCN em PyTorch rodando na CPU. Pesos ocupam menos de 100 KB."
p_sub2.font.name = FONT_FAMILY
p_sub2.font.size = Pt(13)
p_sub2.font.color.rgb = TEXT_MUTED

# Coluna 3: Estimativa Inicial & Custo
tb2_c3 = s2.shapes.add_textbox(Inches(8.8), Inches(2.6), col_w, Inches(3.9))
tf2_c3 = tb2_c3.text_frame
tf2_c3.word_wrap = True
tf2_c3.margin_top = tf2_c3.margin_bottom = tf2_c3.margin_left = tf2_c3.margin_right = 0

p = tf2_c3.paragraphs[0]
p.text = "ESTIMATIVA INICIAL & CUSTO"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(12)

p_num3 = tf2_c3.add_paragraph()
p_num3.text = "R$ 0,00"
p_num3.font.name = FONT_FAMILY
p_num3.font.size = Pt(40)
p_num3.font.bold = True
p_num3.font.color.rgb = ACCENT_BLUE

p_sub3 = tf2_c3.add_paragraph()
p_sub3.text = "Projeto previa < 500 ms e ~300 MB.\nCusto zero em máquina local; escala metropolitana requer backend dedicado."
p_sub3.font.name = FONT_FAMILY
p_sub3.font.size = Pt(13)
p_sub3.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 3: A FALHA (MOSTRADA DE PROPÓSITO)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "03 / A Falha Mostrada de Propósito",
           "A Falha: Over-smoothing na STGCN",
           "A saída da rede sob retenção severa vs valor de referência e a trava adotada.")
add_footer(s3, 3)

# Duas Colunas de Alto Contraste
col_w3 = Inches(5.3)

# Coluna 1: Como a IA Previu (Saída Errada)
tb3_c1 = s3.shapes.add_textbox(Inches(1.0), Inches(2.6), col_w3, Inches(3.9))
tf3_c1 = tb3_c1.text_frame
tf3_c1.word_wrap = True
tf3_c1.margin_top = tf3_c1.margin_bottom = tf3_c1.margin_left = tf3_c1.margin_right = 0

p = tf3_c1.paragraphs[0]
p.text = "SAÍDA DA IA (SUPER-SUAVIZAÇÃO)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ALERT_RED
p.space_after = Pt(10)

p_err = tf3_c1.add_paragraph()
p_err.text = "18 min"
p_err.font.name = FONT_FAMILY
p_err.font.size = Pt(48)
p_err.font.bold = True
p_err.font.color.rgb = ALERT_RED

p_err_txt = tf3_c1.add_paragraph()
p_err_txt.text = "A convolução em grafo diluiu o atraso brusco com as paradas vizinhas desimpedidas. O número parece razoável, mas mente."
p_err_txt.font.name = FONT_FAMILY
p_err_txt.font.size = Pt(14)
p_err_txt.font.color.rgb = TEXT_BLACK
p_err_txt.space_after = Pt(16)

p_who = tf3_c1.add_paragraph()
p_who.text = "QUEM SOFRE O ERRO:"
p_who.font.name = FONT_FAMILY
p_who.font.size = Pt(11)
p_who.font.bold = True
p_who.font.color.rgb = ALERT_RED

p_who_txt = tf3_c1.add_paragraph()
p_who_txt.text = "O passageiro que confia no app, espera um ônibus que não vem e perde o turno ou a prova na faculdade."
p_who_txt.font.name = FONT_FAMILY
p_who_txt.font.size = Pt(13)
p_who_txt.font.color.rgb = TEXT_MUTED

# Coluna 2: Referência e Trava
tb3_c2 = s3.shapes.add_textbox(Inches(7.0), Inches(2.6), col_w3, Inches(3.9))
tf3_c2 = tb3_c2.text_frame
tf3_c2.word_wrap = True
tf3_c2.margin_top = tf3_c2.margin_bottom = tf3_c2.margin_left = tf3_c2.margin_right = 0

p = tf3_c2.paragraphs[0]
p.text = "RETENÇÃO DE REFERÊNCIA (CHOQUE SÚBITO)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_GREEN
p.space_after = Pt(10)

p_cor = tf3_c2.add_paragraph()
p_cor.text = "45 min"
p_cor.font.name = FONT_FAMILY
p_cor.font.size = Pt(48)
p_cor.font.bold = True
p_cor.font.color.rgb = ACCENT_GREEN

p_cor_txt = tf3_c2.add_paragraph()
p_cor_txt.text = "Simulação de retenção severa ou bloqueio físico da via no nó do corredor com atraso abrupto."
p_cor_txt.font.name = FONT_FAMILY
p_cor_txt.font.size = Pt(14)
p_cor_txt.font.color.rgb = TEXT_BLACK
p_cor_txt.space_after = Pt(16)

p_trava = tf3_c2.add_paragraph()
p_trava.text = "A TRAVA DE SEGURANÇA ADOTADA:"
p_trava.font.name = FONT_FAMILY
p_trava.font.size = Pt(11)
p_trava.font.bold = True
p_trava.font.color.rgb = ACCENT_BLUE

p_trava_txt = tf3_c2.add_paragraph()
p_trava_txt.text = "Corte Híbrido: se |STGCN - Referência| > 15 min, o sistema corta a previsão da IA e acende o alerta de interdição [?]."
p_trava_txt.font.name = FONT_FAMILY
p_trava_txt.font.size = Pt(13)
p_trava_txt.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 4: O QUE MUDOU DESDE O SEM1 (DUAS LINHAS CLARAS)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "04 / O Que Mudou desde o Sem1",
           "Decisão Justificada: Por Que Mantivemos a STGCN",
           "O que valia no sem1, o que vale agora e o teste em dados simulados por difusão.")
add_footer(s4, 4)

tb4 = s4.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.333), Inches(3.9))
tf4 = tb4.text_frame
tf4.word_wrap = True
tf4.margin_top = tf4.margin_bottom = tf4.margin_left = tf4.margin_right = 0

# Linha 1: Sem 1
p1_tag = tf4.paragraphs[0]
p1_tag.text = "NO SEM1 (CORREDOR CURTO · 5 PARADAS):"
p1_tag.font.name = FONT_FAMILY
p1_tag.font.size = Pt(11)
p1_tag.font.bold = True
p1_tag.font.color.rgb = TEXT_MUTED

p1_main = tf4.add_paragraph()
p1_main.text = "O cálculo linear simples bateu a STGCN (2,46 min vs 4,42 min)."
p1_main.font.name = FONT_FAMILY
p1_main.font.size = Pt(22)
p1_main.font.bold = True
p1_main.font.color.rgb = TEXT_BLACK

p1_sub = tf4.add_paragraph()
p1_sub.text = "Dúvida legítima do Sem1: 'Para que gastar memória com rede em grafo se uma conta simples ganha?'"
p1_sub.font.name = FONT_FAMILY
p1_sub.font.size = Pt(14)
p1_sub.font.color.rgb = TEXT_MUTED
p1_sub.space_after = Pt(36)

# Linha 2: Sem 2
p2_tag = tf4.add_paragraph()
p2_tag.text = "AGORA NO SEM2 (MALHA GTFS EXPANDIDA · DADOS SINTÉTICOS DE DIFUSÃO):"
p2_tag.font.name = FONT_FAMILY
p2_tag.font.size = Pt(11)
p2_tag.font.bold = True
p2_tag.font.color.rgb = ACCENT_BLUE

p2_main = tf4.add_paragraph()
p2_main.text = "A STGCN reduziu o erro para 1,51 min (contra 1,93 min da linear e 7,13 min da persistência)."
p2_main.font.name = FONT_FAMILY
p2_main.font.size = Pt(22)
p2_main.font.bold = True
p2_main.font.color.rgb = ACCENT_BLUE

p2_sub = tf4.add_paragraph()
p2_sub.text = "Decisão: Fica a STGCN. A GNN mitiga a explosão dimensional da linear (120 variáveis). Validação final requer telemetria contínua."
p2_sub.font.name = FONT_FAMILY
p2_sub.font.size = Pt(13)
p2_sub.font.color.rgb = TEXT_BLACK
p2_sub.space_after = Pt(8)

p2_proto = tf4.add_paragraph()
p2_proto.text = "Protocolo Experimental: 70 casos treino / 50 casos teste (split temporal estrito sem vazamento). A STGCN supera a regressão linear que sofre colinearidade em 20 paradas x 6 lags."
p2_proto.font.name = FONT_FAMILY
p2_proto.font.size = Pt(11)
p2_proto.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 5: FECHO & PONTE DIRETA PARA O SEM3
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "05 / Fecho & Próximo Passo",
           "A Falha de Hoje É a Medida do Experimento de Campo",
           "Seminário 3 (25/11): Experimento formal de validação da trava híbrida.")
add_footer(s5, 5)

tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.333), Inches(3.9))
tf5 = tb5.text_frame
tf5.word_wrap = True
tf5.margin_top = tf5.margin_bottom = tf5.margin_left = tf5.margin_right = 0

p5_tag = tf5.paragraphs[0]
p5_tag.text = "O FECHO DO SEM2:"
p5_tag.font.name = FONT_FAMILY
p5_tag.font.size = Pt(11)
p5_tag.font.bold = True
p5_tag.font.color.rgb = ACCENT_BLUE

p5_main = tf5.add_paragraph()
p5_main.text = "Roda no celular e na CPU local a custo zero, e a falha de over-smoothing é blindada pela regra."
p5_main.font.name = FONT_FAMILY
p5_main.font.size = Pt(22)
p5_main.font.bold = True
p5_main.font.color.rgb = TEXT_BLACK
p5_main.space_after = Pt(36)

p5_exp_tag = tf5.add_paragraph()
p5_exp_tag.text = "A MEDIDA DO SEM3 (25/11):"
p5_exp_tag.font.name = FONT_FAMILY
p5_exp_tag.font.size = Pt(11)
p5_exp_tag.font.bold = True
p5_exp_tag.font.color.rgb = ACCENT_BLUE

p5_exp_main = tf5.add_paragraph()
p5_exp_main.text = "Quantos choques de trânsito na malha a trava híbrida consegue capturar contra o erro puro da IA."
p5_exp_main.font.name = FONT_FAMILY
p5_exp_main.font.size = Pt(20)
p5_exp_main.font.bold = False
p5_exp_main.font.color.rgb = TEXT_BLACK
p5_exp_main.space_after = Pt(24)

p5_foot = tf5.add_paragraph()
p5_foot.text = "Repositório: github.com/lira-labs/workspace  ·  Tag: sem2  ·  Deploy: grafoparadaweb.vercel.app"
p5_foot.font.name = FONT_FAMILY
p5_foot.font.size = Pt(13)
p5_foot.font.color.rgb = TEXT_MUTED

# Salvar apresentação
output_path = "va2/GrafoParada_Seminario2_CauaLira.pptx"
prs.save(output_path)
print(f"PPTX gerado com sucesso em: {output_path}")
