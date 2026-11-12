# -*- coding: utf-8 -*-
"""
Gerador de Slides Minimalista Brutalista / Suíço (Anti-AI-Slop)
Padrão: Fundo Branco Puro (#FFFFFF), Tipografia Robusta, Regra dos Terços, Números Gigantes, >50% Whitespace.
Sem ícones decorativos em círculos, sem gradientes vazios, sem cartões escuros de neon.

Seminário 2 (AI4Good · UFRPE) · Cauã da Cunha Lira
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. Configuração Widescreen 16:9
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# 2. Paleta Minimalista Editorial (Base Clara)
BG_WHITE = RGBColor(255, 255, 255)      # Fundo Branco Puro #FFFFFF
TEXT_BLACK = RGBColor(10, 10, 10)       # Preto Quase Puro #0A0A0A (Alto Contraste)
TEXT_DARK = RGBColor(55, 65, 81)        # Cinza Chumbo #374151
TEXT_MUTED = RGBColor(107, 114, 128)    # Cinza Médio #6B7280
TEXT_LIGHT = RGBColor(156, 163, 175)    # Cinza Claro de Rodapé #9CA3AF
LINE_BORDER = RGBColor(229, 231, 235)   # Linha Discreta #E5E7EB

# Cores de Sotaque Estritas (Usadas Apenas em Números e Palavras-Chave)
KLEIN_BLUE = RGBColor(0, 47, 167)       # Azul Klein Clássico #002FA7
BOTTEGA_GREEN = RGBColor(0, 135, 81)    # Verde Bottega #008751
CRIMSON_RED = RGBColor(192, 0, 0)       # Carmim / Vermelho Sóbrio de Erro #C00000

FONT_FAMILY = "Segoe UI"

def create_slide_base(prs, tag_text, tag_color, title_text, subtitle_text, slide_index):
    """Cria a base minimalista suíça do slide."""
    slide = prs.slides.add_slide(blank_layout)

    # Fundo Branco Puro
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_WHITE
    bg.line.fill.background()

    # Linha Superior Discreta de Separação
    rule_top = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.48), Inches(11.533), Inches(0.015))
    rule_top.fill.solid()
    rule_top.fill.fore_color.rgb = LINE_BORDER
    rule_top.line.fill.background()

    # Tag Monospace / Editorial
    tag_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.58), Inches(11.533), Inches(0.35))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_FAMILY
    p_tag.font.size = Pt(10.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = tag_color

    # Título Principal (40pt a 44pt, Bold, Preto Quase Puro)
    title_box = slide.shapes.add_textbox(Inches(0.9), Inches(0.92), Inches(11.533), Inches(0.85))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(36)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_BLACK

    # Subtítulo (16pt a 18pt, Regular, Cinza Escuro)
    sub_box = slide.shapes.add_textbox(Inches(0.9), Inches(1.82), Inches(11.533), Inches(0.45))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = subtitle_text
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(15.5)
    p_sub.font.color.rgb = TEXT_DARK

    # Rodapé Discreto
    rule_bot = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(6.82), Inches(11.533), Inches(0.015))
    rule_bot.fill.solid()
    rule_bot.fill.fore_color.rgb = LINE_BORDER
    rule_bot.line.fill.background()

    foot_box = slide.shapes.add_textbox(Inches(0.9), Inches(6.9), Inches(11.533), Inches(0.35))
    tf_foot = foot_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = f"AI4Good (UFRPE) · Prof. Lucas Silva Figueiredo | Cauã da Cunha Lira · Slide {slide_index} de 5"
    p_foot.font.name = FONT_FAMILY
    p_foot.font.size = Pt(9.5)
    p_foot.font.color.rgb = TEXT_MUTED

    return slide

# ==============================================================================
# SLIDE 1: ABERTURA & DEMO AO VIVO (REGRA DOS TERÇOS)
# ==============================================================================
slide1 = create_slide_base(
    prs=prs,
    tag_text="01 / DEMONSTRAÇÃO AO VIVO · LINHA 199 (CAMELA ➔ TI CABO) · KIM ET AL. (2026)",
    tag_color=KLEIN_BLUE,
    title_text="A janela pessoal de saída elimina a espera e o abandono.",
    subtitle_text="Da Rodovia PE-60 (Linha 199 Suape) às 400 linhas GTFS com Laya IA · Mitigando Balking e Reneging (Kim et al., 2026).",
    slide_index=1
)

# 3 Colunas Limpas (Regra dos Terços)
col_w = Inches(3.6)
col_gap = Inches(0.36)
col_top = Inches(2.55)

cols_s1 = [
    {
        "tag": "O USUÁRIO REAL & CENSURA VEM",
        "tag_color": TEXT_MUTED,
        "hero": "Trabalhador às 06h10",
        "hero_color": TEXT_BLACK,
        "sub": "Turno Suape 05h45",
        "body": "Morador de Camela em direção ao polo. Janela calculada: saia às 06h08 (caminhada 6 min). A bilhetagem eletrônica sofre de censura à direita: quem desiste na escuridão nunca passa na catraca."
    },
    {
        "tag": "ACESSIBILIDADE & LAYA IA",
        "tag_color": TEXT_MUTED,
        "hero": "Laya IA & Voz pt-BR",
        "hero_color": TEXT_BLACK,
        "sub": "Voz Acolhedora & Favoritos",
        "body": "Comandos de voz interativos ('quando passa meu ônibus?'), onboarding guiado em 3 passos, favoritos (Casa/UFRPE) e Modo Bolso Seguro (0 nits OLED) com vibração tátil."
    },
    {
        "tag": "A TESE CENTRAL",
        "tag_color": KLEIN_BLUE,
        "hero": "48 Trabalhadores",
        "hero_color": KLEIN_BLUE,
        "sub": "Despacho da Frota no Vazio",
        "body": "Demanda latente capturada alimenta a Central CTM: ônibus da Linha 178 no vazio (deadheading) é remanejado para a 199. A espera cai de 18 para 4 min e elimina o abandono."
    }
]

for idx, col in enumerate(cols_s1):
    c_left = Inches(0.9) + idx * (col_w + col_gap)

    # Linha discreta de cabeçalho de coluna
    rule = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, col_top, Inches(0.8), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = col["tag_color"]
    rule.line.fill.background()

    tb = slide1.shapes.add_textbox(c_left, col_top + Inches(0.12), col_w, Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = col["tag"]
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = col["tag_color"]
    p.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = col["hero"]
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(21)
    p2.font.bold = True
    p2.font.color.rgb = col["hero_color"]

    p3 = tf.add_paragraph()
    p3.text = col["sub"]
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(12.5)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_DARK
    p3.space_after = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = col["body"]
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK

# ==============================================================================
# SLIDE 2: O CUSTO (MEDIDO VS FLX.MD) · 3 NÚMEROS GIGANTES
# ==============================================================================
slide2 = create_slide_base(
    prs=prs,
    tag_text="02 / EFICIÊNCIA DE RUNTIME · MEDIÇÃO NO REPOSITÓRIO (0,77 MS)",
    tag_color=KLEIN_BLUE,
    title_text="A inferência em CPU foi 600× mais rápida e opera a custo zero.",
    subtitle_text="Medição empírica no repositório (0,77 ms na CPU e 4,98 ms on-device) comprova soberania pública sem APIs pagas.",
    slide_index=2
)

cols_s2 = [
    {
        "tag": "NO APARELHO (CELULAR)",
        "number": "4,98 ms",
        "num_color": KLEIN_BLUE,
        "sub": "12,0 KB de Memória RAM",
        "body": "FSM cinemática v3 com Soft-Voting em tempo real. Execução instantânea com zero dreno de bateria.\n\nflx estimava: 14,29 µs (passo de rotina) e 8,92 KB de RAM."
    },
    {
        "tag": "NO SERVIDOR LOCAL (CTM)",
        "number": "0,77 ms",
        "num_color": KLEIN_BLUE,
        "sub": "358 MB no Processo",
        "body": "Inferência pura da STGCN em 20 nós da PE-60. Tensores ativos consom apenas 84 KB.\n\nflx estimava: < 500 ms e ~300 MB. A diferença: o PyTorch segura as libs dinâmicas no SO."
    },
    {
        "tag": "CUSTO FINANCEIRO TOTAL",
        "number": "R$ 0,00",
        "num_color": BOTTEGA_GREEN,
        "sub": "34.627 Parâmetros",
        "body": "Roda em computador comum de escritório do consórcio CTM.\n\nZero dependência de APIs pagas em dólar, sem servidores caros em nuvem e 100% soberano."
    }
]

for idx, col in enumerate(cols_s2):
    c_left = Inches(0.9) + idx * (col_w + col_gap)

    rule = slide2.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, col_top, Inches(0.8), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = col["num_color"]
    rule.line.fill.background()

    tb = slide2.shapes.add_textbox(c_left, col_top + Inches(0.12), col_w, Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = col["tag"]
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = col["number"]
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(50)
    p2.font.bold = True
    p2.font.color.rgb = col["num_color"]

    p3 = tf.add_paragraph()
    p3.text = col["sub"]
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_BLACK
    p3.space_after = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = col["body"]
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK

# ==============================================================================
# SLIDE 3: A FALHA REAL · ONDE A REDE NEURAL MENTE (OVER-SMOOTHING)
# ==============================================================================
slide3 = create_slide_base(
    prs=prs,
    tag_text="03 / A FALHA REAL · YAP & CATS (2021) · PESO PSICOLÓGICO 1,68X",
    tag_color=CRIMSON_RED,
    title_text="A STGCN super-suaviza retenções; a trava híbrida corta a IA.",
    subtitle_text="GAP de 27 min na PE-60 aciona trava defensiva (|Δ| > 15 min), mitigando a penalidade de 1,68× da espera forçada.",
    slide_index=3
)

cols_s3 = [
    {
        "tag": "A SAÍDA DA IA (COMO SAIU)",
        "number": "18 min [?]",
        "num_color": CRIMSON_RED,
        "sub": "Previsão Atenuada e Falsa",
        "body": "A difusão Laplaciana dilui 45 min de retenção para 18 min falsos.\n\nAtraso não-anunciado acelera a desistência da espera (Passenger Reneging · Kim et al., 2026)."
    },
    {
        "tag": "O DADO BRUTO DO SATÉLITE",
        "number": "45 min",
        "num_color": TEXT_BLACK,
        "sub": "Penalidade Psicológica 1,68×",
        "body": "Yap & Cats (2021) provam: a espera forçada por queima ou bloqueio pesa 1,68× mais na desutilidade.\n\nQUEM SOFRE: O passageiro que perde o turno desiste do transporte público coletivo."
    },
    {
        "tag": "A SOLUÇÃO HÍBRIDA DO APP",
        "number": "Trava [?]",
        "num_color": KLEIN_BLUE,
        "sub": "Selo de Interdição na Tela",
        "body": "Se |STGCN - GPS| > 15 min, o GrafoParada corta a IA, acende o selo de interdição [?] e avisa por voz no fone que a via travou.\n\nProtegendo o cidadão contra a ilusão da IA."
    }
]

for idx, col in enumerate(cols_s3):
    c_left = Inches(0.9) + idx * (col_w + col_gap)

    rule = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, col_top, Inches(0.8), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = col["num_color"]
    rule.line.fill.background()

    tb = slide3.shapes.add_textbox(c_left, col_top + Inches(0.12), col_w, Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = col["tag"]
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = col["number"]
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(50)
    p2.font.bold = True
    p2.font.color.rgb = col["num_color"]

    p3 = tf.add_paragraph()
    p3.text = col["sub"]
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_BLACK
    p3.space_after = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = col["body"]
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK

# ==============================================================================
# SLIDE 4: O QUE MUDOU DESDE O SEM1 · DECISÃO TÉCNICA E ESCALA
# ==============================================================================
slide4 = create_slide_base(
    prs=prs,
    tag_text="04 / DECISÃO ARQUITETURAL · TOPOLOGIA ESPECTRAL CHEBYSHEV",
    tag_color=KLEIN_BLUE,
    title_text="Na malha expandida, o grafo bate baselines e reduz 78% do erro.",
    subtitle_text="De derrota em 5 paradas (Sem1) para vitória na PE-60 (MAE = 1,51 min), superando a colinearidade de 120 variáveis da OLS.",
    slide_index=4
)

cols_s4 = [
    {
        "tag": "SEM1 · CORREDOR CURTO (5 PARADAS)",
        "number": "2,46 min",
        "num_color": TEXT_MUTED,
        "sub": "Regressão Venceu a STGCN",
        "body": "No trecho simples de 5 paradas, uma conta básica deu 2,46 min contra 4,42 min da STGCN.\n\nDúvida honesta levada à banca: a complexidade da rede de grafos se justificava naquele escopo reduzido?"
    },
    {
        "tag": "SEM2 · MALHA DE 20 NÓS (PE-60)",
        "number": "1,51 min",
        "num_color": BOTTEGA_GREEN,
        "sub": "vs 1,93 min da Linear (OLS)",
        "body": "Na malha real da PE-60, a STGCN reduziu o erro em 78% (MAE 1,51 min vs 1,93 OLS vs 7,13 média).\n\nA OLS sofre forte colinearidade em 120 variáveis achatadas. A GNN preserva a topologia viária."
    },
    {
        "tag": "TRANSPARÊNCIA CIENTÍFICA",
        "number": "Topologia",
        "num_color": KLEIN_BLUE,
        "sub": "Invariância Espacial da Rede",
        "body": "Infraestrutura espacial e paradas são 100% reais do GTFS CTM oficial.\n\nA difusão Laplaciana modela a física da rodovia sem sofrer com a maldição da dimensionalidade tabular."
    }
]

for idx, col in enumerate(cols_s4):
    c_left = Inches(0.9) + idx * (col_w + col_gap)

    rule = slide4.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, col_top, Inches(0.8), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = col["num_color"]
    rule.line.fill.background()

    tb = slide4.shapes.add_textbox(c_left, col_top + Inches(0.12), col_w, Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = col["tag"]
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = col["number"]
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(44 if len(col["number"]) > 7 else 50)
    p2.font.bold = True
    p2.font.color.rgb = col["num_color"]

    p3 = tf.add_paragraph()
    p3.text = col["sub"]
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_BLACK
    p3.space_after = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = col["body"]
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK

# ==============================================================================
# SLIDE 5: O FECHO · IMPACTO REAL E PONTE PARA O SEMINÁRIO 3
# ==============================================================================
slide5 = create_slide_base(
    prs=prs,
    tag_text="05 / FECHO & CAMPO SEM3 · KIM ET AL. (2026) & YAP & CATS (2021)",
    tag_color=BOTTEGA_GREEN,
    title_text="A trava híbrida calibra o teste de campo contra o abandono.",
    subtitle_text="Validação na PE-60 ancorada em Kim et al. (2026) e Yap & Cats (2021): protegendo tarifa social, diesel e privacidade.",
    slide_index=5
)

cols_s5 = [
    {
        "tag": "COMBUSTÍVEL E DIESEL",
        "number": "14 L / h",
        "num_color": BOTTEGA_GREEN,
        "sub": "Diesel Poupado por Ciclo",
        "body": "Economia direta ao evitar que o veículo da Linha 178 circule vazio na contramão.\n\nR$ 155,80 de receita preservada ao mitigar o abandono (Passenger Reneging · Kim et al., 2026)."
    },
    {
        "tag": "BOLSO DO TRABALHADOR",
        "number": "R$ 4,10",
        "num_color": KLEIN_BLUE,
        "sub": "VEM com Janela Blindada",
        "body": "Guardião da integração temporal de 120 minutos no TI Cabo contra cobrança em duplicidade por queima.\n\nPrivacidade total: rotina do passageiro gravada no próprio aparelho em 166 bytes."
    },
    {
        "tag": "SEMINÁRIO 3 · 25/11",
        "number": "25 / 11",
        "num_color": TEXT_BLACK,
        "sub": "Validação de Campo na PE-60",
        "body": "A falha mostrada hoje (over-smoothing) vira a métrica de teste do Sem3:\n\nQuantas vezes a trava híbrida de discrepância protege o passageiro no ponto em Camela contra o peso de 1,68× do Denied Boarding."
    }
]

for idx, col in enumerate(cols_s5):
    c_left = Inches(0.9) + idx * (col_w + col_gap)

    rule = slide5.shapes.add_shape(MSO_SHAPE.RECTANGLE, c_left, col_top, Inches(0.8), Inches(0.04))
    rule.fill.solid()
    rule.fill.fore_color.rgb = col["num_color"]
    rule.line.fill.background()

    tb = slide5.shapes.add_textbox(c_left, col_top + Inches(0.12), col_w, Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = col["tag"]
    p.font.name = FONT_FAMILY
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(4)

    p2 = tf.add_paragraph()
    p2.text = col["number"]
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(50)
    p2.font.bold = True
    p2.font.color.rgb = col["num_color"]

    p3 = tf.add_paragraph()
    p3.text = col["sub"]
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = TEXT_BLACK
    p3.space_after = Pt(12)

    p4 = tf.add_paragraph()
    p4.text = col["body"]
    p4.font.name = FONT_FAMILY
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_DARK

# Salvamento Final
output_path = Path("va2/GrafoParada_Seminario2_CauaLira.pptx")
prs.save(output_path)
print(f"[SUCESSO] Apresentacao Minimalista Brutalista gerada com sucesso: {output_path} ({output_path.stat().st_size:,} bytes)!")
