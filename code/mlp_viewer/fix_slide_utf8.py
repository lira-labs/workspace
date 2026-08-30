# -*- coding: utf-8 -*-
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

pptx_path = r"D:\workspace\code\mlp_viewer\docs\AI4Good - Pratica - MLP.pptx"
downloads_path = r"C:\Users\conta\Downloads\AI4Good - Pratica - MLP_Apresentacao.pptx"

prs = Presentation(pptx_path)

# Mantem apenas os 48 slides originais antes de criar o 49 limpo
while len(prs.slides) > 48:
    rId = prs.slides._sldIdLst[-1].rId
    prs.part.drop_rel(rId)
    del prs.slides._sldIdLst[-1]

blank_layout = prs.slide_layouts[6]
new_slide = prs.slides.add_slide(blank_layout)

for shape in list(new_slide.shapes):
    sp = shape._element
    new_slide.shapes._spTree.remove(sp)

# 1. Caixa de Título (com UTF-8 explícito)
title_box = new_slide.shapes.add_textbox(Inches(0.6), Inches(0.5), Inches(8.5), Inches(0.7))
tf_title = title_box.text_frame
tf_title.word_wrap = True
p_title = tf_title.paragraphs[0]
p_title.text = "0.885 : Cauã Lira"
p_title.font.size = Pt(28)
p_title.font.bold = True
p_title.font.color.rgb = RGBColor(0, 0, 0)

# 2. Caixa de Conteúdo (com UTF-8 explícito)
content_box = new_slide.shapes.add_textbox(Inches(0.6), Inches(1.35), Inches(5.8), Inches(4.5))
tf_content = content_box.text_frame
tf_content.word_wrap = True

lines = [
    "accuracy: 0.885",
    "learning rate: 0.01",
    "activation: relu",
    "architecture: 13 | 8 | 5 | 1",
    "pre-processing: standardize",
    "",
    "comentários: A padronização (standardize) garantiu estabilidade dos gradientes. Identificamos que o dataset heart.csv (1025 linhas) possui 70.5% de duplicatas (302 pacientes únicos); sem desduplicação ocorre data leakage inflando a acurácia para >95%. Com treino rigoroso e regularização, a convergência real se consolida em 88.5%."
]

for idx, line_text in enumerate(lines):
    if idx == 0:
        p = tf_content.paragraphs[0]
    else:
        p = tf_content.add_paragraph()
    p.text = line_text
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(30, 30, 30)

prs.save(pptx_path)
prs.save(downloads_path)
print("[+] Arquivo salvo com sucesso como 'AI4Good - Pratica - MLP_Apresentacao.pptx'!")
