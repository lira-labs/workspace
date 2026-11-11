# -*- coding: utf-8 -*-
"""
Gerador de Apresentação PowerPoint Profissional (Canva/Keynote Style)
Seminário 2 (AI4Good · UFRPE) · Iteração 2, Demonstração
Projeto: GrafoParada · Mobilidade Inteligente na PE-60
Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)
"""

import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. Inicialização da Apresentação 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Paleta de Cores Canva / Editorial
BG_DARK = RGBColor(10, 15, 29)          # Deep Navy/Slate #0A0F1D
CARD_BG = RGBColor(17, 24, 39)          # Dark Slate #111827
CARD_BORDER = RGBColor(31, 41, 55)      # Slate Border #1F2937
ACCENT_BLUE = RGBColor(2, 132, 199)     # Sky Blue #0284C7
ACCENT_CYAN = RGBColor(56, 189, 248)    # Light Sky #38BDF8
EMERALD = RGBColor(16, 185, 129)        # Emerald Green #10B981
DANGER_RED = RGBColor(244, 63, 94)      # Rose/Red #F43F5E
AMBER = RGBColor(245, 158, 11)          # Amber #F59E0B
TEXT_WHITE = RGBColor(248, 250, 252)    # Slate 50 #F8FAFC
TEXT_MUTED = RGBColor(148, 163, 184)    # Slate 400 #94A3B8
TEXT_LIGHT = RGBColor(226, 232, 240)    # Slate 200 #E2E8F0

def add_base_slide(tag_text, tag_color, title_text, subtitle_text, slide_num):
    """Cria a base editorial de um slide com tag, título e subtítulo."""
    slide = prs.slides.add_slide(blank_layout)
    
    # Fundo Sólido Dark Navy
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_DARK
    bg.line.fill.background()

    # Tag Superior em Pílula
    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = "Segoe UI"
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = tag_color

    # Título Principal Editorial
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.75))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    # Subtítulo Descritivo
    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.45), Inches(11.7), Inches(0.35))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(12)
    p_sub.font.color.rgb = TEXT_MUTED

    # Rodapé Editorial Humanizado
    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.7), Inches(0.35))
    tf_foot = foot_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = f"Cauã da Cunha Lira · AI4Good (UFRPE) | Prof. Lucas Silva Figueiredo | Slide {slide_num} de 5"
    p_foot.font.name = "Segoe UI"
    p_foot.font.size = Pt(9.5)
    p_foot.font.color.rgb = TEXT_MUTED

    return slide

# ==============================================================================
# SLIDE 1: PONTA A PONTA, AO VIVO (DEMONSTRAÇÃO REAL · 80 S)
# ==============================================================================
slide1 = add_base_slide(
    tag_text="Slide 1 · Ponta a Ponta, ao Vivo · 80 Segundos",
    tag_color=EMERALD,
    title_text="A Rotina dos Passageiros Orientando a Realocação da Frota no Vazio",
    subtitle_text="Demo ao vivo: grafoparadaweb.vercel.app · Commit 565321f · Linha 199 (Camela ➔ TI Cabo)",
    slide_num=1
)

# Coluna Esquerda: 3 Destaques Humanos e Operacionais
left_w = Inches(7.6)
top_y = Inches(1.95)

# Card 1.1: O Usuário Concreto & A Entrada Real
card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y, left_w, Inches(1.4))
card1.fill.solid()
card1.fill.fore_color.rgb = CARD_BG
card1.line.color.rgb = EMERALD
card1.line.width = Pt(1.5)

tb1 = slide1.shapes.add_textbox(Inches(1.0), top_y + Inches(0.12), left_w - Inches(0.4), Inches(1.15))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "1. O USUÁRIO CONCRETO & A ENTRADA REAL"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = EMERALD

p = tf1.add_paragraph()
p.text = "Trabalhador em Camela às 06h10 com destino ao TI Cabo / Complexo Suape."
p.font.name = "Segoe UI"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p = tf1.add_paragraph()
p.text = "• 1 toque no card 'Minha Rotina': Turno Suape 05h45. O app calcula a Janela Segura de Saída (saia às 06h08) baseada na caminhada de 6 min até a parada, evitando exposição no acostamento escuro."
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.color.rgb = TEXT_LIGHT

# Card 1.2: A Saída na Tela e no Fone (Acessibilidade Universal)
card2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y + Inches(1.55), left_w, Inches(1.4))
card2.fill.solid()
card2.fill.fore_color.rgb = CARD_BG
card2.line.color.rgb = CARD_BORDER
card2.line.width = Pt(1)

tb2 = slide1.shapes.add_textbox(Inches(1.0), top_y + Inches(1.67), left_w - Inches(0.4), Inches(1.15))
tf2 = tb2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "2. A SAÍDA NA TELA E NO FONE (ACESSIBILIDADE REAL)"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT_CYAN

p = tf2.add_paragraph()
p.text = "Previsão exata: Linha 199 chega em 4 min (06:14) · Plataforma 04 · Com Ar."
p.font.name = "Segoe UI"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p = tf2.add_paragraph()
p.text = "• Para idosos (Dona Severina, 68 anos): Letreiro LED âmbar idêntico ao coletivo + confirmação por voz em alto volume. Para estudantes noturnos: Modo Bolso Seguro (0 nits OLED) com vibração oculta."
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.color.rgb = TEXT_LIGHT

# Card 1.3: A Tese Central (Realocação da Frota no Vazio)
card3 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top_y + Inches(3.1), left_w, Inches(1.5))
card3.fill.solid()
card3.fill.fore_color.rgb = CARD_BG
card3.line.color.rgb = ACCENT_BLUE
card3.line.width = Pt(1.5)

tb3 = slide1.shapes.add_textbox(Inches(1.0), top_y + Inches(3.22), left_w - Inches(0.4), Inches(1.25))
tf3 = tb3.text_frame
tf3.word_wrap = True
p = tf3.paragraphs[0]
p.text = "3. A TESE CENTRAL: REALOCAÇÃO DA FROTA NO VAZIO (DEADHEADING MITIGATION)"
p.font.name = "Segoe UI"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = ACCENT_BLUE

p = tf3.add_paragraph()
p.text = "48 trabalhadores cadastrados alimentam a demanda agregada na Central CTM."
p.font.name = "Segoe UI"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = TEXT_WHITE

p = tf3.add_paragraph()
p.text = "• O CTM detecta que a Linha 178 Suape roda no vazio (3 passageiros, queima 14 L/h de diesel) e desvia o veículo ocioso para reforçar a Linha 199. A espera em Camela cai de 18 para 4 minutos!"
p.font.name = "Segoe UI"
p.font.size = Pt(10.5)
p.font.color.rgb = TEXT_LIGHT

# Coluna Direita: Imagem do Mockup Realista de Smartphone
mockup_path = "va2/img/mockup_app_sem2.png"
if os.path.exists(mockup_path):
    slide1.shapes.add_picture(mockup_path, Inches(9.0), Inches(1.85), width=Inches(3.45))

# ==============================================================================
# SLIDE 2: QUANTO CUSTA, MEDIDO VS FLX (O CUSTO · 50 S)
# ==============================================================================
slide2 = add_base_slide(
    tag_text="Slide 2 · Quanto Custa · Medido vs flx · 50 Segundos",
    tag_color=ACCENT_BLUE,
    title_text="Inferência em Menos de 1 ms e Custo Zero de Infraestrutura",
    subtitle_text="Medição real no repositório com medir_custo_sem2.py · Intel Core CPU · Windows 11 · PyTorch",
    slide_num=2
)

# Imagem Central do Card de Custo em Alta Fidelidade
cost_img_path = "va2/img/card_custo_medido.png"
if os.path.exists(cost_img_path):
    slide2.shapes.add_picture(cost_img_path, Inches(0.8), Inches(1.85), width=Inches(11.733))

# ==============================================================================
# SLIDE 3: A FALHA MOSTRADA DE PROPÓSITO (A FALHA REAL · 65 S)
# ==============================================================================
slide3 = add_base_slide(
    tag_text="Slide 3 · A Falha Mostrada de Propósito · 65 Segundos",
    tag_color=DANGER_RED,
    title_text="Onde a Rede Neural Mente: Super-Suavização no Bloqueio da PE-60",
    subtitle_text="Simulação real no Trevo de Ipojuca (Km 14) · Botão interativo de simulação no app",
    slide_num=3
)

# Imagem Central do Gráfico de Over-smoothing
fail_img_path = "va2/img/grafico_falha_oversmoothing.png"
if os.path.exists(fail_img_path):
    slide3.shapes.add_picture(fail_img_path, Inches(0.8), Inches(1.85), width=Inches(11.733))

# ==============================================================================
# SLIDE 4: O QUE MUDOU DESDE O SEM1 (A EVOLUÇÃO · 50 S)
# ==============================================================================
slide4 = add_base_slide(
    tag_text="Slide 4 · O que Mudou desde o Sem1 · 50 Segundos",
    tag_color=ACCENT_CYAN,
    title_text="De 5 para 20 Paradas: A STGCN Virou o Jogo e Provou seu Custo",
    subtitle_text="Validação empírica com 43 paradas e dados de telemetria do GTFS do Grande Recife",
    slide_num=4
)

# Imagem Central do Gráfico MAE e Evolução
mae_img_path = "va2/img/grafico_evolucao_mae.png"
if os.path.exists(mae_img_path):
    slide4.shapes.add_picture(mae_img_path, Inches(0.8), Inches(1.85), width=Inches(11.733))

# ==============================================================================
# SLIDE 5: O FECHO & EXPERIMENTO DO SEM3 (O FECHO · 20 S)
# ==============================================================================
slide5 = add_base_slide(
    tag_text="Slide 5 · Fecho & Experimento de Campo · 20 Segundos",
    tag_color=EMERALD,
    title_text="A Desistência na Parada Financia o Ônibus no Horário de Pico",
    subtitle_text="No dia 25/11 (Sem3): Validação de campo na PE-60 com passageiros reais testando a trava híbrida",
    slide_num=5
)

# Imagem Central do Card de Balanço e Pilares
balanco_img_path = "va2/img/card_realocacao_ctm.png"
if os.path.exists(balanco_img_path):
    slide5.shapes.add_picture(balanco_img_path, Inches(0.8), Inches(1.85), width=Inches(11.733))

# Salvamento Final
output_path = Path("va2/GrafoParada_Seminario2_CauaLira.pptx")
prs.save(output_path)
print(f"[SUCESSO] Apresentação Canva-Style salva em: {output_path} ({output_path.stat().st_size:,} bytes)!")
