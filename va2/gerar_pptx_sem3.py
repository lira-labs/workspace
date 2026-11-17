"""
Gera o deck oficial do Seminário 3 (`sem3`: Como vai ser o teste) em Widescreen 16:9.
Segue estritamente a norma Anti-AI-Slop e o guia do sem3:
- 5 slides (4 a 6 slides permitidos)
- 1 ideia por slide, ZERO parágrafos longos
- Diagrama limpo da comparação pareada, tabela PASSOU/CAIU/INCONCLUSIVO e calendário 18/11 -> 02/12
Salva em:
  1) va2/GrafoParada_Sem3_CauaLira.pptx
  2) code/grafoparada_web/GrafoParada_Sem3_CauaLira.pptx
  3) G:/Meu Drive/IA_Projetos/GrafoParada_Sem3_CauaLira.pptx (se o Drive existir)
"""
from __future__ import annotations

import shutil
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
OUT_VA2 = ROOT / "va2" / "GrafoParada_Sem3_CauaLira.pptx"
OUT_WEB = ROOT / "code" / "grafoparada_web" / "GrafoParada_Sem3_CauaLira.pptx"
DRIVE_DIR = Path(r"G:\Meu Drive\IA_Projetos")

BG = RGBColor(0xF8, 0xFA, 0xFC)
DARK = RGBColor(0x0F, 0x17, 0x2A)
MUTED = RGBColor(0x47, 0x55, 0x69)
GREEN = RGBColor(0x05, 0x96, 0x69)
GREEN_SOFT = RGBColor(0xEC, 0xFD, 0xF5)
RED = RGBColor(0xDC, 0x26, 0x26)
RED_SOFT = RGBColor(0xFE, 0xF2, 0xF2)
AMBER = RGBColor(0xD9, 0x77, 0x06)
AMBER_SOFT = RGBColor(0xFF, 0xFB, 0xEB)
BLUE = RGBColor(0x02, 0x84, 0xC7)
BLUE_SOFT = RGBColor(0xF0, 0xF9, 0xFF)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
BORDER = RGBColor(0xCB, 0xD5, 0xE1)


def set_bg(slide, color=BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, tag: str, title: str, subtitle: str):
    # Barra superior sutil
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GREEN
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.28), Inches(12.0), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    r0 = p0.add_run()
    r0.text = tag.upper()
    r0.font.size = Pt(11)
    r0.font.bold = True
    r0.font.color.rgb = GREEN

    p1 = tf.add_paragraph()
    p1.space_before = Pt(3)
    r1 = p1.add_run()
    r1.text = title
    r1.font.size = Pt(28)
    r1.font.bold = True
    r1.font.color.rgb = DARK

    p2 = tf.add_paragraph()
    p2.space_before = Pt(2)
    r2 = p2.add_run()
    r2.text = subtitle
    r2.font.size = Pt(14)
    r2.font.color.rgb = MUTED


def add_card(slide, left, top, width, height, fill_color=CARD, border_color=BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.adjustments[0] = 0.04
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.25)
    return shape


def add_lines(slide, left, top, width, height, lines: list[tuple[str, int, bool, RGBColor]], align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, (txt, size, bold, color) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(5)
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb


def add_footer(slide, page_num: int):
    add_lines(
        slide,
        0.65,
        7.05,
        12.0,
        0.35,
        [(f"GrafoParada · Seminário 3 (sem3 · 18/11/2026) · Slide {page_num}/5", 10.5, False, MUTED)],
    )


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # SLIDE 1: O COMPETIDOR E A LACUNA
    s1 = prs.slides.add_slide(blank)
    set_bg(s1)
    add_header(
        s1,
        "Slide 1 · O Competidor e o Que Ele Consegue",
        "Por que comparar C1, C2 e C3 nos mesmos cenários",
        "Falha do sem2 (Nó 10 PE-60): choque real de 45,0 min suavizado para 14,3 min sem aviso.",
    )

    cards_s1 = [
        ("C1 · Persistência (Hoje)", "7,13 min MAE (20 nós)\n97% sem aviso (5 nós)", "Olha só o atraso atual.\nSempre chega atrasado.", RED_SOFT, RED),
        ("C2 · Tabular Corredor", "1,93 min MAE (20 nós)\n2,46 min MAE (5 nós)", "Lags achatados sem grafo.\nForte em amostra pequena.", BLUE_SOFT, BLUE),
        ("C3 · ST-GCN Pura", "1,51 min MAE normal\n14,3 min no choque 45m", "Aprende difusão da via,\nmas suaviza pico súbito.", AMBER_SOFT, AMBER),
    ]
    for i, (t, metric, desc, bgc, fg) in enumerate(cards_s1):
        x = 0.65 + i * 4.1
        add_card(s1, x, 1.75, 3.85, 3.35, bgc, fg)
        add_lines(s1, x + 0.22, 1.95, 3.4, 3.0, [
            (t, 16, True, DARK),
            (metric, 20, True, fg),
            (desc, 13.5, False, MUTED),
        ])

    add_card(s1, 0.65, 5.35, 12.03, 1.45, CARD, BORDER)
    add_lines(s1, 0.9, 5.5, 11.5, 1.2, [
        ("Por que apps fechados (Cittamobi / Moovit) e datasets externos ficam fora da tabela principal:", 13.5, True, DARK),
        ("• Apps fechados não rodam nos mesmos cenários controlados. Fontes abertas (Horn et al., 2025; Mansurova et al., 2025; Niemann Tygesen et al., 2023) validam dados AVL e incidentes, sem benchmark publicado de FN > 40 min.", 12.5, False, MUTED),
    ])
    add_footer(s1, 1)

    # SLIDE 2: O QUE QUERO MOSTRAR + REGRA PRÉ-REGISTRADA
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_header(
        s2,
        "Slide 2 · O Alvo e a Regra Escrita Antes do Resultado",
        "Medir falha silenciosa (> 40 min), nunca 'nota de gosto'",
        "Trava Híbrida Defensiva [?]: dispara alerta quando |GPS cinemático (min) − ST-GCN| > 15,0 min.",
    )

    add_card(s2, 0.65, 1.7, 12.03, 1.45, BLUE_SOFT, BLUE)
    add_lines(s2, 0.9, 1.85, 11.5, 1.15, [
        ("Métrica Principal: TCGNS = (FN_choques / N_choques) × 100", 18, True, DARK),
        ("Secundárias: Taxa de Falso Alarme (FPR), Sensibilidade, Precisão do alerta, MAE geral e MAE nos choques graves.", 13.5, False, MUTED),
    ])

    rules = [
        ("PASSOU", "TCGNS ≤ 5%\nFalso Alarme ≤ 10%", "Suportado pelo IC 95%\n(Clopper–Pearson por cenário)", GREEN_SOFT, GREEN),
        ("INCONCLUSIVO", "5% < TCGNS ≤ 15%\nou 10% < FPR ≤ 20%", "Ou se o IC 95%\ncruzar o limiar definido", AMBER_SOFT, AMBER),
        ("CAIU", "TCGNS > 15%\nou Falso Alarme > 20%", "Reprovação técnica\ndocumentada sem ajustes", RED_SOFT, RED),
    ]
    for i, (lbl, cond, note, bgc, fg) in enumerate(rules):
        x = 0.65 + i * 4.1
        add_card(s2, x, 3.45, 3.85, 3.25, bgc, fg)
        add_lines(s2, x + 0.22, 3.65, 3.4, 2.8, [
            (lbl, 18, True, fg),
            (cond, 19, True, DARK),
            (note, 13.5, False, MUTED),
        ])
    add_footer(s2, 2)

    # SLIDE 3: ESQUEMA DA COMPARAÇÃO PAREADA (180 CENÁRIOS)
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_header(
        s3,
        "Slide 3 · Como Será a Comparação",
        "Protocolo pareado em 180 cenários novos (20 paradas · PE-60)",
        "Seeds de treino congeladas (100–159) separadas das seeds de teste (2000–2179).",
    )

    cols = [
        ("1. ENTRADA ÚNICA\n(180 Cenários)", "60 Graves (> 40 min)\n60 Interm. (15–40 min)\n60 Normais (≤ 15 min)\n\nMesma topologia (20 nós),\nmesmo GPS e mesmo input.", BLUE_SOFT, BLUE),
        ("2. 4 CONDIÇÕES\nLADO A LADO", "C1: Persistência\nC2: Tabular Corredor\nC3: ST-GCN Pura\nC4: ST-GCN + Trava [?]\n\nLimiar 15 min congelado\nantes da execução.", CARD, DARK),
        ("3. GABARITO &\nANÁLISE", "Gabarito independente\ninjetado no cenário.\n\nIC 95% Clopper–Pearson\nBootstrap 2000x pareado\npor cenário completo.", GREEN_SOFT, GREEN),
    ]
    for i, (head, body, bgc, fg) in enumerate(cols):
        x = 0.65 + i * 4.1
        add_card(s3, x, 1.8, 3.85, 4.75, bgc, fg)
        add_lines(s3, x + 0.25, 2.05, 3.35, 4.25, [
            (head, 17, True, fg if fg != DARK else DARK),
            (body, 14, False, DARK),
        ])
    add_footer(s3, 3)

    # SLIDE 4: CAMINHO ATÉ 02/12 + TESTE PEQUENO + PLANO B
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_header(
        s4,
        "Slide 4 · Caminho até o Pitch (18/11 → 02/12)",
        "Cronograma, teste pequeno já executado e Plano B",
        "Ética: 100% técnico sem participantes humanos (E2 humano adiado por exigir protocolo CEP).",
    )

    dates = [
        ("18/11", "Plano sem3\n& Regra"),
        ("19/11", "Congelar pesos,\nlimiar & seeds"),
        ("20–24/11", "Gerar 180 casos\n& auditar CSV"),
        ("25/11", "Execução\noficial"),
        ("27/11", "Auditoria\n& ICs 95%"),
        ("02/12", "Tabela no\nPitch Final"),
    ]
    for i, (dt, desc) in enumerate(dates):
        x = 0.65 + i * 2.02
        add_card(s4, x, 1.75, 1.88, 1.7, BLUE_SOFT if i != 3 else GREEN_SOFT, BLUE if i != 3 else GREEN)
        add_lines(s4, x + 0.12, 1.92, 1.64, 1.4, [
            (dt, 18, True, DARK),
            (desc, 12.5, False, MUTED),
        ], align=PP_ALIGN.CENTER)

    add_card(s4, 0.65, 3.75, 5.9, 2.95, AMBER_SOFT, AMBER)
    add_lines(s4, 0.88, 3.92, 5.45, 2.6, [
        ("Teste pequeno já rodou (--mode smoke, 6 cenários):", 15, True, DARK),
        ("• Quebrou na 1ª tentativa (assinatura STGCN: in_channels=1 e HISTORY_LEN=12). Corrigido antes de 18/11.\n• Na 2ª execução (7s): gerou CSV/JSON sem erros; C1 e C3 perderam 2/2 choques, C4 capturou 2/2.", 13, False, MUTED),
    ])

    add_card(s4, 6.78, 3.75, 5.9, 2.95, CARD, BORDER)
    add_lines(s4, 7.0, 3.92, 5.45, 2.6, [
        ("Plano B (execução blindada em 25/11):", 15, True, DARK),
        ("• Conjunto test_set.csv congelado localmente antes de 25/11.\n• Execução em Python/CPU 100% offline (sem depender de internet, navegador web ou banco Neon remoto).", 13, False, MUTED),
    ])
    add_footer(s4, 4)

    # SLIDE 5: FECHO E LIMITE HONESTO
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_header(
        s5,
        "Slide 5 · Escopo e Limite Honesto",
        "O que este teste prova em 02/12 — e o que ele não prova",
        "Rigor metodológico: preservar a possibilidade de a hipótese ser rejeitada pelos dados.",
    )

    add_card(s5, 0.65, 1.9, 5.85, 4.65, GREEN_SOFT, GREEN)
    add_lines(s5, 0.92, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE PROVA", 18, True, GREEN),
        ("• Se a Trava Híbrida [?] reduz falhas silenciosas (> 40 min) frente à ST-GCN pura e baselines.\n\n• Qual o custo exato em falsos alarmes.\n\n• Robustez controlada em perturbações fora da distribuição de treino (topologia de 20 nós da PE-60).", 14, False, DARK),
    ])

    add_card(s5, 6.83, 1.9, 5.85, 4.65, RED_SOFT, RED)
    add_lines(s5, 7.1, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE NÃO PROVA", 18, True, RED),
        ("• Validação operacional em tráfego real do Recife (depende de streaming AVL/GPS do CTM).\n\n• Redução direta de desistência humana sem coleta ética aprovada (CEP/UFRPE).\n\n• Superioridade garantida em MAE sobre regressão tabular.", 14, False, DARK),
    ])
    add_footer(s5, 5)

    OUT_VA2.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_VA2))
    shutil.copy2(OUT_VA2, OUT_WEB)
    print(f"Saved {OUT_VA2} ({OUT_VA2.stat().st_size} bytes)")
    print(f"Saved {OUT_WEB} ({OUT_WEB.stat().st_size} bytes)")
    if DRIVE_DIR.exists():
        drive_out = DRIVE_DIR / OUT_VA2.name
        shutil.copy2(OUT_VA2, drive_out)
        print(f"Synced to {drive_out}")


if __name__ == "__main__":
    build_deck()
