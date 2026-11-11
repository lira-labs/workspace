# -*- coding: utf-8 -*-
"""
Gerador de Slides PowerPoint (PPTX) · Seminário 2 (AI4Good / UFRPE)
GrafoParada · Demonstração e Falha Real · Cauã da Cunha Lira
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

DARK_BG = RGBColor(9, 13, 22)
CARD_BG = RGBColor(17, 24, 39)
BORDER_COLOR = RGBColor(31, 41, 55)
TEXT_WHITE = RGBColor(248, 250, 252)
TEXT_MUTED = RGBColor(148, 163, 184)
ACCENT_BLUE = RGBColor(56, 189, 248)
GREEN = RGBColor(16, 185, 129)
DANGER = RGBColor(244, 63, 94)
WARN = RGBColor(245, 158, 11)

slides_data = [
    {
        "tag": "SLIDE 1 · PONTA A PONTA AO VIVO · 80 S",
        "title": "Rotina mapeada em 1 toque, voz no fone e realocação da frota no vazio",
        "subtitle": "Demo ao vivo: grafoparadaweb.vercel.app · Commit 565321f",
        "cards": [
            ("1. ENTRADA & ROTINA PENDULAR", "📅 Rotina · 05h45", "Janela de Saída segura (saia às 06h08). Farol Noturno anti-queima de 76px e Modo Offline Inercial na PE-60.", GREEN),
            ("2. SAÍDA NA TELA E NO FONE", "4 min · Plat. 04", "Letreiro LED idêntico ao ônibus, confirmação sonora para idosos (Dona Severina) ou Modo Bolso 0 nits para estudantes.", TEXT_WHITE),
            ("3. REALOCAÇÃO CTM & VEM", "Frota 178 ➔ 199", "Central CTM remaneja ônibus vazio da Linha 178 (poupa 14 L/h de diesel) para socorrer 48 passageiros de Camela com VEM protegido.", ACCENT_BLUE)
        ]
    },
    {
        "tag": "SLIDE 2 · QUANTO CUSTA · MEDIDO VS FLX · 50 S",
        "title": "Tempo e memória medidos no repositório com medir_custo_sem2.py",
        "subtitle": "Execução real no Desktop/Notebook Windows com Python 3.12 + PyTorch",
        "cards": [
            ("NO CELULAR (FSM CINEMÁTICA V3)", "4,98 ms · 12 KB", "flx estimava 14,29 µs (passo simples) e 8,92 KB de RAM. Soft-Voting + cinemática rodam em < 5 ms. Zero impacto de bateria.", GREEN),
            ("NO SERVIDOR (STGCN 20 NÓS PE-60)", "0,77 ms · 84 KB", "flx estimava < 500 ms e ~300 MB. Inferência pura na CPU é instantânea. O processo total do PyTorch consome 358 MB.", ACCENT_BLUE),
            ("CUSTO FINANCEIRO NA ESCALA", "R$ 0,00", "34.627 parâmetros. Roda em computador comum de escritório do consórcio CTM, sem gastar nada com nuvem paga.", GREEN)
        ]
    },
    {
        "tag": "SLIDE 3 · A FALHA MOSTRADA DE PROPÓSITO · 65 S",
        "title": "Bloqueio no Trevo de Ipojuca: a STGCN espalha e suaviza o atraso",
        "subtitle": "Demonstração da falha ao vivo no app pelo botão 'Simular Interdição PE-60'",
        "cards": [
            ("A ENTRADA REAL (GPS BRUTO)", "45 min", "Ônibus travou no bloqueio da rodovia PE-60. O atraso medido no satélite salta bruscamente de 5 para 45 minutos.", DANGER),
            ("A SAÍDA DA IA (COMO SAIU)", "18 min [?]", "Convolução espacial difunde o choque para as paradas vizinhas. Previsão mente dizendo que o ônibus tá perto.", WARN),
            ("QUEM SOFRE & O QUE REVELA", "O Trabalhador", "Operário perde o turno em Suape. Revela over-smoothing. Solução: selo de alerta [?] quando STGCN difere > 15 min do GPS.", TEXT_WHITE)
        ]
    },
    {
        "tag": "SLIDE 4 · O QUE MUDOU DESDE O SEM1 · 50 S",
        "title": "De 5 para 20 paradas: STGCN comprovada e foco na rotina e inclusão",
        "subtitle": "Confirmação empírica de modelo profundo quando a rede e os dados escalam",
        "cards": [
            ("NO SEM1 (CORREDOR CURTO 5 PARADAS)", "2,46 vs 4,42 min", "Cálculo simples superou a STGCN. Promessa feita à banca de testar se a IA se justificava na malha maior.", TEXT_MUTED),
            ("AGORA NO SEM2 (MALHA REAL 20 PARADAS)", "1,51 vs 1,93 min", "STGCN virou o jogo e venceu a regressão linear (1,51 vs 1,93 min) e reduziu 78% do erro contra persistência (7,13 min).", GREEN),
            ("DO RASTREADOR À REALOCAÇÃO", "Rotina & Inclusão", "Rotina dos trabalhadores orienta o despacho da frota ociosa. Acessibilidade com Letreiro LED para idosos e Modo Bolso para jovens.", ACCENT_BLUE)
        ]
    },
    {
        "tag": "SLIDE 5 · FECHO · 20 S",
        "title": "A desistência na parada financia o ônibus no horário de pico",
        "subtitle": "No dia 25/11 (Sem3): validação experimental de campo com passageiros reais na PE-60",
        "cards": [
            ("NO APARELHO DO USUÁRIO", "Privado & Seguro", "Rotina gravada no celular (166 bytes). Alerta calmo por voz no fone. Tela preta anti-assalto. Zero rastreamento externo.", GREEN),
            ("NO CONSÓRCIO GRANDE RECIFE", "14 L · R$ 155 · R$ 4,10", "Poupa 14 L de diesel por viagem ociosa evitada, preserva R$ 155 contra ligeirinhos e protege o débito indevido do VEM.", ACCENT_BLUE),
            ("EXPERIMENTO DO SEMINÁRIO 3", "25 de Novembro", "Medição de campo com passageiros reais na PE-60 testando o escudo de regra contra o over-smoothing da STGCN.", TEXT_WHITE)
        ]
    }
]

for idx, sdata in enumerate(slides_data, start=1):
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = DARK_BG
    bg.line.fill.background()

    tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.7), Inches(0.4))
    tf_tag = tag_box.text_frame
    tf_tag.word_wrap = True
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = sdata["tag"]
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_BLUE

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.0), Inches(11.7), Inches(1.0))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = sdata["title"]
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(0.4))
    tf_sub = sub_box.text_frame
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = sdata["subtitle"]
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED

    card_w = Inches(3.65)
    card_h = Inches(3.8)
    card_gap = Inches(0.38)
    left_start = Inches(0.8)
    top_pos = Inches(2.55)

    for c_idx, (c_title, c_val, c_desc, val_color) in enumerate(sdata["cards"]):
        c_left = left_start + c_idx * (card_w + card_gap)
        c_shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_left, top_pos, card_w, card_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = CARD_BG
        c_shape.line.color.rgb = BORDER_COLOR
        c_shape.line.width = Pt(1.5)

        c_tb = slide.shapes.add_textbox(c_left + Inches(0.2), top_pos + Inches(0.2), card_w - Inches(0.4), card_h - Inches(0.4))
        tf = c_tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = c_title
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_MUTED
        p1.space_after = Pt(14)

        p2 = tf.add_paragraph()
        p2.text = c_val
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = val_color
        p2.space_after = Pt(14)

        p3 = tf.add_paragraph()
        p3.text = c_desc
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_MUTED

    foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.75), Inches(11.7), Inches(0.4))
    tf_foot = foot_box.text_frame
    p_foot = tf_foot.paragraphs[0]
    p_foot.text = f"Cauã da Cunha Lira · Tópicos Avançados em IA (AI4Good · UFRPE) | Slide {idx} de 5"
    p_foot.font.size = Pt(10)
    p_foot.font.color.rgb = TEXT_MUTED

output_path = Path("va2/GrafoParada_Seminario2_CauaLira.pptx")
prs.save(output_path)
print(f"[OK] Apresentação salva com sucesso em: {output_path} ({output_path.stat().st_size:,} bytes)!")
