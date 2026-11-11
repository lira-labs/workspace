# -*- coding: utf-8 -*-
"""
Gerador de Slides Minimalista e Direto (Padrão sem2-excelente do Prof. Lucas)
Sem sobreposição de texto, sem parágrafos densos, sem AI Slop.
Apenas números medidos, ideias centrais e suporte para a fala do aluno.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Paleta limpa e contrastante
BG_COLOR = RGBColor(255, 255, 255)       # Branco Puro
TEXT_MAIN = RGBColor(17, 24, 39)         # Quase Preto #111827
TEXT_MUTED = RGBColor(107, 114, 128)     # Cinza Médio #6B7280
LINE_COLOR = RGBColor(229, 231, 235)     # Linha #E5E7EB
ACCENT_BLUE = RGBColor(0, 47, 167)       # Azul Klein #002FA7
ALERT_RED = RGBColor(192, 0, 0)          # Carmesim #C00000
ACCENT_GREEN = RGBColor(16, 124, 65)     # Verde #107C41

FONT_FAMILY = "Segoe UI"

def add_header(slide, tag, title, subtitle):
    """Adiciona cabeçalho com espaçamento vertical estrito sem sobreposição."""
    # Tag superior
    tb_tag = slide.shapes.add_textbox(Inches(1.0), Inches(0.6), Inches(11.333), Inches(0.35))
    tf_tag = tb_tag.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag.upper()
    p_tag.font.name = FONT_FAMILY
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_BLUE

    # Título Principal
    tb_title = slide.shapes.add_textbox(Inches(1.0), Inches(1.05), Inches(11.333), Inches(0.6))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    tf_title.margin_top = tf_title.margin_bottom = tf_title.margin_left = tf_title.margin_right = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_MAIN

    # Subtítulo explicativo curto
    tb_sub = slide.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.333), Inches(0.4))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    tf_sub.margin_top = tf_sub.margin_bottom = tf_sub.margin_left = tf_sub.margin_right = 0
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(14)
    p_sub.font.color.rgb = TEXT_MUTED

    # Linha divisória
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.25), Inches(11.333), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

def add_footer(slide, slide_num):
    """Adiciona rodapé limpo."""
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(6.8), Inches(11.333), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = LINE_COLOR
    line.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(1.0), Inches(6.9), Inches(11.333), Inches(0.35))
    tf = tb.text_frame
    tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
    p = tf.paragraphs[0]
    p.text = f"AI4Good (UFRPE) · Sem2 · Cauã da Cunha Lira | Slide {slide_num} de 5"
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 1: DEMO AO VIVO (PONTA A PONTA)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
add_header(s1, "01 / Ponta a Ponta · Demo ao Vivo", 
           "GrafoParada: Previsão da Linha 199 na PE-60", 
           "Usuário real, entrada real e o que a tela deixa o passageiro fazer.")
add_footer(s1, 1)

# Coluna 1: O Caso Concreto
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(6.2), Inches(3.8))
tf1 = tb1.text_frame
tf1.word_wrap = True
tf1.margin_top = tf1.margin_bottom = tf1.margin_left = tf1.margin_right = 0

items_s1 = [
    ("QUEM USA", "Passageiro trabalhador na parada da PE-60 (Camela / Ipojuca)"),
    ("ENTRADA REAL", "Linha 199 (Camela ➔ TI Cabo), saída às 06h10 para Suape"),
    ("SAÍDA NA TELA", "Previsão exata: 4 min, Plataforma 04, 14 assentos livres"),
    ("O QUE DEIXA FAZER", "Sair no minuto certo (06h08) sem mofar no acostamento escuro")
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
    p_val.font.color.rgb = TEXT_MAIN
    p_val.space_after = Pt(14)

# Coluna 2: Box de Execução ao Vivo
box_demo = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.8), Inches(2.7), Inches(4.5), Inches(3.6))
box_demo.fill.solid()
box_demo.fill.fore_color.rgb = RGBColor(248, 249, 250)
box_demo.line.color.rgb = LINE_COLOR
box_demo.line.width = Pt(1)

tb_box = s1.shapes.add_textbox(Inches(8.2), Inches(3.0), Inches(3.7), Inches(3.0))
tf_box = tb_box.text_frame
tf_box.word_wrap = True
tf_box.margin_top = tf_box.margin_bottom = tf_box.margin_left = tf_box.margin_right = 0

p = tf_box.paragraphs[0]
p.text = "DEMONSTRAÇÃO AO VIVO"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(16)

p2 = tf_box.add_paragraph()
p2.text = "Roda direto do repositório"
p2.font.name = FONT_FAMILY
p2.font.size = Pt(18)
p2.font.bold = True
p2.font.color.rgb = TEXT_MAIN
p2.space_after = Pt(14)

p3 = tf_box.add_paragraph()
p3.text = "• Web: grafoparadaweb.vercel.app\n• Commit: 0cdf397\n• Aparelho: Celular espelhado na sala\n• Reserva: Vídeo contínuo gravado"
p3.font.name = FONT_FAMILY
p3.font.size = Pt(13)
p3.font.color.rgb = TEXT_MUTED


# ==============================================================================
# SLIDE 2: QUANTO CUSTA (MEDIDO VS FLX.MD)
# ==============================================================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "02 / Quanto Custa, Medido", 
           "Medição Real na Máquina vs Estimativa do flx", 
           "Execução com medir_custo_sem2.py identificada por tempo e pico de memória.")
add_footer(s2, 2)

# Bloco Esquerdo: MEDIDO
tb2_left = s2.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.4), Inches(3.8))
tf2_left = tb2_left.text_frame
tf2_left.word_wrap = True
tf2_left.margin_top = tf2_left.margin_bottom = tf2_left.margin_left = tf2_left.margin_right = 0

p = tf2_left.paragraphs[0]
p.text = "MEDIDO NESTA MÁQUINA (COMMIT 0CDF397)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE
p.space_after = Pt(14)

# Número 1 Celular
p_c1 = tf2_left.add_paragraph()
p_c1.text = "4,98 ms  ·  12 KB"
p_c1.font.name = FONT_FAMILY
p_c1.font.size = Pt(36)
p_c1.font.bold = True
p_c1.font.color.rgb = TEXT_MAIN

p_c1_sub = tf2_left.add_paragraph()
p_c1_sub.text = "No aparelho (celular) — FSM cinemática v3"
p_c1_sub.font.name = FONT_FAMILY
p_c1_sub.font.size = Pt(13)
p_c1_sub.font.color.rgb = TEXT_MUTED
p_c1_sub.space_after = Pt(20)

# Número 2 Servidor
p_c2 = tf2_left.add_paragraph()
p_c2.text = "0,77 ms  ·  358 MB"
p_c2.font.name = FONT_FAMILY
p_c2.font.size = Pt(36)
p_c2.font.bold = True
p_c2.font.color.rgb = TEXT_MAIN

p_c2_sub = tf2_left.add_paragraph()
p_c2_sub.text = "No servidor (CPU) — STGCN em 20 paradas da PE-60"
p_c2_sub.font.name = FONT_FAMILY
p_c2_sub.font.size = Pt(13)
p_c2_sub.font.color.rgb = TEXT_MUTED


# Bloco Direito: ESTIMADO NO FLX & EXPLICAÇÃO
tb2_right = s2.shapes.add_textbox(Inches(7.2), Inches(2.7), Inches(5.1), Inches(3.8))
tf2_right = tb2_right.text_frame
tf2_right.word_wrap = True
tf2_right.margin_top = tf2_right.margin_bottom = tf2_right.margin_left = tf2_right.margin_right = 0

p_r = tf2_right.paragraphs[0]
p_r.text = "ESTIMADO NO FLX.MD"
p_r.font.name = FONT_FAMILY
p_r.font.size = Pt(11)
p_r.font.bold = True
p_r.font.color.rgb = TEXT_MUTED
p_r.space_after = Pt(14)

p_r1 = tf2_right.add_paragraph()
p_r1.text = "< 500 ms  ·  ~300 MB"
p_r1.font.name = FONT_FAMILY
p_r1.font.size = Pt(36)
p_r1.font.bold = True
p_r1.font.color.rgb = TEXT_MUTED

p_r1_sub = tf2_right.add_paragraph()
p_r1_sub.text = "Estimativa teórica preliminar do fluxo"
p_r1_sub.font.name = FONT_FAMILY
p_r1_sub.font.size = Pt(13)
p_r1_sub.font.color.rgb = TEXT_MUTED
p_r1_sub.space_after = Pt(24)

p_diff = tf2_right.add_paragraph()
p_diff.text = "A DIFERENÇA EXPLICADA:"
p_diff.font.name = FONT_FAMILY
p_diff.font.size = Pt(11)
p_diff.font.bold = True
p_diff.font.color.rgb = ACCENT_BLUE

p_diff_txt = tf2_right.add_paragraph()
p_diff_txt.text = "1. Tempo: A inferência na CPU pura levou 0,77 ms (muito menor que o teto de 500 ms).\n2. Memória: 358 MB medidos do processo PyTorch segurando bibliotecas no SO.\n3. Custo financeiro: R$ 0,00 (sem nuvem paga)."
p_diff_txt.font.name = FONT_FAMILY
p_diff_txt.font.size = Pt(13)
p_diff_txt.font.color.rgb = TEXT_MAIN


# ==============================================================================
# SLIDE 3: A FALHA REAL (MOSTRADA DE PROPÓSITO)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "03 / A Falha Mostrada de Propósito", 
           "Bloqueio no Trevo de Ipojuca: Over-smoothing na STGCN", 
           "A entrada que erra, o que sai, o certo e quem sofre.")
add_footer(s3, 3)

# Coluna 1: Como Saiu (IA)
tb3_left = s3.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(5.3), Inches(3.8))
tf3_left = tb3_left.text_frame
tf3_left.word_wrap = True
tf3_left.margin_top = tf3_left.margin_bottom = tf3_left.margin_left = tf3_left.margin_right = 0

p = tf3_left.paragraphs[0]
p.text = "COMO A IA PREVIU (SAÍDA ERRADA)"
p.font.name = FONT_FAMILY
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = ALERT_RED
p.space_after = Pt(12)

p_err = tf3_left.add_paragraph()
p_err.text = "18 minutos"
p_err.font.name = FONT_FAMILY
p_err.font.size = Pt(44)
p_err.font.bold = True
p_err.font.color.rgb = ALERT_RED

p_err_txt = tf3_left.add_paragraph()
p_err_txt.text = "A STGCN suavizou o atraso pela malha gráfica com as paradas vizinhas. O número parece razoável, mas mente."
p_err_txt.font.name = FONT_FAMILY
p_err_txt.font.size = Pt(14)
p_err_txt.font.color.rgb = TEXT_MAIN
p_err_txt.space_after = Pt(20)

p_quem = tf3_left.add_paragraph()
p_quem.text = "QUEM SOFRE O ERRO:"
p_quem.font.name = FONT_FAMILY
p_quem.font.size = Pt(11)
p_quem.font.bold = True
p_quem.font.color.rgb = ALERT_RED

p_quem_txt = tf3_left.add_paragraph()
p_quem_txt.text = "O trabalhador na parada: confia no app, espera o ônibus que não vem e perde o turno da fábrica."
p_quem_txt.font.name = FONT_FAMILY
p_quem_txt.font.size = Pt(14)
p_quem_txt.font.color.rgb = TEXT_MAIN


# Coluna 2: O Certo (GPS Real) e a Proteção
tb3_right = s3.shapes.add_textbox(Inches(7.0), Inches(2.7), Inches(5.3), Inches(3.8))
tf3_right = tb3_right.text_frame
tf3_right.word_wrap = True
tf3_right.margin_top = tf3_right.margin_bottom = tf3_right.margin_left = tf3_right.margin_right = 0

p_r = tf3_right.paragraphs[0]
p_r.text = "O CERTO (REALIDADE DO GPS)"
p_r.font.name = FONT_FAMILY
p_r.font.size = Pt(11)
p_r.font.bold = True
p_r.font.color.rgb = ACCENT_GREEN
p_r.space_after = Pt(12)

p_cor = tf3_right.add_paragraph()
p_cor.text = "45 minutos"
p_cor.font.name = FONT_FAMILY
p_cor.font.size = Pt(44)
p_cor.font.bold = True
p_cor.font.color.rgb = ACCENT_GREEN

p_cor_txt = tf3_right.add_paragraph()
p_cor_txt.text = "O ônibus travou totalmente no bloqueio do Trevo de Ipojuca (PE-60 / Nó 10)."
p_cor_txt.font.name = FONT_FAMILY
p_cor_txt.font.size = Pt(14)
p_cor_txt.font.color.rgb = TEXT_MAIN
p_cor_txt.space_after = Pt(20)

p_prot = tf3_right.add_paragraph()
p_prot.text = "A PROTEÇÃO ADOTADA:"
p_prot.font.name = FONT_FAMILY
p_prot.font.size = Pt(11)
p_prot.font.bold = True
p_prot.font.color.rgb = ACCENT_BLUE

p_prot_txt = tf3_right.add_paragraph()
p_prot_txt.text = "Trava híbrida: se |STGCN - GPS| > 15 min, corta a IA e acende alerta de interdição [?] na tela."
p_prot_txt.font.name = FONT_FAMILY
p_prot_txt.font.size = Pt(14)
p_prot_txt.font.color.rgb = TEXT_MAIN


# ==============================================================================
# SLIDE 4: O QUE MUDOU DESDE O SEM1 (DUAS LINHAS CLARAS)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "04 / O Que Mudou desde o Sem1", 
           "Decisão Justificada: Por Que Mantivemos a STGCN", 
           "O que valia no sem1, o que vale agora e o porquê comprovado na malha.")
add_footer(s4, 4)

tb4 = s4.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.333), Inches(3.8))
tf4 = tb4.text_frame
tf4.word_wrap = True
tf4.margin_top = tf4.margin_bottom = tf4.margin_left = tf4.margin_right = 0

# Linha 1: Sem 1
p1_tag = tf4.paragraphs[0]
p1_tag.text = "NO SEM1 (CORREDOR CURTO · 5 PARADAS):"
p1_tag.font.name = FONT_FAMILY
p1_tag.font.size = Pt(12)
p1_tag.font.bold = True
p1_tag.font.color.rgb = TEXT_MUTED

p1_main = tf4.add_paragraph()
p1_main.text = "O cálculo linear simples bateu a STGCN (2,46 min vs 4,42 min)."
p1_main.font.name = FONT_FAMILY
p1_main.font.size = Pt(22)
p1_main.font.bold = True
p1_main.font.color.rgb = TEXT_MAIN

p1_sub = tf4.add_paragraph()
p1_sub.text = "Dúvida legítima da banca: 'Para que usar rede em grafo se a conta simples ganha?'"
p1_sub.font.name = FONT_FAMILY
p1_sub.font.size = Pt(14)
p1_sub.font.color.rgb = TEXT_MUTED
p1_sub.space_after = Pt(36)

# Linha 2: Sem 2
p2_tag = tf4.add_paragraph()
p2_tag.text = "AGORA NO SEM2 (MALHA COMPLETA DA PE-60 · 20 PARADAS):"
p2_tag.font.name = FONT_FAMILY
p2_tag.font.size = Pt(12)
p2_tag.font.bold = True
p2_tag.font.color.rgb = ACCENT_BLUE

p2_main = tf4.add_paragraph()
p2_main.text = "A STGCN virou o jogo: erro caiu para 1,51 min (contra 1,93 min da linear e 7,13 min da persistência)."
p2_main.font.name = FONT_FAMILY
p2_main.font.size = Pt(22)
p2_main.font.bold = True
p2_main.font.color.rgb = ACCENT_BLUE

p2_sub = tf4.add_paragraph()
p2_sub.text = "Decisão: Fica a STGCN. Na malha rodoviária real, a propagação espacial de atrasos justifica a IA (-78% de erro)."
p2_sub.font.name = FONT_FAMILY
p2_sub.font.size = Pt(14)
p2_sub.font.color.rgb = TEXT_MAIN


# ==============================================================================
# SLIDE 5: O FECHO (PONTE DIRETA PARA O SEM3)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "05 / Fecho & Próximo Passo", 
           "A Falha de Hoje É a Medida do Experimento", 
           "Seminário 3 (25/11): Experimento formal e medidas de campo na PE-60.")
add_footer(s5, 5)

tb5 = s5.shapes.add_textbox(Inches(1.0), Inches(2.7), Inches(11.333), Inches(3.8))
tf5 = tb5.text_frame
tf5.word_wrap = True
tf5.margin_top = tf5.margin_bottom = tf5.margin_left = tf5.margin_right = 0

p5_tag = tf5.paragraphs[0]
p5_tag.text = "O FECHO DO SEM2:"
p5_tag.font.name = FONT_FAMILY
p5_tag.font.size = Pt(12)
p5_tag.font.bold = True
p5_tag.font.color.rgb = ACCENT_BLUE

p5_main = tf5.add_paragraph()
p5_main.text = "Roda no celular e na CPU local a custo zero, e a falha de over-smoothing é blindada pela regra."
p5_main.font.name = FONT_FAMILY
p5_main.font.size = Pt(22)
p5_main.font.bold = True
p5_main.font.color.rgb = TEXT_MAIN
p5_main.space_after = Pt(36)

p5_exp_tag = tf5.add_paragraph()
p5_exp_tag.text = "A MEDIDA DO SEM3 (25/11):"
p5_exp_tag.font.name = FONT_FAMILY
p5_exp_tag.font.size = Pt(12)
p5_exp_tag.font.bold = True
p5_exp_tag.font.color.rgb = ACCENT_BLUE

p5_exp_main = tf5.add_paragraph()
p5_exp_main.text = "Quantos choques de trânsito na PE-60 a trava híbrida consegue capturar contra o erro puro da IA."
p5_exp_main.font.name = FONT_FAMILY
p5_exp_main.font.size = Pt(20)
p5_exp_main.font.bold = False
p5_exp_main.font.color.rgb = TEXT_MAIN
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
