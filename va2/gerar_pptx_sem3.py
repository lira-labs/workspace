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
        "Slide 1 · O Problema e os Concorrentes",
        "Por que comparar 3 modelos nos mesmos cenários",
        "No teste anterior (PE-60), um atraso grave de 45 min foi previsto como 14 min sem nenhum alerta.",
    )

    cards_s1 = [
        ("1. Modelo Simples (Hoje)", "Erro médio: 7,13 min\nPerdeu 97% dos alertas", "Olha só o atraso do momento.\nSempre avisa tarde demais.", RED_SOFT, RED),
        ("2. Modelo de Tabela", "Erro médio: 1,93 min\nBom em amostras pequenas", "Usa histórico fixo da linha,\nmas não enxerga a rede toda.", BLUE_SOFT, BLUE),
        ("3. Rede Neural Pura", "Erro médio normal: 1,51 min\n14 min no atraso de 45 min", "Aprende o ritmo da cidade,\nmas suaviza bloqueios súbitos.", AMBER_SOFT, AMBER),
    ]
    for i, (t, metric, desc, bgc, fg) in enumerate(cards_s1):
        x = 0.65 + i * 4.1
        add_card(s1, x, 1.75, 3.85, 3.35, bgc, fg)
        add_lines(s1, x + 0.22, 1.95, 3.4, 3.0, [
            (t, 16.5, True, DARK),
            (metric, 19, True, fg),
            (desc, 13.5, False, MUTED),
        ])

    add_card(s1, 0.65, 5.35, 12.03, 1.45, CARD, BORDER)
    add_lines(s1, 0.9, 5.5, 11.5, 1.2, [
        ("Por que comparamos com modelos abertos e não apenas com apps comerciais (Cittamobi / Moovit)?", 13.5, True, DARK),
        ("• Apps fechados não permitem rodar os mesmos cenários controlados. Nossa avaliação mede em igualdade de condições quem evita deixar o passageiro esperando sem aviso.", 12.5, False, MUTED),
    ])
    add_footer(s1, 1)

    # SLIDE 2: O QUE QUEREMOS MEDIR E QUANDO PASSA
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_header(
        s2,
        "Slide 2 · O Alvo e a Regra de Aprovação",
        "Evitar atrasos graves sem aviso (acima de 40 min)",
        "Trava de Segurança: dispara alerta quando o GPS mostra mais de 15 min de diferença para a previsão.",
    )

    add_card(s2, 0.65, 1.7, 12.03, 1.45, BLUE_SOFT, BLUE)
    add_lines(s2, 0.9, 1.85, 11.5, 1.15, [
        ("Pergunta central: quantos atrasos graves passam sem alerta ao passageiro?", 18, True, DARK),
        ("Também medimos: quantos alarmes falsos ocorrem, acerto dos alertas e erro médio em minutos.", 13.5, False, MUTED),
    ])

    rules = [
        ("APROVADO", "Até 5% de falhas graves\nAté 10% de alarmes falsos", "Resultado firme e confiável\nem todos os cenários", GREEN_SOFT, GREEN),
        ("INCONCLUSIVO", "Entre 5% e 15% de falhas\nou 10% a 20% de alarmes falsos", "Precisa de mais testes\npara confirmar o ganho", AMBER_SOFT, AMBER),
        ("REPROVADO", "Acima de 15% de falhas\nou mais de 20% de alarmes falsos", "Reprovação registrada\ncom transparência", RED_SOFT, RED),
    ]
    for i, (lbl, cond, note, bgc, fg) in enumerate(rules):
        x = 0.65 + i * 4.1
        add_card(s2, x, 3.45, 3.85, 3.25, bgc, fg)
        add_lines(s2, x + 0.22, 3.65, 3.4, 2.8, [
            (lbl, 18, True, fg),
            (cond, 17.5, True, DARK),
            (note, 13.5, False, MUTED),
        ])
    add_footer(s2, 2)

    # SLIDE 3: COMO SERÁ O TESTE PAREADO
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_header(
        s3,
        "Slide 3 · Como Será a Comparação",
        "Mesmos 180 cenários testados nos 4 modelos lado a lado",
        "Dados de treino separados dos cenários de teste para garantir avaliação justa.",
    )

    cols = [
        ("1. MESMA ENTRADA\n(180 Cenários)", "60 Atrasos Graves (mais de 40 min)\n60 Atrasos Médios (15 a 40 min)\n60 Dias Normais (até 15 min)\n\nMesmas 20 paradas da PE-60\ne mesmo sinal de GPS.", BLUE_SOFT, BLUE),
        ("2. 4 MODELOS\nLADO A LADO", "1. Modelo Simples (Hoje)\n2. Modelo de Tabela\n3. Rede Neural Pura\n4. Rede Neural + Trava\n\nRegra de 15 min fixada\nantes de rodar os testes.", CARD, DARK),
        ("3. ANÁLISE\nTRANSPARENTE", "Gabarito real salvo\nem cada cenário.\n\nComparamos a taxa de\nfalhas e o erro em minutos\ncom margem estatística.", GREEN_SOFT, GREEN),
    ]
    for i, (head, body, bgc, fg) in enumerate(cols):
        x = 0.65 + i * 4.1
        add_card(s3, x, 1.8, 3.85, 4.75, bgc, fg)
        add_lines(s3, x + 0.25, 2.05, 3.35, 4.25, [
            (head, 17, True, fg if fg != DARK else DARK),
            (body, 14, False, DARK),
        ])
    add_footer(s3, 3)

    # SLIDE 4: CRONOGRAMA E TESTE PILOTO
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_header(
        s4,
        "Slide 4 · Cronograma até o Pitch (18/11 a 02/12)",
        "Etapas planejadas, teste piloto já aprovado e Plano B",
        "Ética: teste técnico sem expor passageiros reais (coleta com pessoas fica para etapa futura).",
    )

    dates = [
        ("18/11", "Definir plano\ne regras"),
        ("19/11", "Congelar modelo\ne cenários"),
        ("20 a 24/11", "Gerar 180 casos\ne conferir dados"),
        ("25/11", "Rodar o teste\noficial"),
        ("27/11", "Conferir\nresultados"),
        ("02/12", "Apresentar\nno Pitch Final"),
    ]
    for i, (dt, desc) in enumerate(dates):
        x = 0.65 + i * 2.02
        add_card(s4, x, 1.75, 1.88, 1.7, BLUE_SOFT if i != 3 else GREEN_SOFT, BLUE if i != 3 else GREEN)
        add_lines(s4, x + 0.12, 1.92, 1.64, 1.4, [
            (dt, 17, True, DARK),
            (desc, 12.5, False, MUTED),
        ], align=PP_ALIGN.CENTER)

    add_card(s4, 0.65, 3.75, 5.9, 2.95, AMBER_SOFT, AMBER)
    add_lines(s4, 0.88, 3.92, 5.45, 2.6, [
        ("Teste piloto já executado (6 cenários):", 15, True, DARK),
        ("• Ajustamos a entrada do modelo antes da apresentação.\n• No teste completo (7s): gerou planilhas e resultados sem erros; os modelos sem trava perderam 2 de 2 atrasos graves, enquanto o modelo com trava detectou os 2.", 13, False, MUTED),
    ])

    add_card(s4, 6.78, 3.75, 5.9, 2.95, CARD, BORDER)
    add_lines(s4, 7.0, 3.92, 5.45, 2.6, [
        ("Plano B (garantia no dia 25/11):", 15, True, DARK),
        ("• Base de cenários salva localmente no computador.\n• Execução 100% offline em Python, sem depender de internet, navegador ou servidor externo.", 13, False, MUTED),
    ])
    add_footer(s4, 4)

    # SLIDE 5: O QUE ESTE TESTE PROVA E O QUE NÃO PROVA
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_header(
        s5,
        "Slide 5 · Escopo e Transparência",
        "O que este teste comprova em 02/12 — e seus limites",
        "Honestidade científica: aceitar o resultado que os dados mostrarem.",
    )

    add_card(s5, 0.65, 1.9, 5.85, 4.65, GREEN_SOFT, GREEN)
    add_lines(s5, 0.92, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE COMPROVA", 18, True, GREEN),
        ("• Se a Trava de Segurança reduz falhas silenciosas em atrasos graves (mais de 40 min).\n\n• Quantos alarmes falsos ela gera na prática.\n\n• Como o modelo reage a bloqueios inesperados fora do padrão de treino.", 14, False, DARK),
    ])

    add_card(s5, 6.83, 1.9, 5.85, 4.65, RED_SOFT, RED)
    add_lines(s5, 7.1, 2.15, 5.3, 4.15, [
        ("O QUE O TESTE NÃO COMPROVA", 18, True, RED),
        ("• Operação em tempo real com todos os ônibus do Recife (depende de sinal oficial ao vivo).\n\n• Mudança no comportamento de passageiros reais (exige pesquisa aprovada com usuários).\n\n• Que a rede neural vença sempre em dias comuns sem incidentes.", 14, False, DARK),
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
