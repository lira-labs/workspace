"""
Gera o deck oficial do Seminário 3 (`sem3`: Como vai ser o teste) em Widescreen 16:9.
Segue estritamente o estilo visual do Prof. Lucas Silva Figueiredo (Pitch e Divulgação):
- Fundo Black/Dark limpo (#0E1117), ZERO caixas/cards poluídos
- 1 tag pill colorida no topo esquerdo por slide
- Tipografia grande (24pt a 56pt), alinhada à esquerda, palavras-chave em negrito
- 1 ideia por slide (6 slides, dentro do limite de 4 a 6 slides do sem3)
- Sem jargões obscuros ou símbolos matemáticos confusos

Salva em:
  1) va2/GrafoParada_Sem3_CauaLira.pptx
  2) code/grafoparada_web/GrafoParada_Sem3_CauaLira.pptx
  3) G:/Meu Drive/IA_Projetos/GrafoParada_Sem3_CauaLira.pptx
  4) G:/Meu Drive/IA_Projetos/GrafoParada_Sem3_BlackDark_CauaLira.pptx
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

# Paleta Black/Dark minimalista (inspirada nos slides do Prof. Lucas Figueiredo)
BG = RGBColor(0x0E, 0x11, 0x17)
WHITE = RGBColor(0xF8, 0xFA, 0xFC)
SOFT = RGBColor(0xCB, 0xD5, 0xE1)
MUTED = RGBColor(0x94, 0xA3, 0xB8)

TAG_TEAL = RGBColor(0x0D, 0x94, 0x88)
TAG_MAGENTA = RGBColor(0xBE, 0x18, 0x5D)
TAG_BLUE = RGBColor(0x02, 0x84, 0xC7)
TAG_AMBER = RGBColor(0xB4, 0x53, 0x09)
TAG_GREEN = RGBColor(0x05, 0x96, 0x69)
TAG_RED = RGBColor(0xB9, 0x1C, 0x1C)

ACCENT_GREEN = RGBColor(0x34, 0xD3, 0x99)
ACCENT_RED = RGBColor(0xFB, 0x71, 0x85)
ACCENT_AMBER = RGBColor(0xFB, 0xBF, 0x24)
ACCENT_BLUE = RGBColor(0x38, 0xBD, 0xF8)

FONT_NAME = "Segoe UI"
FONT_LIGHT = "Segoe UI Light"


def set_bg(slide, color=BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_pill_tag(slide, text: str, bg_color: RGBColor, left: float = 0.9, top: float = 0.65, width: float = 3.2):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.68)
    )
    shape.adjustments[0] = 0.25
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.name = FONT_NAME
    r.font.size = Pt(20)
    r.font.bold = False
    r.font.color.rgb = WHITE
    return shape


def add_rich_paragraphs(slide, left: float, top: float, width: float, height: float, paragraphs: list[dict]):
    """
    paragraphs: lista de dicts com:
      - runs: lista de tuplas (texto, tamanho_pt, bold, cor)
      - space_after: Pt opcional (default 18)
      - space_before: Pt opcional (default 0)
    """
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, p_cfg in enumerate(paragraphs):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.alignment = p_cfg.get("align", PP_ALIGN.LEFT)
        p.space_after = Pt(p_cfg.get("space_after", 18))
        p.space_before = Pt(p_cfg.get("space_before", 0))
        for txt, size, bold, color in p_cfg["runs"]:
            r = p.add_run()
            r.text = txt
            r.font.name = FONT_NAME if bold else FONT_LIGHT
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
    return tb


def add_footer(slide, page_num: int, total: int = 6):
    add_rich_paragraphs(
        slide,
        0.9,
        6.9,
        11.5,
        0.4,
        [{
            "runs": [(f"GrafoParada  ·  Seminário 3  ·  {page_num}/{total}", 13, False, MUTED)],
            "space_after": 0,
        }],
    )


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: O COMPETIDOR — O QUE ELE MEDE E O NÚMERO DELE
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_bg(s1)
    add_pill_tag(s1, "o competidor", TAG_BLUE, width=2.8)
    add_rich_paragraphs(s1, 0.9, 1.65, 11.6, 5.1, [
        {
            "runs": [
                ("o que os competidores ", 36, False, WHITE),
                ("medem", 36, True, WHITE),
                (" no mesmo cenário", 36, False, WHITE),
            ],
            "space_after": 32,
        },
        {
            "runs": [
                ("•  ", 24, True, ACCENT_RED),
                ("Persistência", 24, True, WHITE),
                (" (último atraso): ", 24, False, SOFT),
                ("7,1 min", 24, True, ACCENT_RED),
                (" de erro · perde 97% dos alertas", 24, False, SOFT),
            ],
            "space_after": 24,
        },
        {
            "runs": [
                ("•  ", 24, True, ACCENT_BLUE),
                ("Regressão Tabular", 24, True, WHITE),
                (" (histórico da via): ", 24, False, SOFT),
                ("1,9 min", 24, True, ACCENT_BLUE),
                (" de erro em 20 paradas", 24, False, SOFT),
            ],
            "space_after": 24,
        },
        {
            "runs": [
                ("•  ", 24, True, ACCENT_AMBER),
                ("ST-GCN sozinha", 24, True, WHITE),
                (" (rede neural): ", 24, False, SOFT),
                ("1,5 min", 24, True, ACCENT_AMBER),
                (" normal · falha em bloqueio", 24, False, SOFT),
            ],
            "space_after": 40,
        },
        {
            "runs": [
                ("Cittamobi e Moovit são fechados — não permitem rodar o mesmo cenário controlado.", 18, False, MUTED),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s1, 1)

    # =========================================================================
    # SLIDE 2: A FALHA QUE QUEREMOS RESOLVER (1 IDEIA, IMPACTO IMEDIATO)
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    set_bg(s2)
    add_pill_tag(s2, "o problema real", TAG_RED, width=3.1)
    add_rich_paragraphs(s2, 0.9, 1.85, 11.6, 4.8, [
        {
            "runs": [
                ("45 minutos", 58, True, ACCENT_RED),
                (" de atraso real", 46, False, WHITE),
            ],
            "space_after": 12,
        },
        {
            "runs": [
                ("previsto como ", 44, False, SOFT),
                ("14 minutos", 52, True, ACCENT_AMBER),
                (" — sem aviso.", 44, False, WHITE),
            ],
            "space_after": 38,
        },
        {
            "runs": [
                ("Na Parada 10 da PE-60, a rede neural sozinha suavizou o bloqueio.", 26, False, SOFT),
            ],
            "space_after": 12,
        },
        {
            "runs": [
                ("O passageiro ficou esperando no ponto ", 26, False, SOFT),
                ("sem saber o que aconteceu.", 26, True, WHITE),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s2, 2)

    # =========================================================================
    # SLIDE 3: O QUE NÓS MEDIMOS E O QUE A NOSSA IDEIA MELHORA
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    set_bg(s3)
    add_pill_tag(s3, "o que medimos", TAG_MAGENTA, width=3.0)
    add_rich_paragraphs(s3, 0.9, 1.55, 11.6, 5.2, [
        {
            "runs": [
                ("Nossa melhoria: ", 32, False, SOFT),
                ("ST-GCN + Alerta pelo GPS", 34, True, ACCENT_GREEN),
            ],
            "space_after": 8,
        },
        {
            "runs": [
                ("Avisa o passageiro sempre que o GPS divergir mais de ", 24, False, SOFT),
                ("15 min", 24, True, WHITE),
                (" da previsão.", 24, False, SOFT),
            ],
            "space_after": 28,
        },
        {
            "runs": [
                ("•  ", 25, True, ACCENT_GREEN),
                ("Medida principal: ", 25, True, WHITE),
                ("atrasos acima de 40 min perdidos sem aviso", 25, False, SOFT),
            ],
            "space_after": 14,
        },
        {
            "runs": [
                ("•  ", 25, True, ACCENT_AMBER),
                ("Custo medido: ", 25, True, WHITE),
                ("alarmes falsos em dias normais", 25, False, SOFT),
            ],
            "space_after": 28,
        },
        {
            "runs": [
                ("Passou: ", 24, True, ACCENT_GREEN),
                ("até 5% de falhas graves e até 10% de alarmes falsos", 24, False, SOFT),
            ],
            "space_after": 10,
        },
        {
            "runs": [
                ("Caiu: ", 24, True, ACCENT_RED),
                ("acima de 15% de falhas ou 20% de alarmes falsos", 24, False, SOFT),
                ("  (entre os dois: inconclusivo)", 20, False, MUTED),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s3, 3)

    # =========================================================================
    # SLIDE 4: COMO VAMOS COMPARAR (180 CENÁRIOS PAREADOS)
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    set_bg(s4)
    add_pill_tag(s4, "como testar", TAG_TEAL, width=2.6)
    add_rich_paragraphs(s4, 0.9, 1.65, 11.6, 5.1, [
        {
            "runs": [
                ("180 cenários novos", 42, True, WHITE),
                (" nas 20 paradas da PE-60", 34, False, SOFT),
            ],
            "space_after": 28,
        },
        {
            "runs": [
                ("•  ", 28, True, ACCENT_RED),
                ("60", 30, True, ACCENT_RED),
                (" atrasos graves (mais de 40 min)", 28, False, SOFT),
            ],
            "space_after": 14,
        },
        {
            "runs": [
                ("•  ", 28, True, ACCENT_AMBER),
                ("60", 30, True, ACCENT_AMBER),
                (" atrasos médios (15 a 40 min)", 28, False, SOFT),
            ],
            "space_after": 14,
        },
        {
            "runs": [
                ("•  ", 28, True, ACCENT_GREEN),
                ("60", 30, True, ACCENT_GREEN),
                (" dias normais (até 15 min)", 28, False, SOFT),
            ],
            "space_after": 30,
        },
        {
            "runs": [
                ("Os ", 24, False, SOFT),
                ("4 métodos", 24, True, WHITE),
                (" recebem exatamente o mesmo trajeto, horário e GPS — separados do treino.", 24, False, SOFT),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s4, 4)

    # =========================================================================
    # SLIDE 5: CAMINHO ATÉ O PITCH (02/12) + PILOTO + PLANO B
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    set_bg(s5)
    add_pill_tag(s5, "até 02/12", TAG_AMBER, width=2.3)
    add_rich_paragraphs(s5, 0.9, 1.65, 11.8, 5.1, [
        {
            "runs": [
                ("18/11 ", 25, True, WHITE),
                ("plano  ·  ", 23, False, MUTED),
                ("19/11 ", 25, True, WHITE),
                ("congelar  ·  ", 23, False, MUTED),
                ("25/11 ", 25, True, ACCENT_GREEN),
                ("rodar 180 casos  ·  ", 23, False, ACCENT_GREEN),
                ("02/12 ", 25, True, WHITE),
                ("pitch", 23, False, MUTED),
            ],
            "space_after": 36,
        },
        {
            "runs": [
                ("•  ", 25, True, ACCENT_GREEN),
                ("Teste piloto (6 cenários) já rodou: ", 25, True, WHITE),
                ("os métodos sem alerta perderam os 2 atrasos graves; o Alerta pelo GPS pegou os 2 sem alarmes falsos.", 25, False, SOFT),
            ],
            "space_after": 24,
        },
        {
            "runs": [
                ("•  ", 25, True, ACCENT_BLUE),
                ("Plano B: ", 25, True, WHITE),
                ("base congelada no PC e execução 100% offline em Python.", 25, False, SOFT),
            ],
            "space_after": 28,
        },
        {
            "runs": [
                ("Ética: teste 100% técnico, sem expor passageiros reais.", 19, False, MUTED),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s5, 5)

    # =========================================================================
    # SLIDE 6: O QUE PROVA E O LIMITE HONESTO
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    set_bg(s6)
    add_pill_tag(s6, "limites", TAG_GREEN, width=2.2)
    add_rich_paragraphs(s6, 0.9, 1.7, 11.5, 5.0, [
        {
            "runs": [
                ("O que este teste ", 34, False, WHITE),
                ("prova", 34, True, ACCENT_GREEN),
            ],
            "space_after": 12,
        },
        {
            "runs": [
                ("Se o ", 26, False, SOFT),
                ("Alerta pelo GPS", 26, True, WHITE),
                (" corta falhas silenciosas acima de 40 min na PE-60 — e quantos alarmes falsos custa.", 26, False, SOFT),
            ],
            "space_after": 36,
        },
        {
            "runs": [
                ("O que ele ", 34, False, WHITE),
                ("não prova ainda", 34, True, ACCENT_RED),
            ],
            "space_after": 12,
        },
        {
            "runs": [
                ("Operação ao vivo com toda a frota do Recife (depende do sinal oficial do CTM) nem estudo com passageiros (exige comitê de ética).", 26, False, SOFT),
            ],
            "space_after": 0,
        },
    ])
    add_footer(s6, 6)

    OUT_VA2.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(OUT_VA2))
    shutil.copy2(OUT_VA2, OUT_WEB)
    print(f"Saved {OUT_VA2} ({OUT_VA2.stat().st_size} bytes)")
    print(f"Saved {OUT_WEB} ({OUT_WEB.stat().st_size} bytes)")
    if DRIVE_DIR.exists():
        for name in (OUT_VA2.name, "GrafoParada_Sem3_BlackDark_CauaLira.pptx"):
            drive_out = DRIVE_DIR / name
            shutil.copy2(OUT_VA2, drive_out)
            print(f"Synced to {drive_out}")


if __name__ == "__main__":
    build_deck()
