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

BG = RGBColor(0x09, 0x0D, 0x16)
CARD = RGBColor(0x11, 0x18, 0x27)
BORDER = RGBColor(0x28, 0x35, 0x48)
DARK = RGBColor(0xF9, 0xFA, 0xFB)
MUTED = RGBColor(0x9C, 0xA3, 0xAF)
BODY = RGBColor(0xD1, 0xD5, 0xDB)

GREEN = RGBColor(0x10, 0xB9, 0x81)
GREEN_SOFT = RGBColor(0x0A, 0x26, 0x1F)
RED = RGBColor(0xF8, 0x71, 0x71)
RED_SOFT = RGBColor(0x2B, 0x12, 0x16)
AMBER = RGBColor(0xFB, 0xBF, 0x24)
AMBER_SOFT = RGBColor(0x29, 0x1E, 0x0B)
BLUE = RGBColor(0x38, 0xBD, 0xF8)
BLUE_SOFT = RGBColor(0x0D, 0x21, 0x36)


def set_bg(slide, color=BG):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_header(slide, tag: str, title: str, subtitle: str):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.08))
    bar.fill.solid()
    bar.fill.fore_color.rgb = GREEN
    bar.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.28), Inches(12.0), Inches(1.18))
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
    r1.font.size = Pt(27)
    r1.font.bold = True
    r1.font.color.rgb = DARK

    p2 = tf.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = subtitle
    r2.font.size = Pt(13.5)
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
        p.space_after = Pt(6)
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

    # SLIDE 1: O COMPETIDOR E O QUE ELE CONSEGUE
    s1 = prs.slides.add_slide(blank)
    set_bg(s1)
    add_header(
        s1,
        "Slide 1 · O Competidor e o Que Ele Consegue",
        "Por que comparar Persistência, Regressão Tabular e ST-GCN Pura",
        "Caso real do Seminário 2 (Parada 10 · PE-60): atraso de 45 min previsto como 14,3 min sem aviso.",
    )

    cards_s1 = [
        ("1. Persistência", "7,13 min de erro médio\n97% dos alertas perdidos", "Apenas repete o último atraso medido.\nSempre avisa tarde demais.", RED_SOFT, RED),
        ("2. Regressão Tabular", "1,93 min de erro médio\n(em 20 paradas da via)", "Usa o histórico fixo do corredor,\nmas não enxerga a rede em grafo.", BLUE_SOFT, BLUE),
        ("3. ST-GCN Pura (sem trava)", "1,51 min em dia normal\n14,3 min no choque de 45 min", "Aprende a difusão na rede,\nmas suaviza bloqueios súbitos.", AMBER_SOFT, AMBER),
    ]
    for i, (t, metric, desc, bgc, fg) in enumerate(cards_s1):
        x = 0.65 + i * 4.1
        add_card(s1, x, 1.8, 3.85, 3.3, bgc, fg)
        add_lines(s1, x + 0.24, 2.02, 3.37, 2.9, [
            (t, 16.5, True, DARK),
            (metric, 18.5, True, fg),
            (desc, 13.5, False, BODY),
        ])

    add_card(s1, 0.65, 5.38, 12.03, 1.42, CARD, BORDER)
    add_lines(s1, 0.9, 5.52, 11.5, 1.15, [
        ("Por que Cittamobi e Moovit ficam fora da comparação direta?", 13.5, True, DARK),
        ("• São aplicativos fechados e não rodam sobre os mesmos cenários controlados. A comparação científica justa avalia os modelos abertos sobre exatamente a mesma entrada.", 12.5, False, BODY),
    ])
    add_footer(s1, 1)

    # SLIDE 2: O QUE QUERO MOSTRAR E COMO VOU MEDIR
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_header(
        s2,
        "Slide 2 · O Alvo e a Regra Pré-Registrada",
        "Reduzir atrasos graves sem aviso (acima de 40 min)",
        "ST-GCN + Trava Híbrida: dispara alerta sempre que o GPS divergir mais de 15 min da previsão.",
    )

    add_card(s2, 0.65, 1.75, 12.03, 1.42, BLUE_SOFT, BLUE)
    add_lines(s2, 0.9, 1.9, 11.5, 1.12, [
        ("Métrica principal: percentual de atrasos graves (acima de 40 min) perdidos sem aviso", 17.5, True, DARK),
        ("Métricas secundárias: taxa de alarmes falsos, sensibilidade do alerta e erro médio em minutos (geral e nos choques).", 13, False, BODY),
    ])

    rules = [
        ("PASSOU", "Até 5% de falhas graves\nAté 10% de alarmes falsos", "Sustentado por intervalo de\nconfiança de 95% nos cenários", GREEN_SOFT, GREEN),
        ("INCONCLUSIVO", "Entre 5% e 15% de falhas\nou 10% a 20% de alarmes falsos", "Ou quando a margem de 95%\ncruzar o limite definido", AMBER_SOFT, AMBER),
        ("CAIU", "Acima de 15% de falhas\nou mais de 20% de alarmes falsos", "Reprovação documentada\nsem ajustar o limiar depois", RED_SOFT, RED),
    ]
    for i, (lbl, cond, note, bgc, fg) in enumerate(rules):
        x = 0.65 + i * 4.1
        add_card(s2, x, 3.45, 3.85, 3.25, bgc, fg)
        add_lines(s2, x + 0.24, 3.68, 3.37, 2.8, [
            (lbl, 18, True, fg),
            (cond, 17, True, DARK),
            (note, 13.5, False, BODY),
        ])
    add_footer(s2, 2)

    # SLIDE 3: COMO SERÁ A COMPARAÇÃO PAREADA
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_header(
        s3,
        "Slide 3 · Como Será a Comparação",
        "Protocolo pareado em 180 cenários novos (20 paradas · PE-60)",
        "Cenários de teste separados dos cenários de treino, com pesos e limiar congelados antes da execução.",
    )

    cols = [
        ("1. ENTRADA ÚNICA\n(180 Cenários)", "60 Choques Graves (acima de 40 min)\n60 Intermediários (15 a 40 min)\n60 Normais (até 15 min)\n\nMesmas 20 paradas da PE-60,\nmesmo horário e mesmo GPS.", BLUE_SOFT, BLUE),
        ("2. QUATRO CONDIÇÕES\nLADO A LADO", "1. Persistência\n2. Regressão Tabular\n3. ST-GCN Pura\n4. ST-GCN + Trava Híbrida\n\nTodas avaliadas sobre a\nmesma entrada, sem ajustes.", CARD, BLUE),
        ("3. GABARITO &\nAUDITORIA", "Atraso real e rótulo de choque\ngrave definidos antes do modelo.\n\nApuração com intervalo de\nconfiança de 95% por cenário.", GREEN_SOFT, GREEN),
    ]
    for i, (head, body, bgc, fg) in enumerate(cols):
        x = 0.65 + i * 4.1
        add_card(s3, x, 1.82, 3.85, 4.75, bgc, fg)
        add_lines(s3, x + 0.25, 2.08, 3.35, 4.25, [
            (head, 17, True, fg),
            (body, 14, False, BODY),
        ])
    add_footer(s3, 3)

    # SLIDE 4: COMO CHEGAR AO PITCH COM RESULTADO
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_header(
        s4,
        "Slide 4 · Caminho até o Pitch (18/11 a 02/12)",
        "Cronograma, teste piloto já executado e Plano B offline",
        "Ética: teste 100% técnico sem participantes humanos (coleta com pessoas exige aprovação prévia em comitê).",
    )

    dates = [
        ("18/11", "Plano e regra\npré-registrada"),
        ("19/11", "Congelar pesos,\nlimiar e seeds"),
        ("20 a 24/11", "Gerar 180 casos\ne validar dados"),
        ("25/11", "Execução\noficial"),
        ("27/11", "Auditoria e\nmargens 95%"),
        ("02/12", "Tabela final\nno Pitch"),
    ]
    for i, (dt, desc) in enumerate(dates):
        x = 0.65 + i * 2.02
        add_card(s4, x, 1.78, 1.88, 1.7, BLUE_SOFT if i != 3 else GREEN_SOFT, BLUE if i != 3 else GREEN)
        add_lines(s4, x + 0.12, 1.95, 1.64, 1.4, [
            (dt, 17, True, DARK),
            (desc, 12, False, BODY),
        ], align=PP_ALIGN.CENTER)

    add_card(s4, 0.65, 3.78, 5.9, 2.92, AMBER_SOFT, AMBER)
    add_lines(s4, 0.88, 3.95, 5.45, 2.55, [
        ("Teste piloto já executado (6 cenários):", 15, True, AMBER),
        ("• Corrigimos a assinatura de entrada da ST-GCN antes do seminário.\n• Na execução completa (7s): Persistência e ST-GCN Pura perderam os 2 choques graves; ST-GCN + Trava Híbrida capturou os 2 sem alarmes falsos.", 13, False, BODY),
    ])

    add_card(s4, 6.78, 3.78, 5.9, 2.92, CARD, BORDER)
    add_lines(s4, 7.0, 3.95, 5.45, 2.55, [
        ("Plano B (execução blindada em 25/11):", 15, True, DARK),
        ("• Base de cenários congelada localmente em arquivo CSV.\n• Execução 100% offline em Python no PC, sem depender de internet, navegador ou servidor externo.", 13, False, BODY),
    ])
    add_footer(s4, 4)

    # SLIDE 5: FECHO E LIMITE HONESTO
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_header(
        s5,
        "Slide 5 · Fecho e Limite Honesto",
        "O que este teste prova em 02/12 — e o que não prova ainda",
        "Rigor científico: preservar a possibilidade de a hipótese ser rejeitada pelos dados.",
    )

    add_card(s5, 0.65, 1.9, 5.85, 4.65, GREEN_SOFT, GREEN)
    add_lines(s5, 0.92, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE PROVA", 18, True, GREEN),
        ("• Se a ST-GCN + Trava Híbrida reduz falhas silenciosas (acima de 40 min) frente à ST-GCN Pura, Regressão Tabular e Persistência.\n\n• Qual é o custo real em alarmes falsos.\n\n• Robustez controlada a bloqueios fora do padrão de treino nas 20 paradas da PE-60.", 14, False, BODY),
    ])

    add_card(s5, 6.83, 1.9, 5.85, 4.65, RED_SOFT, RED)
    add_lines(s5, 7.1, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE NÃO PROVA AINDA", 18, True, RED),
        ("• Validação operacional em tempo real com toda a frota do Recife (depende de sinal oficial ao vivo do CTM).\n\n• Redução direta de desistência humana na parada (exige estudo aprovado em comitê de ética).\n\n• Superioridade garantida em erro médio nos dias comuns.", 14, False, BODY),
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
