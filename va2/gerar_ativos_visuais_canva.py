# -*- coding: utf-8 -*-
"""
Gerador de Ativos Gráficos em Alta Resolução (300 DPI Style) para Slides do Seminário 2
Padronização Canva/Keynote: Zero AI-Slop, dados reais, tipografia limpa e diagramação editorial.
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("va2/img", exist_ok=True)

# Paleta de Cores Editorial Canva
BG_DARK = (10, 15, 29)          # Deep Navy/Slate #0A0F1D
CARD_BG = (17, 24, 39)          # Dark Slate #111827
CARD_BORDER = (31, 41, 55)      # Slate Border #1F2937
ACCENT_BLUE = (2, 132, 199)     # Sky Blue #0284C7
ACCENT_CYAN = (56, 189, 248)    # Light Sky #38BDF8
EMERALD = (16, 185, 129)        # Emerald Green #10B981
EMERALD_BG = (6, 78, 59)        # Deep Green #064E3B
DANGER_RED = (244, 63, 94)      # Rose/Red #F43F5E
DANGER_BG = (76, 5, 25)         # Deep Red #4C0519
AMBER = (245, 158, 11)          # Amber #F59E0B
AMBER_BG = (69, 26, 3)          # Deep Amber #451A03
TEXT_WHITE = (248, 250, 252)    # Slate 50 #F8FAFC
TEXT_MUTED = (148, 163, 184)    # Slate 400 #94A3B8
TEXT_LIGHT = (226, 232, 240)    # Slate 200 #E2E8F0

FONT_DIR = r"C:\Windows\Fonts"
def get_font(name="segoeui.ttf", size=14):
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()

def draw_rounded_card(draw, box, radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

# ==============================================================================
# ATIVO 1: MOCKUP REALISTA DO SMARTPHONE COM GRAFOPARADA (va2/img/mockup_app_sem2.png)
# ==============================================================================
def gerar_mockup_smartphone():
    W, H = 540, 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Corpo do Smartphone (Titânio Slate)
    phone_box = [15, 15, W - 15, H - 15]
    draw.rounded_rectangle(phone_box, radius=52, fill=(24, 30, 44), outline=(51, 65, 85), width=6)
    
    # Tela Interna
    screen_box = [24, 24, W - 24, H - 24]
    draw.rounded_rectangle(screen_box, radius=44, fill=(248, 250, 252))

    # Mapa de Fundo da PE-60 (Simulação Vetorial Nítida)
    # Fundo do mapa em tom pastel
    draw.rectangle([24, 24, W - 24, 620], fill=(226, 232, 240))
    # Ruas secundárias
    draw.line([(30, 180), (W - 30, 220)], fill=(203, 213, 225), width=6)
    draw.line([(80, 80), (120, 500)], fill=(203, 213, 225), width=8)
    draw.line([(380, 120), (420, 600)], fill=(203, 213, 225), width=8)
    # Rodovia PE-60 Principal (Traçado Azul Turquesa da Linha 199)
    pe60_pts = [
        (80, 520), (140, 430), (210, 350), (280, 280), (350, 210), (430, 140), (480, 80)
    ]
    draw.line(pe60_pts, fill=(2, 132, 199, 80), width=16) # Glow
    draw.line(pe60_pts, fill=(2, 132, 199), width=7)

    # Paradas ao longo da rota (#01 a #04)
    stops_coords = [
        ((80, 520), "#01 Camela", True),
        ((210, 350), "#02 Trevo PE-60", False),
        ((350, 210), "#03 Suape", False),
        ((480, 80), "#04 TI Cabo", False),
    ]
    for pt, label, is_active in stops_coords:
        x, y = pt
        if is_active:
            draw.ellipse([x - 14, y - 14, x + 14, y + 14], fill=(16, 185, 129), outline=(255, 255, 255), width=3)
            # Tooltip
            draw.rounded_rectangle([x - 55, y - 48, x + 55, y - 20], radius=8, fill=(15, 23, 42))
            draw.text((x, y - 34), "📍 Parada Atual", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 11), anchor="mm")
        else:
            draw.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(2, 132, 199), outline=(255, 255, 255), width=2)

    # Ônibus Animado 199 em trânsito
    bx, by = 175, 390
    draw.rounded_rectangle([bx - 60, by - 16, bx + 60, by + 16], radius=16, fill=(15, 23, 42), outline=(16, 185, 129), width=2)
    draw.text((bx, by), "🚌 199 · 42 km/h", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 12), anchor="mm")

    # Dynamic Island / Notch
    draw.rounded_rectangle([W//2 - 65, 32, W//2 + 65, 62], radius=16, fill=(0, 0, 0))
    draw.ellipse([W//2 + 38, 42, W//2 + 48, 52], fill=(20, 20, 30))

    # Barra Superior de Status (06:10 · 5G · 94%)
    draw.text((54, 46), "06:10", fill=(15, 23, 42), font=get_font("segoeuib.ttf", 13), anchor="lm")
    draw.text((W - 54, 46), "5G  94%", fill=(15, 23, 42), font=get_font("segoeuib.ttf", 12), anchor="rm")

    # Floating Top Bar com Pílulas
    pills_y = 78
    pills = [
        ("👤 Cauã", (255, 255, 255), (15, 23, 42)),
        ("📅 05h45", (220, 252, 231), (22, 101, 52)),
        ("👁️ Fácil", (241, 245, 249), (51, 65, 85)),
        ("🏛️ CTM", (224, 242, 254), (3, 105, 161)),
        ("🟢 199", (220, 252, 231), (22, 101, 52)),
    ]
    px = 38
    for txt, bg_c, fg_c in pills:
        draw.rounded_rectangle([px, pills_y, px + 84, pills_y + 30], radius=15, fill=bg_c, outline=(203, 213, 225), width=1)
        draw.text((px + 42, pills_y + 15), txt, fill=fg_c, font=get_font("segoeuib.ttf", 11), anchor="mm")
        px += 92

    # Bottom Sheet (Painel Inferior de Alta Usabilidade)
    bs_top = 460
    draw.rounded_rectangle([24, bs_top, W - 24, H - 24], radius=32, fill=(255, 255, 255), outline=(226, 232, 240), width=2)
    # Handle bar
    draw.rounded_rectangle([W//2 - 24, bs_top + 10, W//2 + 24, bs_top + 15], radius=3, fill=(203, 213, 225))

    # Banner CTM de Realocação de Frota
    draw.rounded_rectangle([38, bs_top + 26, W - 38, bs_top + 64], radius=10, fill=(240, 249, 255), outline=(186, 230, 253), width=1)
    draw.text((48, bs_top + 45), "⚡ CTM FROTA: Ônibus 178 transferido do vazio para reforço!", fill=(2, 132, 199), font=get_font("segoeuib.ttf", 11), anchor="lm")

    # Card da Parada Atual
    card_y = bs_top + 74
    draw.rounded_rectangle([38, card_y, W - 38, card_y + 140], radius=14, fill=(248, 250, 252), outline=(226, 232, 240), width=1)
    draw.text((50, card_y + 20), "CÓD 030613  ·  IPOJUCA / CAMELA", fill=(71, 85, 105), font=get_font("segoeuib.ttf", 10), anchor="lm")
    draw.text((50, card_y + 42), "Praça Pedro Serafim (Camela)", fill=(15, 23, 42), font=get_font("segoeuib.ttf", 16), anchor="lm")
    draw.text((50, card_y + 64), "Ref: Igreja Matriz / Mercado Público · Abrigo Coberto", fill=(100, 116, 139), font=get_font("segoeui.ttf", 11), anchor="lm")

    # Box de Previsão Imediata (ETA)
    eta_box_y = card_y + 78
    draw.rounded_rectangle([50, eta_box_y, W - 50, eta_box_y + 50], radius=10, fill=(236, 253, 245), outline=(167, 243, 208), width=1)
    draw.text((62, eta_box_y + 16), "PRÓXIMO LINHA 199:", fill=(4, 120, 87), font=get_font("segoeuib.ttf", 10), anchor="lm")
    draw.text((62, eta_box_y + 35), "Chega em 4 min (06:14)", fill=(6, 95, 70), font=get_font("segoeuib.ttf", 15), anchor="lm")
    # Botão Ouvir
    draw.rounded_rectangle([W - 148, eta_box_y + 10, W - 62, eta_box_y + 40], radius=8, fill=(16, 185, 129))
    draw.text((W - 105, eta_box_y + 25), "🔊 Ouvir", fill=(255, 255, 255), font=get_font("segoeuib.ttf", 12), anchor="mm")

    # Letreiro LED Idêntico ao Coletivo
    led_y = card_y + 152
    draw.rounded_rectangle([38, led_y, W - 38, led_y + 48], radius=10, fill=(0, 0, 0), outline=(245, 158, 11), width=2)
    draw.text((W//2, led_y + 24), "199  CAMELA / CABO VIA PE-60", fill=(245, 158, 11), font=get_font("segoeuib.ttf", 15), anchor="mm")

    # Card Minha Rotina Pendular
    rot_y = led_y + 58
    draw.rounded_rectangle([38, rot_y, W - 38, rot_y + 86], radius=12, fill=(240, 253, 244), outline=(187, 247, 208), width=1)
    draw.text((50, rot_y + 20), "📅 MINHA ROTINA · TURNO SUAPE 05h45", fill=(22, 101, 52), font=get_font("segoeuib.ttf", 11), anchor="lm")
    draw.text((50, rot_y + 42), "💡 Janela: Caminhada de 6 min. Saia de casa às 06:08.", fill=(15, 23, 42), font=get_font("segoeuib.ttf", 12), anchor="lm")
    draw.text((50, rot_y + 64), "👥 48 operários nesta rota alimentando a Central CTM.", fill=(71, 85, 105), font=get_font("segoeui.ttf", 11), anchor="lm")

    # 2 Botões Gigantes de Ação 1-Tap
    btn_y = rot_y + 96
    draw.rounded_rectangle([38, btn_y, W//2 - 6, btn_y + 68], radius=14, fill=(236, 253, 245), outline=(16, 185, 129), width=2)
    draw.text((W//4 + 16, btn_y + 24), "🏠 Vou pra Casa", fill=(6, 95, 70), font=get_font("segoeuib.ttf", 14), anchor="mm")
    draw.text((W//4 + 16, btn_y + 46), "Camela · 4 min", fill=(4, 120, 87), font=get_font("segoeui.ttf", 12), anchor="mm")

    draw.rounded_rectangle([W//2 + 6, btn_y, W - 38, btn_y + 68], radius=14, fill=(240, 249, 255), outline=(2, 132, 199), width=2)
    draw.text((3*W//4 - 16, btn_y + 24), "💼 Vou pro Destino", fill=(3, 105, 161), font=get_font("segoeuib.ttf", 14), anchor="mm")
    draw.text((3*W//4 - 16, btn_y + 46), "TI Cabo · 32 min", fill=(2, 132, 199), font=get_font("segoeui.ttf", 12), anchor="mm")

    # Guia Anti-Pânico
    panic_y = btn_y + 78
    draw.rounded_rectangle([38, panic_y, W - 38, panic_y + 44], radius=10, fill=(254, 242, 242), outline=(254, 202, 202), width=1)
    draw.text((50, panic_y + 22), "🧭 Primeira vez aqui ou perdido? Guia anti-pânico ➔", fill=(225, 29, 72), font=get_font("segoeuib.ttf", 11), anchor="lm")

    out_file = "va2/img/mockup_app_sem2.png"
    img.save(out_file, "PNG")
    print(f"[OK] Mockup do app gerado com sucesso: {out_file} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# ATIVO 2: GRÁFICO DA FALHA REAL - OVER-SMOOTHING (va2/img/grafico_falha_oversmoothing.png)
# ==============================================================================
def gerar_grafico_falha():
    W, H = 1100, 640
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((45, 35), "DEMONSTRAÇÃO DA FALHA: SUPER-SUAVIZAÇÃO ESPACIAL (OVER-SMOOTHING)", fill=DANGER_RED, font=get_font("segoeuib.ttf", 18))
    draw.text((45, 68), "Cenário Real: Bloqueio no Trevo de Ipojuca (Km 14 da PE-60) — Ônibus parado por 45 minutos", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 13))

    # Canvas do Gráfico
    gx, gy, gw, gh = 60, 110, 980, 310
    draw_rounded_card(draw, [gx, gy, gx + gw, gy + gh], radius=14, fill=CARD_BG, outline=CARD_BORDER)

    # Grid Lines
    for y_val, label in [(0, "0 min"), (15, "15 min"), (30, "30 min"), (45, "45 min")]:
        y_pos = gy + gh - 40 - int(y_val * 5.0)
        draw.line([(gx + 70, y_pos), (gx + gw - 40, y_pos)], fill=(31, 41, 55), width=1)
        draw.text((gx + 25, y_pos), label, fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11), anchor="lm")

    # Time Axis
    for t_val in [0, 10, 20, 30, 40, 50]:
        x_pos = gx + 80 + int(t_val * 16.5)
        draw.text((x_pos, gy + gh - 18), f"{t_val} min", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 11), anchor="mm")

    # Curva 1: GPS Real do Satélite (Salto Brusco no Bloqueio)
    gps_points = [
        (gx + 80, gy + gh - 40 - 25),
        (gx + 80 + 165, gy + gh - 40 - 30),
        (gx + 80 + 200, gy + gh - 40 - 225),  # Salto brusco aos 12 min
        (gx + 80 + 400, gy + gh - 40 - 225),
        (gx + 80 + 600, gy + gh - 40 - 225),
        (gx + 80 + 825, gy + gh - 40 - 225)
    ]
    draw.line(gps_points, fill=DANGER_RED, width=5)

    # Curva 2: STGCN com Convolução em Grafo (Laplaciana Suaviza o Salto)
    stgcn_points = [
        (gx + 80, gy + gh - 40 - 25),
        (gx + 80 + 165, gy + gh - 40 - 32),
        (gx + 80 + 240, gy + gh - 40 - 45),
        (gx + 80 + 360, gy + gh - 40 - 65),
        (gx + 80 + 500, gy + gh - 40 - 85),
        (gx + 80 + 825, gy + gh - 40 - 90)   # Estagna em 18 min!
    ]
    draw.line(stgcn_points, fill=AMBER, width=4)

    # Destaque de Divergência
    div_x = gx + 80 + 550
    draw.line([(div_x, gy + gh - 40 - 225), (div_x, gy + gh - 40 - 90)], fill=(255, 255, 255), width=2)
    draw.text((div_x + 12, gy + gh - 40 - 158), "GAP CRÍTICO: 27 MIN DE ERRO!", fill=DANGER_RED, font=get_font("segoeuib.ttf", 13), anchor="lm")

    # Legendas no Gráfico
    draw.rounded_rectangle([gx + gw - 320, gy + 16, gx + gw - 20, gy + 74], radius=8, fill=(10, 15, 29), outline=CARD_BORDER)
    draw.line([(gx + gw - 305, gy + 32), (gx + gw - 275, gy + 32)], fill=DANGER_RED, width=4)
    draw.text((gx + gw - 265, gy + 32), "GPS Real do Satélite (45 min)", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 11), anchor="lm")
    draw.line([(gx + gw - 305, gy + 56), (gx + gw - 275, gy + 56)], fill=AMBER, width=4)
    draw.text((gx + gw - 265, gy + 56), "Previsão STGCN Suavizada (18 min)", fill=AMBER, font=get_font("segoeuib.ttf", 11), anchor="lm")

    # 2 Caixas Explicativas Abaixo do Gráfico
    box_w = 475
    box_h = 175
    y_cards = 445

    # Card da Falha
    draw_rounded_card(draw, [60, y_cards, 60 + box_w, y_cards + box_h], radius=14, fill=DANGER_BG, outline=DANGER_RED)
    draw.text((80, y_cards + 26), "🔴 O QUE A IA ENTREGOU: 18 MINUTOS [?]", fill=DANGER_RED, font=get_font("segoeuib.ttf", 14), anchor="lm")
    msg_fail = (
        "• Como a STGCN usa convolução espacial com matriz Laplaciana, ela espalha\n"
        "  o atraso brusco para as paradas vizinhas, gerando uma curva atenuada.\n"
        "• A tela mostrava '18 min', mas o ônibus estava travado há 45 min no bloqueio.\n"
        "• QUEM SOFRE: O operário em Camela perde o turno na fábrica de Suape."
    )
    draw.text((80, y_cards + 54), msg_fail, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=5)

    # Card da Solução Híbrida
    draw_rounded_card(draw, [565, y_cards, 565 + box_w, y_cards + box_h], radius=14, fill=EMERALD_BG, outline=EMERALD)
    draw.text((585, y_cards + 26), "🛡️ A TRAVA HÍBRIDA DO GRAFOPARADA: SELO [?]", fill=EMERALD, font=get_font("segoeuib.ttf", 14), anchor="lm")
    msg_shield = (
        "• O GrafoParada NUNCA esconde o GPS bruto: criamos a Trava de Discrepância.\n"
        "• Se |STGCN - GPS| > 15 min, o app corta a previsão pura da IA, acende o\n"
        "  selo amarelo de alerta [?] e avisa por voz: 'Rodovia interditada'.\n"
        "• É a nossa métrica para o Sem3: quantas falhas a regra blinda no mundo real."
    )
    draw.text((585, y_cards + 54), msg_shield, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=5)

    out_file = "va2/img/grafico_falha_oversmoothing.png"
    img.save(out_file, "PNG")
    print(f"[OK] Gráfico da falha gerado: {out_file} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# ATIVO 3: GRÁFICO MAE: SEM1 VS SEM2 (va2/img/grafico_evolucao_mae.png)
# ==============================================================================
def gerar_grafico_evolucao_mae():
    W, H = 1100, 640
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((45, 35), "O QUE MUDOU DESDE O SEMINÁRIO 1: A IA ESPACIAL SE PAGOU?", fill=ACCENT_CYAN, font=get_font("segoeuib.ttf", 18))
    draw.text((45, 68), "De 5 paradas (corredor curto) para 20 paradas reais da PE-60 com GTFS do Grande Recife", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 13))

    # 2 Colunas de Gráficos de Barras
    col_w = 475
    col_h = 360
    y_cols = 115

    # COLUNA 1: SEMINÁRIO 1 (5 PARADAS)
    draw_rounded_card(draw, [60, y_cols, 60 + col_w, y_cols + col_h], radius=14, fill=CARD_BG, outline=CARD_BORDER)
    draw.text((85, y_cols + 32), "SEMINÁRIO 1 · CORREDOR CURTO (5 PARADAS)", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 12))
    draw.text((85, y_cols + 58), "A IA foi Derrotada pelo Cálculo Simples", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 16))

    # Barras Sem1
    # Barra Linear
    draw.rounded_rectangle([85, y_cols + 110, 85 + 246, y_cols + 155], radius=8, fill=ACCENT_BLUE)
    draw.text((85 + 246 + 15, y_cols + 132), "2,46 min", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 14), anchor="lm")
    draw.text((85, y_cols + 96), "Regressão Linear / Cinemática (Vencedora no Sem1)", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), anchor="lm")

    # Barra STGCN
    draw.rounded_rectangle([85, y_cols + 195, 85 + 442, y_cols + 240], radius=8, fill=(147, 51, 234))
    draw.text((85 + 442 + 15, y_cols + 217), "4,42 min", fill=DANGER_RED, font=get_font("segoeuib.ttf", 14), anchor="lm")
    draw.text((85, y_cols + 181), "STGCN (IA em Grafo - Perdeu no trecho curto)", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), anchor="lm")

    draw.rounded_rectangle([85, y_cols + 270, 60 + col_w - 25, y_cols + 335], radius=10, fill=(24, 30, 44), outline=CARD_BORDER)
    draw.text((95, y_cols + 302), "⚠️ Dilema no Sem1: A complexidade da STGCN não compensava\n     no corredor simples de 5 paradas. Promessa de testar na malha.", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 11), spacing=3)

    # COLUNA 2: SEMINÁRIO 2 (20 PARADAS PE-60)
    draw_rounded_card(draw, [565, y_cols, 565 + col_w, y_cols + col_h], radius=14, fill=CARD_BG, outline=EMERALD)
    draw.text((590, y_cols + 32), "SEMINÁRIO 2 · MALHA REAL PE-60 (20 PARADAS)", fill=EMERALD, font=get_font("segoeuib.ttf", 12))
    draw.text((590, y_cols + 58), "A STGCN Virou o Jogo e Venceu com Escala", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 16))

    # Barras Sem2
    # Persistência
    draw.rounded_rectangle([590, y_cols + 105, 590 + 350, y_cols + 135], radius=6, fill=(51, 65, 85))
    draw.text((590 + 350 + 15, y_cols + 120), "7,13 min", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 13), anchor="lm")
    draw.text((590, y_cols + 93), "Persistência Cega (Baseline)", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 10.5), anchor="lm")

    # Regressão Linear
    draw.rounded_rectangle([590, y_cols + 165, 590 + 193, y_cols + 200], radius=6, fill=ACCENT_BLUE)
    draw.text((590 + 193 + 15, y_cols + 182), "1,93 min", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 13), anchor="lm")
    draw.text((590, y_cols + 153), "Regressão Linear", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 10.5), anchor="lm")

    # STGCN
    draw.rounded_rectangle([590, y_cols + 230, 590 + 151, y_cols + 270], radius=8, fill=EMERALD)
    draw.text((590 + 151 + 15, y_cols + 250), "1,51 min (-78% de Erro!)", fill=EMERALD, font=get_font("segoeuib.ttf", 15), anchor="lm")
    draw.text((590, y_cols + 218), "STGCN Espaço-Temporal (VENCEDORA ABSOLUTA)", fill=EMERALD, font=get_font("segoeuib.ttf", 11), anchor="lm")

    draw.rounded_rectangle([590, y_cols + 290, 565 + col_w - 25, y_cols + 345], radius=10, fill=EMERALD_BG, outline=EMERALD)
    draw.text((600, y_cols + 317), "✅ Confirmação Empírica: Na malha real com atrasos propagados,\n     a IA em grafo superou os modelos clássicos por ampla margem.", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 11), spacing=3)

    # Card Inferior: A Grande Mudança Conceitual
    card_bot_y = y_cols + col_h + 20
    draw_rounded_card(draw, [60, card_bot_y, W - 60, card_bot_y + 115], radius=14, fill=CARD_BG, outline=ACCENT_BLUE)
    draw.text((85, card_bot_y + 24), "💡 A MAIOR MUDANÇA: DE RASTREADOR PASSIVO A REALOCADOR DE FROTA NO VAZIO", fill=ACCENT_CYAN, font=get_font("segoeuib.ttf", 13))
    msg_change = (
        "No Sem1, o app era apenas uma tela passiva de previsão. No Sem2, ele passou a entender a rotina dos trabalhadores\n"
        "(Suape 05h45) e dos idosos (Dona Severina), alimentando a Central CTM para remanejar ônibus ociosos que rodavam vazios\n"
        "na Linha 178 para socorrer quem aguardava no escuro da PE-60. A IA saiu do laboratório e virou serviço público."
    )
    draw.text((85, card_bot_y + 52), msg_change, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=4)

    out_file = "va2/img/grafico_evolucao_mae.png"
    img.save(out_file, "PNG")
    print(f"[OK] Gráfico de evolução MAE gerado: {out_file} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# ATIVO 4: CARD DE CUSTO MEDIDO VS ESTIMADO (va2/img/card_custo_medido.png)
# ==============================================================================
def gerar_card_custo():
    W, H = 1100, 640
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((45, 35), "QUANTO CUSTA: MEDIÇÃO REAL NO REPOSITÓRIO (medir_custo_sem2.py)", fill=ACCENT_BLUE, font=get_font("segoeuib.ttf", 18))
    draw.text((45, 68), "Ambiente de Teste: Intel Core CPU, Windows 11, Python 3.12 + PyTorch (Commit 565321f)", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 13))

    # 3 Cards de Métricas Principais
    cw = 315
    ch = 330
    y_pos = 120
    coords = [60, 60 + cw + 18, 60 + 2 * (cw + 18)]

    # CARD 1: NO APARELHO (CELULAR)
    draw_rounded_card(draw, [coords[0], y_pos, coords[0] + cw, y_pos + ch], radius=16, fill=CARD_BG, outline=EMERALD)
    draw.text((coords[0] + 24, y_pos + 30), "NO CELULAR (FSM V3)", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((coords[0] + 24, y_pos + 70), "4,98 ms", fill=EMERALD, font=get_font("segoeuib.ttf", 36))
    draw.text((coords[0] + 24, y_pos + 120), "12,0 KB de RAM", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 16))
    draw.line([(coords[0] + 24, y_pos + 155), (coords[0] + cw - 24, y_pos + 155)], fill=CARD_BORDER, width=1)
    
    msg_c1 = (
        "• flx estimava: 14,29 µs · 8,92 KB\n"
        "• 4,98 ms é a inferência completa\n"
        "  com Soft-Voting e cinemática.\n"
        "• Roda localmente sem travar.\n"
        "• ZERO impacto na bateria."
    )
    draw.text((coords[0] + 24, y_pos + 175), msg_c1, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=5)

    # CARD 2: NO SERVIDOR (STGCN 20 NÓS PE-60)
    draw_rounded_card(draw, [coords[1], y_pos, coords[1] + cw, y_pos + ch], radius=16, fill=CARD_BG, outline=ACCENT_CYAN)
    draw.text((coords[1] + 24, y_pos + 30), "NO SERVIDOR LOCAL (CTM)", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((coords[1] + 24, y_pos + 70), "0,77 ms", fill=ACCENT_CYAN, font=get_font("segoeuib.ttf", 36))
    draw.text((coords[1] + 24, y_pos + 120), "358,2 MB no Processo", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 16))
    draw.line([(coords[1] + 24, y_pos + 155), (coords[1] + cw - 24, y_pos + 155)], fill=CARD_BORDER, width=1)

    msg_c2 = (
        "• flx estimava: < 500 ms · ~300 MB\n"
        "• 0,77 ms na CPU por ciclo.\n"
        "• Tensores ativos ocupam 83,7 KB.\n"
        "• Processo PyTorch: 358 MB.\n"
        "• Explicação: Runtime carrega libs."
    )
    draw.text((coords[1] + 24, y_pos + 175), msg_c2, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=5)

    # CARD 3: CUSTO FINANCEIRO NA ESCALA
    draw_rounded_card(draw, [coords[2], y_pos, coords[2] + cw, y_pos + ch], radius=16, fill=CARD_BG, outline=EMERALD)
    draw.text((coords[2] + 24, y_pos + 30), "CUSTO FINANCEIRO TOTAL", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((coords[2] + 24, y_pos + 70), "R$ 0,00", fill=EMERALD, font=get_font("segoeuib.ttf", 36))
    draw.text((coords[2] + 24, y_pos + 120), "Zero Nuvem Paga", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 16))
    draw.line([(coords[2] + 24, y_pos + 155), (coords[2] + cw - 24, y_pos + 155)], fill=CARD_BORDER, width=1)

    msg_c3 = (
        "• 34.627 parâmetros totais.\n"
        "• Roda em computador comum de\n"
        "  escritório do Consórcio CTM.\n"
        "• Sem API paga de LLM externa.\n"
        "• 100% soberano e replicável."
    )
    draw.text((coords[2] + 24, y_pos + 175), msg_c3, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=5)

    # Banner Inferior Comparativo
    ban_y = y_pos + ch + 20
    draw_rounded_card(draw, [60, ban_y, W - 60, ban_y + 125], radius=14, fill=CARD_BG, outline=CARD_BORDER)
    draw.text((85, ban_y + 24), "📊 RESUMO DA AUDITORIA TÉCNICA · POR QUE O FLX ESTIMOU DIFERENTE?", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 13))
    msg_audit = (
        "A estimativa teórica do flx.md previa até 500 ms de inferência e 300 MB de RAM. A medição real revelou que a inferência pura\n"
        "da STGCN leva menos de 1 milissegundo (0,77 ms), porque matrizes de adjacência de 20 nós cabem no cache L2 da CPU Intel.\n"
        "A memória total do processo no SO (358 MB) reflete as DLLs dinâmicas do PyTorch, enquanto os pesos da rede consomem só 84 KB."
    )
    draw.text((85, ban_y + 52), msg_audit, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=4)

    out_file = "va2/img/card_custo_medido.png"
    img.save(out_file, "PNG")
    print(f"[OK] Card de custo gerado: {out_file} ({os.path.getsize(out_file):,} bytes)")

# ==============================================================================
# ATIVO 5: CARD DO BALANÇO FINAL E IMPACTO REAL (va2/img/card_realocacao_ctm.png)
# ==============================================================================
def gerar_card_balanco():
    W, H = 1100, 640
    img = Image.new("RGB", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Header
    draw.text((45, 35), "IMPACTO REAL NA MOBILIDADE: A DESISTÊNCIA NA PARADA FINANCIA O ÔNIBUS NO PICO", fill=EMERALD, font=get_font("segoeuib.ttf", 18))
    draw.text((45, 68), "Balanço Técnico e Econômico da Operação no Corredor PE-60 (Ipojuca ➔ Cabo de Santo Agostinho)", fill=TEXT_MUTED, font=get_font("segoeui.ttf", 13))

    # 4 Pilares
    pw = 230
    ph = 280
    y_pos = 120
    pxs = [60 + i * (pw + 18) for i in range(4)]

    # Pilar 1: Diesel
    draw_rounded_card(draw, [pxs[0], y_pos, pxs[0] + pw, y_pos + ph], radius=14, fill=CARD_BG, outline=EMERALD)
    draw.text((pxs[0] + 18, y_pos + 24), "COMBUSTÍVEL", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((pxs[0] + 18, y_pos + 60), "14 Litros", fill=EMERALD, font=get_font("segoeuib.ttf", 28))
    draw.text((pxs[0] + 18, y_pos + 100), "Poupar Diesel/h", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 14))
    draw.line([(pxs[0] + 18, y_pos + 128), (pxs[0] + pw - 18, y_pos + 128)], fill=CARD_BORDER, width=1)
    draw.text((pxs[0] + 18, y_pos + 144), "Ao evitar que a Linha\n178 rode vazia na\ncontramão (deadheading)\nsem passageiros.", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), spacing=3)

    # Pilar 2: Receita
    draw_rounded_card(draw, [pxs[1], y_pos, pxs[1] + pw, y_pos + ph], radius=14, fill=CARD_BG, outline=ACCENT_BLUE)
    draw.text((pxs[1] + 18, y_pos + 24), "ARRECADAÇÃO", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((pxs[1] + 18, y_pos + 60), "R$ 155,80", fill=ACCENT_CYAN, font=get_font("segoeuib.ttf", 28))
    draw.text((pxs[1] + 18, y_pos + 100), "Receita Preservada", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 14))
    draw.line([(pxs[1] + 18, y_pos + 128), (pxs[1] + pw - 18, y_pos + 128)], fill=CARD_BORDER, width=1)
    draw.text((pxs[1] + 18, y_pos + 144), "Evita que os 48\ntrabalhadores desistam\ndo ônibus para pegar\no 'ligeirinho' ilegal.", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), spacing=3)

    # Pilar 3: VEM
    draw_rounded_card(draw, [pxs[2], y_pos, pxs[2] + pw, y_pos + ph], radius=14, fill=CARD_BG, outline=AMBER)
    draw.text((pxs[2] + 18, y_pos + 24), "BOLSO DO USUÁRIO", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((pxs[2] + 18, y_pos + 60), "R$ 4,10", fill=AMBER, font=get_font("segoeuib.ttf", 28))
    draw.text((pxs[2] + 18, y_pos + 100), "VEM Blindado", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 14))
    draw.line([(pxs[2] + 18, y_pos + 128), (pxs[2] + pw - 18, y_pos + 128)], fill=CARD_BORDER, width=1)
    draw.text((pxs[2] + 18, y_pos + 144), "Guardião da Janela\nde 120 min de Integração\nTemporal no TI Cabo\ncontra cobrança dupla.", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), spacing=3)

    # Pilar 4: Privacidade
    draw_rounded_card(draw, [pxs[3], y_pos, pxs[3] + pw, y_pos + ph], radius=14, fill=CARD_BG, outline=(147, 51, 234))
    draw.text((pxs[3] + 18, y_pos + 24), "PRIVACIDADE", fill=TEXT_MUTED, font=get_font("segoeuib.ttf", 11))
    draw.text((pxs[3] + 18, y_pos + 60), "166 Bytes", fill=(192, 132, 252), font=get_font("segoeuib.ttf", 28))
    draw.text((pxs[3] + 18, y_pos + 100), "Rotina no Celular", fill=TEXT_WHITE, font=get_font("segoeuib.ttf", 14))
    draw.line([(pxs[3] + 18, y_pos + 128), (pxs[3] + pw - 18, y_pos + 128)], fill=CARD_BORDER, width=1)
    draw.text((pxs[3] + 18, y_pos + 144), "A rotina nunca sai do\naparelho. O CTM só\nrecebe a contagem\nanônima da parada.", fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11), spacing=3)

    # Box Inferior: Conexão com o Seminário 3 (Experimento de Campo)
    exp_y = y_pos + ph + 24
    draw_rounded_card(draw, [60, exp_y, W - 60, exp_y + 150], radius=16, fill=(15, 23, 42), outline=EMERALD, width=2)
    draw.text((85, exp_y + 26), "🔬 O QUE VEM NO SEMINÁRIO 3 · EXPERIMENTO DE CAMPO NA PE-60 (25/11)", fill=EMERALD, font=get_font("segoeuib.ttf", 14))
    msg_exp = (
        "No Sem3, no dia 25/11, levaremos a medição para o ponto de ônibus real na PE-60 em Camela com passageiros de verdade.\n"
        "A falha mostrada hoje (o over-smoothing da STGCN em bloqueios) é a primeira candidata a virar medida lá:\n"
        "Quantas vezes a trava híbrida de discrepância protegeu o trabalhador contra a previsão suave da IA antes da catraca?\n"
        "Esse é o rigor científico: a falha de hoje vira a hipótese testada e comprovada em campo no próximo seminário."
    )
    draw.text((85, exp_y + 56), msg_exp, fill=TEXT_LIGHT, font=get_font("segoeui.ttf", 11.5), spacing=4)

    out_file = "va2/img/card_realocacao_ctm.png"
    img.save(out_file, "PNG")
    print(f"[OK] Card de balanço gerado: {out_file} ({os.path.getsize(out_file):,} bytes)")

if __name__ == "__main__":
    gerar_mockup_smartphone()
    gerar_grafico_falha()
    gerar_grafico_evolucao_mae()
    gerar_card_custo()
    gerar_card_balanco()
    print("[FINALIZADO] Todos os ativos visuais foram criados com sucesso!")
