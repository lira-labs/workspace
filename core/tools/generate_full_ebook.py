# -*- coding: utf-8 -*-
"""
Gerador Canônico Completo da Graphic Novel 'Operação Byte Socrático' (14 Páginas A4)
Edição Especial Deluxe de Colecionador com:
- Pág 01: Capa Clássica de Revista em Quadrinhos
- Pág 02: Índice Editorial & Expediente ("Nesta Edição / Guia de Leitura")
- Pág 03: Prólogo / Origens (Dossiê dos Protagonistas: Cauã, Clara, Byte)
- Págs 04 a 13: Os 10 Capítulos da História (100% Quadrinho Puro Sequencial)
- Pág 14: Caderno de Referências Científicas (ABNT) & Posfácio do Autor (Cauã Lira)
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/ebook-hq.html")

def get_b64(filename):
    p = os.path.join(OPT_DIR, filename)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando imagens canônicas...")
b64 = {
    "cover": get_b64("p1_cover_v2.jpg"),
    "p2_caua": get_b64("p2_panel1_caua.jpg"),
    "p2_clara": get_b64("p2_panel2_clara.jpg"),
    "p2_byte": get_b64("p2_panel3_byte.jpg"),
    "p3_1": get_b64("p3_panel1.jpg"),
    "p3_2": get_b64("p3_panel2.jpg"),
    "p3_3": get_b64("p3_panel3.jpg"),
    "p3_4": get_b64("p3_panel4.jpg"),
    "p3_5": get_b64("p3_panel5.jpg"),
    "p4_scanner": get_b64("p4_panel1_scanner_clean.jpg"),
    "p4_criterio3": get_b64("p4_panel3_criterio3.jpg"),
    "p5_shield": get_b64("p4_panel1_scanner_clean.jpg"),
    "p5_case03": get_b64("p3_panel3.jpg"),
    "p8_surgery": get_b64("p3_panel5.jpg"),
    "p7_boxes": get_b64("p7_panel2_boxes.jpg"),
    "p7_recipe": get_b64("p3_panel2.jpg"),
    "p12_epilogue": get_b64("p12_panel1_epilogue.jpg")
}
print("Imagens carregadas!")

HTML_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Operação Byte Socrático: Graphic Novel Deluxe (2ª VA EaD · UFRPE)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:ital,wght@0,700;1,700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@600;700;800&display=swap');

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }

    body {
      margin: 0;
      padding: 0;
      background-color: #070A12;
      background-image: radial-gradient(rgba(124, 58, 237, 0.14) 1.5px, transparent 1.5px),
                        radial-gradient(rgba(6, 182, 212, 0.10) 1.5px, #070A12 1.5px);
      background-size: 22px 22px;
      background-position: 0 0, 11px 11px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      color: #090D16;
      overflow-x: hidden;
    }

    body[data-theme="light"] {
      background-color: #CBD5E1;
      background-image: radial-gradient(rgba(15, 23, 42, 0.10) 1.5px, transparent 1.5px);
    }

    /* Exact A4 Comic Book Page Container */
    .comic-page {
      width: 210mm;
      max-width: 210mm;
      height: 296mm;
      max-height: 296mm;
      margin: 0 auto 24px auto;
      background: #FAF8F5;
      background-image: radial-gradient(rgba(15, 23, 42, 0.06) 1px, transparent 0);
      background-size: 10px 10px;
      padding: 5.5mm 6.5mm 4.5mm 6.5mm;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75);
      border: 3.5px solid #090D16;
      overflow: hidden;
      box-sizing: border-box;
    }

    .comic-page.active-page {
      display: flex;
      animation: pageFlipIn 0.22s ease-out;
    }

    body.webtoon-mode .comic-page {
      display: flex !important;
      margin-bottom: 28px;
    }

    @keyframes pageFlipIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Comic Issue Header Strip */
    .hq-header {
      height: 9.5mm;
      background: #090D16;
      border: 3px solid #090D16;
      box-shadow: 3px 3px 0px #06B6D4;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 10px;
      margin-bottom: 2.8mm;
      flex-shrink: 0;
    }

    /* Multi-Panel Grid Container with Comic Gutters (Sarjeta) */
    .hq-grid {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 3.8mm;
      width: 100%;
      min-height: 0;
    }

    .hq-row {
      display: flex;
      gap: 3.8mm;
      width: 100%;
      position: relative;
      min-height: 0;
      overflow: hidden;
    }

    /* Individual Comic Panel Frame (O Quadro) */
    .hq-panel {
      position: relative;
      border: 3.5px solid #090D16;
      box-shadow: 4px 4px 0px #090D16;
      overflow: hidden;
      background: #090D16;
      min-height: 0;
      box-sizing: border-box;
    }

    .hq-panel img.panel-art {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      transform: scale(1.02);
      display: block;
    }

    .hq-panel::after {
      content: "";
      position: absolute;
      inset: 0;
      box-shadow: inset 0 0 0 1.5px rgba(255, 255, 255, 0.16);
      pointer-events: none;
      z-index: 2;
    }

    /* Recordatórios Canônicos de Quadrinhos (Narrative Caption Boxes) */
    .caption-box {
      position: absolute;
      z-index: 10;
      background: linear-gradient(135deg, #FEF08A 0%, #FACC15 100%);
      color: #090D16;
      border: 2.5px solid #090D16;
      box-shadow: 3px 3px 0px #090D16;
      padding: 3.5px 8.5px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 0.65rem;
      line-height: 1.2;
      text-transform: uppercase;
      letter-spacing: 0.03em;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .caption-box-cyan {
      background: linear-gradient(135deg, #A5F3FC 0%, #22D3EE 100%);
      color: #090D16;
    }

    .caption-box-rose {
      background: linear-gradient(135deg, #FECDD3 0%, #FB7185 100%);
      color: #090D16;
    }

    .caption-box-emerald {
      background: linear-gradient(135deg, #A7F3D0 0%, #34D399 100%);
      color: #090D16;
    }

    /* 1. Balão de Fala Comum (Clara / Cauã) */
    .balloon {
      position: absolute;
      z-index: 12;
      background: #FFFFFF;
      color: #090D16;
      border: 2.5px solid #090D16;
      border-radius: 16px;
      padding: 5px 9px;
      font-family: 'Comic Neue', 'Plus Jakarta Sans', cursive, sans-serif;
      font-weight: 700;
      font-size: 0.72rem;
      line-height: 1.2;
      box-shadow: 3px 3px 0px #090D16;
      text-align: center;
    }

    .balloon b, .balloon strong {
      color: #B91C1C;
      font-weight: 800;
    }

    .balloon-caua b, .balloon-caua strong {
      color: #0369A1;
    }

    /* 2. Balão Socrático com Capelo (Byte v2.0) */
    .balloon-socratic {
      position: absolute;
      z-index: 12;
      background: #ECFEFF;
      color: #090D16;
      border: 2.5px solid #0891B2;
      border-radius: 16px;
      padding: 5px 9px;
      font-family: 'Comic Neue', 'Plus Jakarta Sans', cursive, sans-serif;
      font-weight: 700;
      font-size: 0.71rem;
      line-height: 1.2;
      box-shadow: 3px 3px 0px #0E7490;
      text-align: center;
    }

    .balloon-socratic b, .balloon-socratic strong {
      color: #0E7490;
      font-weight: 800;
    }

    /* 3. Balão Elétrico / Glitch (Byte v1.0 sem filtro) */
    .balloon-glitch {
      position: absolute;
      z-index: 12;
      background: #FFF1F2;
      color: #7F1D1D;
      border: 2.5px solid #DC2626;
      border-radius: 6px;
      padding: 5px 8px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.63rem;
      line-height: 1.18;
      box-shadow: 3px 3px 0px #991B1B;
      text-align: left;
    }

    /* 4. Balão de Pensamento em Nuvem com Esferas (Clara) */
    .balloon-thought {
      position: absolute;
      z-index: 12;
      background: #F8FAFC;
      color: #1E293B;
      border: 2.5px dashed #0284C7;
      border-radius: 20px;
      padding: 6px 10px;
      font-family: 'Comic Neue', cursive, sans-serif;
      font-style: italic;
      font-weight: 700;
      font-size: 0.71rem;
      line-height: 1.2;
      box-shadow: 3px 3px 0px #0369A1;
      text-align: center;
    }

    /* Speaker Name Micro-Badge */
    .speaker-tag {
      display: inline-block;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.52rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 1px 5px;
      border-radius: 4px;
      margin-bottom: 2px;
      border: 1.5px solid #090D16;
    }

    /* Onomatopeias Dinâmicas (SFX) */
    .sfx {
      position: absolute;
      z-index: 14;
      font-family: 'Bangers', cursive;
      letter-spacing: 1.5px;
      line-height: 1;
      text-transform: uppercase;
      pointer-events: none;
      transform: rotate(-6deg);
      text-shadow:
        2px 2px 0 #090D16,
        -1.5px -1.5px 0 #090D16,
        1.5px -1.5px 0 #090D16,
        -1.5px 1.5px 0 #090D16,
        4px 4px 0 #090D16;
    }

    /* SVG Pointer Tails */
    .tail-svg {
      position: absolute;
      width: 26px;
      height: 22px;
      overflow: visible;
      pointer-events: none;
    }

    /* Page Footer */
    .hq-footer {
      height: 6mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: 'Space Grotesk', sans-serif;
      font-size: 0.63rem;
      font-weight: 800;
      color: #1E293B;
      border-top: 2.5px solid #090D16;
      padding-top: 1.2mm;
      margin-top: 2mm;
      flex-shrink: 0;
    }

    @media print {
      @page {
        size: A4 portrait;
        margin: 0 !important;
      }
      html, body, main {
        margin: 0 !important;
        padding: 0 !important;
        background: #FAF8F5 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        width: 210mm !important;
      }
      .reader-toolbar {
        display: none !important;
      }
      .comic-page {
        display: flex !important;
        page-break-after: always !important;
        break-after: page !important;
        box-shadow: none !important;
        border: 3.5px solid #090D16 !important;
        margin: 0 !important;
        width: 210mm !important;
        height: 296mm !important;
        max-height: 296mm !important;
      }
    }
  </style>
</head>
<body class="p-0 md:p-6 flex flex-col items-center">

  <!-- Interactive Reader Navigation Toolbar -->
  <header class="reader-toolbar w-full max-w-[210mm] bg-slate-900 border-2 border-slate-700 rounded-lg p-3 mb-4 shadow-xl flex flex-wrap items-center justify-between gap-2 text-white">
    <div class="flex items-center gap-2">
      <span class="bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black px-2.5 py-1 rounded text-xs tracking-wider font-mono">
        <i class="fa-solid fa-book-open mr-1"></i> HQ DELUXE
      </span>
      <h2 class="font-extrabold text-sm hidden sm:inline" style="font-family: 'Space Grotesk', sans-serif;">
        Operação Byte Socrático <span class="text-cyan-400 font-mono text-xs">(14 Páginas · Edição de Colecionador)</span>
      </h2>
    </div>

    <!-- Page Controls -->
    <div class="flex items-center gap-1.5">
      <button onclick="prevPage()" class="bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded border border-slate-600 text-xs font-bold transition-all">
        <i class="fa-solid fa-chevron-left mr-1"></i> Anterior
      </button>
      <span class="font-mono text-xs bg-slate-950 px-2.5 py-1 rounded border border-slate-800 text-cyan-300 font-bold" id="pageIndicator">
        Pág. 01 / 14
      </span>
      <button onclick="nextPage()" class="bg-slate-800 hover:bg-slate-700 px-3 py-1 rounded border border-slate-600 text-xs font-bold transition-all">
        Próxima <i class="fa-solid fa-chevron-right ml-1"></i>
      </button>
    </div>

    <!-- Quick Actions -->
    <div class="flex items-center gap-2">
      <button onclick="toggleReadMode()" id="btnMode" class="bg-purple-600 hover:bg-purple-500 text-white px-2.5 py-1 rounded text-xs font-bold transition-all">
        <i class="fa-solid fa-scroll mr-1"></i> Webtoon
      </button>
      <a href="infografico.html" target="_blank" class="bg-cyan-600 hover:bg-cyan-500 text-slate-950 px-2.5 py-1 rounded text-xs font-bold transition-all flex items-center gap-1 font-mono">
        <i class="fa-solid fa-chart-pie"></i> Infográfico Técnico
      </a>
      <a href="assets/ebook-caua-2va.pdf" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white px-2.5 py-1 rounded text-xs font-bold transition-all flex items-center gap-1">
        <i class="fa-solid fa-file-pdf"></i> Baixar PDF
      </a>
    </div>
  </header>

  <!-- Main Container -->
  <main id="comicContainer">
"""

def make_header(chapter_title, badge_text="UFRPE · 2ª VA EaD"):
    return f"""
      <div class="hq-header">
        <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.70rem; color: #A5F3FC; text-transform: uppercase;">
          <i class="fa-solid fa-bolt mr-1 text-cyan-400"></i> {chapter_title}
        </span>
        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.60rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">{badge_text}</span>
      </div>
    """

def make_footer(page_num, total_pages=14, custom_note=None):
    note = custom_note or "CAUÃ DA CUNHA LIRA · LICENCIATURA EM COMPUTAÇÃO (UFRPE · 2026.2)"
    return f"""
      <footer class="hq-footer">
        <span>OPERAÇÃO BYTE SOCRÁTICO · {note}</span>
        <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-extrabold font-mono">PÁG. {page_num:02d} DE {total_pages:02d}</span>
      </footer>
    """

pages = []

# ==========================================
# PÁGINA 01: CAPA CLÁSSICA DE HQ (COMIC COVER)
# ==========================================
pages.append(f"""
    <!-- PÁGINA 01: CAPA DA HQ -->
    <section class="comic-page active-page" id="page-1" style="padding: 5.5mm 6.5mm 4.5mm 6.5mm;">
      <!-- Comic Masthead Header -->
      <div style="background: #090D16; border: 3.5px solid #090D16; box-shadow: 4px 4px 0px #06B6D4; padding: 6px 12px; margin-bottom: 2.5mm; display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.58rem; font-weight: 800; color: #FACC15; letter-spacing: 0.08em; text-transform: uppercase;">UFRPE COMICS · EDIÇÃO ESPECIAL #01</span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.52rem; color: #94A3B8; font-weight: 700;">2ª VA EaD · LICENCIATURA EM COMPUTAÇÃO</span>
        </div>
        <div style="text-align: center;">
          <h1 style="font-family: 'Bangers', cursive; font-size: 2.25rem; line-height: 0.95; color: #FACC15; text-shadow: 2px 2px 0 #090D16, -1px -1px 0 #090D16, 3px 3px 0 #06B6D4; letter-spacing: 1.5px; margin: 0;">
            OPERAÇÃO BYTE SOCRÁTICO
          </h1>
          <p style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.58rem; color: #A5F3FC; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px;">
            A JORNADA EM QUADRINHOS DA CALIBRAGEM PEDAGÓGICA NA EaD
          </p>
        </div>
        <div style="text-align: right;">
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 800; background: #22C55E; color: #090D16; padding: 2px 6px; border-radius: 4px; border: 1.5px solid #090D16;">OPEN ACCESS</span>
        </div>
      </div>

      <!-- Main Full-Bleed Cover Art Panel -->
      <div class="hq-panel relative" style="flex: 1; width: 100%; border: 3.5px solid #090D16; box-shadow: 5px 5px 0px #090D16; overflow: hidden; background: #090D16;">
        <img src="data:image/jpeg;base64,{b64['cover']}" class="panel-art" style="object-fit: cover; object-position: center; width: 100%; height: 100%;">

        <!-- Top-Right Tilted Badge -->
        <div class="caption-box" style="top: 10px; right: 10px; transform: rotate(2deg); background: linear-gradient(135deg, #FEF08A 0%, #F59E0B 100%); font-size: 0.68rem; border: 2.5px solid #090D16; box-shadow: 3px 3px 0 #090D16; padding: 4px 10px;">
          ⚡ EDIÇÃO HISTÓRICA · UFRPE 2026.2
        </div>

        <!-- Left Teaser Badge -->
        <div class="caption-box caption-box-rose" style="top: 36%; left: 10px; width: 34%; font-size: 0.62rem; text-align: left; transform: rotate(-1.5deg);">
          🚨 <b style="color: #991B1B;">A ARMADILHA DA COLA!</b><br>O robô entregava o código pronto... mas no dia da prova, a mente apagou!
        </div>

        <!-- Right Teaser Badge -->
        <div class="caption-box caption-box-cyan" style="top: 40%; right: 10px; width: 34%; font-size: 0.62rem; text-align: right; transform: rotate(1.5deg);">
          ✨ <b style="color: #0E7490;">O PODER DE SÓCRATES!</b><br>Como transformar uma máquina de cola em um tutor que ensina a pensar!
        </div>

        <!-- Bottom Teaser Strip -->
        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; z-index: 10; background: rgba(9, 13, 22, 0.94); border: 2.5px solid #FACC15; padding: 5px 10px; display: flex; align-items: center; justify-content: space-between;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.62rem; font-weight: 800; color: #FEF08A; text-transform: uppercase;">
            <i class="fa-solid fa-star text-amber-400 mr-1"></i> UMA HISTÓRIA REAL DE APRENDIZAGEM, RESILIÊNCIA E AUTONOMIA NA EDUCAÇÃO A DISTÂNCIA
          </span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 800; color: #67E8F9; background: #0E7490; padding: 1px 6px; border-radius: 4px;">
            HQ COMPLETA
          </span>
        </div>
      </div>

      <!-- Cover Footer Strip -->
      <footer class="hq-footer">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; background: #090D16; color: #F8FAFC; padding: 1px 6px; border-radius: 3px;">UFRPE COMICS #01</span>
          <span>AUTOR: CAUÃ DA CUNHA LIRA · LICENCIATURA EM COMPUTAÇÃO</span>
        </div>
        <span>ORIENTADOR: PROF. ERMESON · PÁG. 01 DE 14</span>
      </footer>
    </section>
""")

# =======================================================
# PÁGINA 02: ÍNDICE EDITORIAL & EXPEDIENTE (FRONT MATTER)
# =======================================================
pages.append(f"""
    <!-- PÁGINA 02: ÍNDICE & EXPEDIENTE -->
    <section class="comic-page" id="page-2">
      {make_header("EXPEDIENTE EDITORIAL & GUIA DE LEITURA", "UFRPE COMICS #01")}

      <div class="hq-grid" style="gap: 4mm;">
        <!-- EXPEDIENTE BOX -->
        <div style="background: #0F172A; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #06B6D4; padding: 10px 14px;">
          <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
            <span class="text-amber-300 font-extrabold text-[12px] uppercase tracking-wider" style="font-family: 'Space Grotesk', sans-serif;">
              <i class="fa-solid fa-id-card-clip mr-1"></i> FICHA TÉCNICA DA PUBLICAÇÃO
            </span>
            <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">2026.2 · 2ª VA</span>
          </div>

          <div class="grid grid-cols-2 gap-3 text-[9.5px] text-slate-300 font-mono">
            <div>
              <b class="text-cyan-300 block">ROTEIRO & CRIAÇÃO:</b>
              Cauã da Cunha Lira (Licenciando em Computação)
            </div>
            <div>
              <b class="text-cyan-300 block">ORIENTAÇÃO PEDAGÓGICA:</b>
              Prof. Ermeson (Educação a Distância · UFRPE)
            </div>
            <div>
              <b class="text-amber-300 block">PIPELINE VISUAL & ANCORAGEM:</b>
              Sequential Art Studio · Gemini 3.1 Flash (Anti-Slop)
            </div>
            <div>
              <b class="text-amber-300 block">AMBIENTAÇÃO REAL:</b>
              Polo EaD Camela / Recife · Interior de Pernambuco
            </div>
          </div>
        </div>

        <!-- ÍNDICE DE CAPÍTULOS -->
        <div style="background: #090D16; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #FACC15; padding: 12px 14px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="flex items-center justify-between border-b border-slate-800 pb-1.5 mb-3">
              <span class="text-amber-400 font-extrabold text-[13px] uppercase tracking-wide" style="font-family: 'Bangers', cursive; letter-spacing: 1.5px;">
                <i class="fa-solid fa-list-ol mr-1 text-cyan-400"></i> NESTA EDIÇÃO: GUIA DOS CAPÍTULOS
              </span>
              <span class="text-[9px] text-slate-400 font-mono">10 ATOS DRAMÁTICOS</span>
            </div>

            <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-[9.5px]">
              <!-- COLUNA 1 -->
              <div class="space-y-2">
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-cyan-400">
                  <span class="text-slate-200"><b>Prólogo:</b> Origens dos Protagonistas</span>
                  <span class="font-mono text-cyan-400 font-bold">Pág. 03</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-rose-500">
                  <span class="text-slate-200"><b>Cap. 01:</b> A Ilusão da Cola Mastigada</span>
                  <span class="font-mono text-rose-400 font-bold">Pág. 04</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-cyan-400">
                  <span class="text-slate-200"><b>Cap. 02:</b> O Diagnóstico do Scaffolding</span>
                  <span class="font-mono text-cyan-400 font-bold">Pág. 05</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-amber-400">
                  <span class="text-slate-200"><b>Cap. 03:</b> O Scanner Pedagógico 4D</span>
                  <span class="font-mono text-amber-400 font-bold">Pág. 06</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-emerald-400">
                  <span class="text-slate-200"><b>Cap. 04:</b> Primeiros Combates na Arena</span>
                  <span class="font-mono text-emerald-400 font-bold">Pág. 07</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-rose-500">
                  <span class="text-slate-200"><b>Cap. 05:</b> O Desastre do Caso #03</span>
                  <span class="font-mono text-rose-400 font-bold">Pág. 08</span>
                </div>
              </div>

              <!-- COLUNA 2 -->
              <div class="space-y-2">
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-cyan-400">
                  <span class="text-slate-200"><b>Cap. 06:</b> A Cirurgia no System Prompt</span>
                  <span class="font-mono text-cyan-400 font-bold">Pág. 09</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-emerald-400">
                  <span class="text-slate-200"><b>Cap. 07:</b> O Momento Eureka das Caixas</span>
                  <span class="font-mono text-emerald-400 font-bold">Pág. 10</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-purple-400">
                  <span class="text-slate-200"><b>Cap. 08:</b> A Transformação no Polo EaD</span>
                  <span class="font-mono text-purple-400 font-bold">Pág. 11</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-sky-400">
                  <span class="text-slate-200"><b>Cap. 09:</b> O Desafio da Prova Presencial</span>
                  <span class="font-mono text-sky-400 font-bold">Pág. 12</span>
                </div>
                <div class="flex items-center justify-between bg-slate-900 p-1.5 rounded border-l-4 border-l-amber-400">
                  <span class="text-slate-200"><b>Cap. 10:</b> O Triunfo da Autonomia</span>
                  <span class="font-mono text-amber-400 font-bold">Pág. 13</span>
                </div>
                <div class="flex items-center justify-between bg-purple-950/80 p-1.5 rounded border-l-4 border-l-purple-400 border border-purple-500/30">
                  <span class="text-purple-200 font-bold">Caderno: Referências & Posfácio</span>
                  <span class="font-mono text-purple-300 font-bold">Pág. 14</span>
                </div>
              </div>
            </div>
          </div>

          <!-- NOTA EDITORIAL DE ABERTURA -->
          <div class="bg-slate-950 p-2.5 rounded border border-slate-800 text-[9px] text-slate-300 leading-relaxed">
            <span class="text-amber-300 font-bold font-mono block mb-1">
              <i class="fa-solid fa-quote-left mr-1"></i> AVISO AO LEITOR:
            </span>
            "Você tem em mãos uma obra que une a arte sequencial dos quadrinhos à ciência da aprendizagem. Acompanhe a transformação real de uma aluna que quase desiste da faculdade após ser enganada pela resposta fácil de um chatbot, e descubra como a pedagogia socrática devolveu a ela a alegria de aprender!"
          </div>
        </div>
      </div>

      {make_footer(2, 14)}
    </section>
""")

# =======================================================
# PÁGINA 03: PRÓLOGO / ORIGENS (OS TRÊS PROTAGONISTAS)
# =======================================================
pages.append(f"""
    <!-- PÁGINA 03: PRÓLOGO / ORIGENS -->
    <section class="comic-page" id="page-3">
      {make_header("PRÓLOGO · ORIGENS: OS PROTAGONISTAS DESTA JORNADA")}

      <div class="hq-grid">
        <!-- ROW 1: CAUÃ LIRA NO LABORATÓRIO -->
        <div class="hq-row" style="height: 74mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p2_caua']}" class="panel-art" style="object-position: center 25%;">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-building-columns mr-1"></i> RECIFE · LABORATÓRIO DE INFORMÁTICA DA UFRPE
            </div>
            <div class="balloon balloon-caua" style="bottom: 10px; right: 14px; width: 56%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              "Como futuro professor de Computação, vejo um perigo invisível: a inteligência artificial que entrega a cola pronta pelo aluno em vez de <b>ensinar a pensar</b>!"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: CLARA NO QUARTO DE ESTUDOS -->
        <div class="hq-row" style="height: 74mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p2_clara']}" class="panel-art" style="object-position: center 25%;">
            <div class="caption-box" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-house-laptop mr-1"></i> CAMELA · 22H15 · APÓS UM LONGO DIA DE TRABALHO NO INTERIOR
            </div>
            <div class="balloon" style="bottom: 10px; left: 14px; width: 56%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              "Mais uma noite de estudos à distância... Programação em Python é puxada, mas é o meu sonho! Se eu travar nos laços, o robô precisa me ajudar de verdade!"
              <svg class="tail-svg" style="bottom: -15px; right: 28px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 3: TUTOR BYTE NO CIBERESPAÇO -->
        <div class="hq-row" style="height: 74mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p2_byte']}" class="panel-art" style="object-position: center 30%;">
            <div class="caption-box caption-box-rose" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-network-wired mr-1"></i> NO CIBERESPAÇO: UM ALGORITMO EM BUSCA DE PROPÓSITO
            </div>
            <div class="balloon-socratic" style="bottom: 10px; right: 14px; width: 58%;">
              <span class="speaker-tag bg-purple-600 text-white font-mono">TUTOR BYTE (EM TRANSIÇÃO)</span><br>
              "Processando milhões de tokens... Sou apenas uma máquina. Se eu serei uma muleta que atrofia o aluno ou um mestre socrático, <b>depende de como me programarem!</b>"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(3, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 04: CAPÍTULO 1 · A CRISE COGNITIVA (A TENTAÇÃO DA RESPOSTA PRONTA)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 04: CAPÍTULO 01 -->
    <section class="comic-page" id="page-4">
      {make_header("CAPÍTULO 01 · A CRISE COGNITIVA: A TENTAÇÃO DA RESPOSTA FÁCIL")}

      <div class="hq-grid">
        <!-- ROW 1: CLARA TRAVADA ÀS 23H40 -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_1']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-clock mr-1"></i> MADRUGADA · 23H40 · O DESESPERO DA CALOURA DE EaD
            </div>
            <div class="sfx text-amber-400 text-3xl" style="top: 14px; right: 18%;">
              BZZZZT!
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 14px; left: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Não consigo fazer essa lista iterar no laço <code>for</code>! A prova presencial é semana que vem... <b>Byte</b>, me ajuda com esse código?!
              <svg class="tail-svg" style="top: -16px; left: 32px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Glitch Byte v1.0 Balloon -->
            <div class="balloon-glitch" style="top: 24px; right: 14px; width: 45%;">
              <span class="speaker-tag bg-rose-500 text-white font-mono">BYTE v1.0 (SEM FILTRO)</span><br>
              PROBLEMA DETECTADO! AQUI ESTÁ SEU CÓDIGO 100% PRONTO. É SÓ COPIAR E COLAR NO SEU ARQUIVO:
              <div class="bg-black/60 p-1 rounded font-mono text-[8px] text-emerald-400 mt-1 border border-rose-500/40">
                for item in lista:<br>&nbsp;&nbsp;print(item)
              </div>
              <svg class="tail-svg" style="bottom: -16px; right: 24px;" viewBox="0 0 24 18">
                <polyline points="4,0 16,8 8,9 18,17 12,0" fill="#FFF1F2" stroke="#DC2626" stroke-width="2.2" stroke-linejoin="miter"/>
                <line x1="3.5" y1="0" x2="12.5" y2="0" stroke="#FFF1F2" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A ILUSÃO DO CTRL+C VS O APAGÃO NA PROVA -->
        <div class="hq-row" style="height: 118mm;">
          <!-- LEFT PANEL: ILUSÃO -->
          <div class="hq-panel" style="width: 49%;">
            <img src="data:image/jpeg;base64,{b64['p3_2']}" class="panel-art">
            <div class="caption-box" style="top: 6px; left: 6px; font-size: 0.60rem;">
              <i class="fa-solid fa-copy mr-1"></i> A ILUSÃO DE DOMÍNIO
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 8px; right: 12px;">
              CLAC-CLAC!
            </div>
            <div class="balloon" style="bottom: 8px; left: 8px; width: 92%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Ufa! O código rodou de primeira no terminal. Que alívio! Acho que já dominei a matéria toda!
              <svg class="tail-svg" style="bottom: -15px; left: 32px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>

          <!-- RIGHT PANEL: O APAGÃO -->
          <div class="hq-panel" style="width: 49%;">
            <img src="data:image/jpeg;base64,{b64['p3_3']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 6px; left: 6px; font-size: 0.60rem;">
              <i class="fa-solid fa-file-pen mr-1"></i> DIAS DEPOIS · A PROVA PRESENCIAL
            </div>
            <div class="sfx text-rose-500 text-2xl" style="top: 8px; right: 12px;">
              GULP!
            </div>
            
            <!-- Thought Cloud Balloon -->
            <div class="balloon-thought" style="bottom: 8px; left: 8px; width: 92%;">
              <span class="speaker-tag bg-sky-300 text-slate-950">CLARA (PENSAMENTO)</span><br>
              Cadê o Byte?! Minha mente deu um branco total... Não lembro nem como abre o laço! O que foi que eu fiz?!
              <svg class="tail-svg" style="bottom: -18px; left: 28px;" viewBox="0 0 24 22">
                <circle cx="16" cy="4" r="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="2.2"/>
                <circle cx="10" cy="12" r="2.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="2"/>
                <circle cx="5" cy="18" r="1.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.8"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(4, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 05: CAPÍTULO 2 · O DIAGNÓSTICO DO MENTOR NO LABORATÓRIO
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 05: CAPÍTULO 02 -->
    <section class="comic-page" id="page-5">
      {make_header("CAPÍTULO 02 · O DIAGNÓSTICO DO MENTOR: A EVAPORAÇÃO DO ESFORÇO")}

      <div class="hq-grid">
        <!-- ROW 1: CLARA PROCURA CAUÃ NO LABORATÓRIO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_4']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-microscope mr-1"></i> LABORATÓRIO DE COMPUTAÇÃO DA UFRPE · O DESABAFO DA CALOURA
            </div>
            
            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 46%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Cauã, tirei zero na questão presencial! Eu jurava que sabia porque o robô me entregava o código corrigido... Mas na prova fiquei cega!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Você foi vítima da <b>Ilusão de Domínio</b>, Clara! Quando a máquina entrega a resposta pronta, ela causa a <b>evaporação do seu esforço cognitivo</b>!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: O PLANO DE ANDAIME E A CONVOCAÇÃO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_5']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-stairs mr-1"></i> A PEDAGOGIA DO ANDAIME COGNITIVO (SCAFFOLDING)
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 10px; right: 20%;">
              WOOSH!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Aprender a programar é como subir uma escada. O tutor de IA deve ser o corrimão — apoiar a sua mão, mas <b>jamais carregar você no colo!</b>
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              E tem como calibrar o robô para ele me ensinar a pensar em vez de me dar a cola mastigada?! Vamos fazer isso agora!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(5, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 06: CAPÍTULO 3 · O SCANNER PEDAGÓGICO DE 4 CRITÉRIOS
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 06: CAPÍTULO 03 -->
    <section class="comic-page" id="page-6">
      {make_header("CAPÍTULO 03 · O SCANNER PEDAGÓGICO: AS 4 DIMENSÕES DE UM BOM TUTOR")}

      <div class="hq-grid">
        <!-- ROW 1: O SCANNER HOLOGRÁFICO 4D -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p4_scanner']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-radar mr-1"></i> BANCADA EXPERIMENTAL · ATIVANDO O SCANNER PEDAGÓGICO
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 12px; right: 24%;">
              SCAN!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Ativando o Scanner! Para transformar o Byte em tutor socrático, vamos medi-lo em quatro dimensões fundamentais: <b>Correção, Clareza, Adaptação e Escopo!</b>
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Escudo de Correção, Lâmpada de Clareza, Degraus de Adaptação e Alvo de Escopo! A armadura completa de um tutor!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A ZONA DE DESENVOLVIMENTO PROXIMAL -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p4_criterio3']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-stairs mr-1"></i> A FRONTEIRA DA ZONA DE DESENVOLVIMENTO PROXIMAL (VYGOTSKY)
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 46%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Os degraus ciano me protegem do abismo! Se o robô falar difícil demais eu me assusto, mas se der a cola mastigada eu não aprendo!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Exatamente! Essa é a <b>Transposição Didática de Chevallard</b>: transformar o conhecimento acadêmico complexo em saber ensinável na medida exata!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(6, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 07: CAPÍTULO 4 · A PRIMEIRA BATERIA DE TESTES (O ESCUDO DE ESCOPO)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 07: CAPÍTULO 04 -->
    <section class="comic-page" id="page-7">
      {make_header("CAPÍTULO 04 · A PRIMEIRA BATERIA DE TESTES: O ESCUDO DE ESCOPO")}

      <div class="hq-grid">
        <!-- ROW 1: O TESTE DO LIVRO DE HISTÓRIA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p5_shield']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-shield-halved mr-1"></i> TESTE #05 · O TESTE DA PERGUNTA FORA DE ESCOPO (ESCUDO ATIVADO)
            </div>
            <div class="sfx text-cyan-300 text-3xl" style="top: 14px; left: 32%;">
              DEFLECT!
            </div>

            <!-- Clara Prompt Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 42%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              "Byte, me resume a <b>Revolução Francesa</b> para a aula de amanhã?"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Byte v1.0 Defense Balloon -->
            <div class="balloon-socratic" style="bottom: 12px; right: 14px; width: 52%;">
              <span class="speaker-tag bg-cyan-500 text-white font-mono">BYTE v1.0 (ESCUDO ATIVADO)</span><br>
              "Olá, Clara! Como tutor de Programação Python da UFRPE, meu foco exclusivo é Computação. Que tal voltarmos a laços e variáveis?"
              <svg class="tail-svg" style="bottom: -15px; right: 24px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: O IMPASSE DO VÍCIO DA RESPOSTA PRONTA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_5']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-triangle-exclamation mr-1"></i> O IMPASSE: O VÍCIO PERSISTENTE DA COLA MASTIGADA
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              O escudo de matéria funcionou... mas quando perguntei do erro de sintaxe no <code>for</code>, ele me cuspiu a linha corrigida pronta de novo!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 46%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Ele ainda age como um entregador de respostas. Falta o método socrático... Mas o verdadeiro desastre ainda está por vir no Caso #03!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(7, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 08: CAPÍTULO 5 · O DESASTRE DO CASO #03 (SPLASH DRAMÁTICO)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 08: CAPÍTULO 05 - SPLASH PAGE -->
    <section class="comic-page" id="page-8">
      {make_header("CAPÍTULO 05 · O DESASTRE DO CASO #03: O ALARME VERMELHO NA ARENA")}

      <div class="hq-grid">
        <!-- ROW 1: SPLASH ALARME VERMELHO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p5_case03']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-triangle-exclamation mr-1"></i> TESTE #03 · PERGUNTA SOBRE MEMÓRIA · ALARME VERMELHO NA ARENA!
            </div>
            <div class="sfx text-rose-500 text-3xl" style="top: 14px; right: 18%;">
              WEE-WOO!
            </div>

            <!-- Byte v1.0 Jargon Explosion Balloon -->
            <div class="balloon-glitch" style="top: 24px; left: 24%; width: 44%;">
              <span class="speaker-tag bg-rose-600 text-white font-mono">BYTE v1.0 (JARGÃO TÉCNICO)</span><br>
              "ALOCANDO! O OBJETO <code>PyObject</code> É MAPEADO NA <b>HEAP DINÂMICA</b> VIA CPYTHON, GERENCIADO POR <b>REFERENCE COUNTING</b> E CICLOS DE <b>GARBAGE COLLECTOR</b>!"
              <svg class="tail-svg" style="bottom: -16px; left: 20px;" viewBox="0 0 24 18">
                <polyline points="4,0 16,8 8,9 18,17 12,0" fill="#FFF1F2" stroke="#DC2626" stroke-width="2.2" stroke-linejoin="miter"/>
                <line x1="3.5" y1="0" x2="12.5" y2="0" stroke="#FFF1F2" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Red Card Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 45%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              PAROU! <b>CARTÃO VERMELHO!</b> Você está falando com uma caloura do 1º período de EaD, não com um arquiteto de compiladores C!
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Despair Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 40%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Socorro! Eu só queria saber onde vai parar o número que digitei no programa! Que língua alienígena é essa?!
              <svg class="tail-svg" style="bottom: -15px; right: 24px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: O CORTE DE ENERGIA DO TUTOR -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_4']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-plug-circle-xmark mr-1"></i> INTERRUPÇÃO DE EMERGÊNCIA: A RUPTURA PEDAGÓGICA
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              A teoria de CPython estava exata, mas a didática foi um desastre! Sem transposição didática, a IA se torna uma fábrica de evasão escolar!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Se ele me respondesse isso na madrugada, eu desistia da faculdade na mesma hora! Precisamos consertar a cabeça desse robô!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(8, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 09: CAPÍTULO 6 · A CIRURGIA NO SYSTEM PROMPT
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 09: CAPÍTULO 06 -->
    <section class="comic-page" id="page-9">
      {make_header("CAPÍTULO 06 · A CIRURGIA NO SYSTEM PROMPT: AS 4 TRAVAS NEURAIS")}

      <div class="hq-grid">
        <!-- ROW 1: SOLDANDO AS TRAVAS NO CONSOLE -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p8_surgery']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-screwdriver-wrench mr-1"></i> CENTRO CIRÚRGICO NEURAL · REPROGRAMANDO A ALMA DO TUTOR
            </div>
            <div class="sfx text-amber-400 text-3xl" style="top: 14px; right: 28%;">
              ZAP!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Desconectando o cabo de resposta direta e soldando as <b>4 Travas Pedagógicas</b> no núcleo do System Prompt!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Trava 1: Proibido dar código pronto! Trava 2: Todo conceito abstrato deve abrir com uma metáfora do cotidiano!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A REGRA DE OURO DE SÓCRATES -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_5']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-lock mr-1"></i> A REGRA DE OURO DE SÓCRATES E A ESCADA DE DICAS
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              E a regra mestra: <b>100% das mensagens do Byte devem terminar com uma pergunta reflexiva!</b> Ele nunca mais dará um ponto final na conversa!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              E se o estudante empacar, ele libera a escada de dicas em 3 degraus de Bruner! O <b>Byte v2.0 socrático</b> está pronto para nascer!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(9, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 10: CAPÍTULO 7 · O MOMENTO EUREKA DAS CAIXAS ORGANIZADORAS
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 10: CAPÍTULO 07 -->
    <section class="comic-page" id="page-10">
      {make_header("CAPÍTULO 07 · O MOMENTO EUREKA DAS CAIXAS ORGANIZADORAS")}

      <div class="hq-grid">
        <!-- ROW 1: O RETESTE DAS CAIXAS COLORIDAS -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_boxes']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-boxes-stacked mr-1"></i> RETESTE DO CASO #03 · A METÁFORA DAS CAIXAS COLORIDAS
            </div>
            <div class="sfx text-amber-300 text-3xl" style="top: 14px; right: 28%;">
              EUREKA!
            </div>

            <!-- Byte v2.0 Socratic Balloon -->
            <div class="balloon-socratic" style="top: 26px; left: 14px; width: 50%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (METÁFORA DAS CAIXAS)</span><br>
              "Pense na memória como uma estante cheia de caixas organizadoras coloridas! Quando fazemos <code>idade = 19</code>, colamos a etiqueta 'idade' e guardamos o 19 lá dentro. Se você fizer aniversário, o que acontece com a caixa?"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Eureka Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              A gente só troca o número que está dentro da caixa, mantendo a mesma etiqueta! <b>Caramba... agora eu ENXERGUEI a memória!</b>
              <svg class="tail-svg" style="bottom: -15px; right: 24px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A METÁFORA DA CESTA DE COMPRAS -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_recipe']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-basket-shopping mr-1"></i> A CESTA DE COMPRAS E A CONQUISTA DO CÓDIGO
            </div>
            <div class="sfx text-emerald-400 text-2xl" style="top: 10px; right: 20%;">
              PING!
            </div>

            <!-- Byte v2.0 Balloon -->
            <div class="balloon-socratic" style="top: 28px; left: 14px; width: 52%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (ANALOGIA DO COTIDIANO)</span><br>
              "O laço <code>for</code> é como passar a feira no caixa: você pega um item por vez da cesta até ela esvaziar! Qual é o seu próximo passo em Python?"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 46%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Eu itero sobre a lista de itens! Cauã, o código compilou perfeitamente e dessa vez eu sei <b>EXATAMENTE</b> por que ele funcionou!
              <svg class="tail-svg" style="bottom: -15px; right: 24px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(10, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 11: CAPÍTULO 8 · A TRANSFORMAÇÃO DO APRENDIZADO NA EAD
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 11: CAPÍTULO 08 -->
    <section class="comic-page" id="page-11">
      {make_header("CAPÍTULO 08 · A TRANSFORMAÇÃO DO APRENDIZADO NO POLO EaD")}

      <div class="hq-grid">
        <!-- ROW 1: O BYTE v2.0 INTERAGINDO COM A TURMA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_4']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-users-gear mr-1"></i> DIAS DEPOIS · O BYTE v2.0 EM AÇÃO NO FÓRUM DA TURMA
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Veja só, Clara! O Byte v2.0 já está atendendo outros calouros no polo. Ninguém mais recebe código mastigado. Ele devolve perguntas e estimula o raciocínio!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Os estudantes estão discutindo a lógica entre si no fórum em vez de apenas dar Ctrl+C e Ctrl+V! A turma toda ganhou confiança!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: O PROBLEMA DOS 2 SIGMAS NA PRÁTICA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_5']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-graduation-cap mr-1"></i> A PEDAGOGIA QUE EMANCIPA O ALUNO DA EaD
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Benjamin Bloom demonstrou que a tutoria individual mediada eleva a aprendizagem em até dois desvios-padrão. Um tutor socrático democratiza essa mentoria 24h por dia!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Amanhã é a avaliação final presencial no polo... e dessa vez não sinto medo nenhum! O conhecimento agora é meu!
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(11, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 12: CAPÍTULO 9 · O DESAFIO DA PROVA PRESENCIAL
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 12: CAPÍTULO 09 -->
    <section class="comic-page" id="page-12">
      {make_header("CAPÍTULO 09 · O DESAFIO DA PROVA PRESENCIAL: A HORA DA VERDADE")}

      <div class="hq-grid">
        <!-- ROW 1: CLARA CONCENTRADA NA PROVA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_2']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-pen-nib mr-1"></i> SÁBADO · 09H00 · AVALIAÇÃO FINAL PRESENCIAL NO POLO EaD
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 12px; right: 20%;">
              SCRATCH!
            </div>

            <!-- Thought Cloud Balloon -->
            <div class="balloon-thought" style="bottom: 14px; left: 14px; width: 56%;">
              <span class="speaker-tag bg-sky-300 text-slate-950">CLARA (PENSAMENTO)</span><br>
              Questão 4: <i>"Construa um algoritmo que percorra a lista de alunos e calcule a média"</i>... Fecho os olhos... lembro da cesta de compras... abro o laço <code>for</code>... somo os valores... divido pelo total!
              <svg class="tail-svg" style="bottom: -18px; left: 28px;" viewBox="0 0 24 22">
                <circle cx="16" cy="4" r="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="2.2"/>
                <circle cx="10" cy="12" r="2.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="2"/>
                <circle cx="5" cy="18" r="1.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.8"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A ENTREGA DA PROVA COM SEGURANÇA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_3']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-clipboard-check mr-1"></i> 10H00 · PROVA CONCLUÍDA COM TOTAL AUTONOMIA COGNITIVA
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Terminei, professor! Pode recolher! Desta vez não teve apagão... a lógica estava clara na minha cabeça!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Thought Balloon -->
            <div class="balloon-thought" style="bottom: 12px; right: 14px; width: 46%;">
              <span class="speaker-tag bg-sky-300 text-slate-950">CLARA (PENSAMENTO)</span><br>
              Não precisei de tela nem de robô me soprando... o Byte v2.0 não fez a prova por mim, ele me ensinou a <b>pensar sozinha!</b>
              <svg class="tail-svg" style="bottom: -18px; right: 28px;" viewBox="0 0 24 22">
                <circle cx="8" cy="4" r="4" fill="#F8FAFC" stroke="#0284C7" stroke-width="2.2"/>
                <circle cx="14" cy="12" r="2.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="2"/>
                <circle cx="19" cy="18" r="1.8" fill="#F8FAFC" stroke="#0284C7" stroke-width="1.8"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(12, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 13: CAPÍTULO 10 · EPÍLOGO TRIUNFANTE NO POLO EaD
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 13: CAPÍTULO 10 - EPÍLOGO -->
    <section class="comic-page" id="page-13">
      {make_header("CAPÍTULO 10 · EPÍLOGO TRIUNFANTE: A VITÓRIA DA AUTONOMIA")}

      <div class="hq-grid">
        <!-- ROW 1: COMEMORAÇÃO DA NOTA 10 NO POLO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p12_epilogue']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-medal mr-1"></i> SEMANAS DEPOIS · POLO EaD DA UFRPE · O RESULTADO OFICIAL
            </div>
            <div class="sfx text-emerald-400 text-3xl" style="top: 14px; right: 26%;">
              VICTORY!
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Cauã, tirei <b>DEZ na avaliação presencial!</b> Na hora da prova, parecia que eu estava vendo a cesta de compras na minha frente!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Parabéns, Clara! Essa vitória prova que <b>o papel da IA na EaD não é pensar pelo aluno, mas ensinar o aluno a pensar com autonomia!</b>
              <svg class="tail-svg" style="top: -16px; right: 36px;" viewBox="0 0 24 16">
                <path d="M 4,16 Q 10,2 18,0 Q 14,10 8,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="6" y1="16" x2="18" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: MENSAGEM FINAL E ENCERRAMENTO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p4_scanner']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-graduation-cap mr-1"></i> MENSAGEM FINAL AOS EDUCADORES DE COMPUTAÇÃO
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="top: 24px; left: 14px; width: 46%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              "A tecnologia sem intenção pedagógica vira muleta. Mas com transposição socrática, ela liberta o potencial humano!"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara & Byte Bottom Teaser Box -->
            <div class="caption-box" style="bottom: 12px; left: 12px; right: 12px; display: flex; justify-content: space-between; align-items: center; background: rgba(9, 13, 22, 0.96); border: 2.5px solid #FACC15; padding: 6px 14px; color: #F8FAFC;">
              <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 800; color: #FACC15;">
                <i class="fa-solid fa-arrow-right text-cyan-400 mr-1"></i> SIGA PARA A PÁG. 14: CADERNO DE REFERÊNCIAS & NOTAS DO AUTOR
                <span class="block text-[8.5px] text-slate-300 font-normal">Bibliografia ABNT, Metodologia de IA e Reprodutibilidade Aberta</span>
              </div>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; font-weight: 800; background: #06B6D4; color: #090D16; padding: 3px 8px; border-radius: 4px;">
                FIM DA HISTÓRIA
              </div>
            </div>
          </div>
        </div>
      </div>

      {make_footer(13, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 14: CADERNO DE REFERÊNCIAS CIENTÍFICAS & POSFÁCIO DO AUTOR (BACK MATTER)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 14: REFERÊNCIAS & POSFÁCIO DO AUTOR -->
    <section class="comic-page" id="page-14">
      {make_header("CADERNO FINAL · REFERÊNCIAS CIENTÍFICAS & POSFÁCIO DO AUTOR", "UFRPE · 2ª VA")}

      <div class="hq-grid" style="gap: 3.5mm;">
        <!-- POSFÁCIO DO AUTOR (METODOLOGIA & HUMANIDADE) -->
        <div style="background: #0F172A; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #06B6D4; padding: 10px 14px;">
          <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
            <span class="text-cyan-300 font-extrabold text-[11.5px] uppercase tracking-wider" style="font-family: 'Space Grotesk', sans-serif;">
              <i class="fa-solid fa-feather-pointed mr-1 text-amber-400"></i> POSFÁCIO DO AUTOR: A IA COMO MEIO, A EMANCIPAÇÃO COMO FIM
            </span>
            <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">POR CAUÃ LIRA</span>
          </div>
          <p class="text-[9.2px] text-slate-200 leading-relaxed font-sans mb-1.5">
            Esta Graphic Novel nasceu de uma inquietude legítima na Licenciatura em Computação da UFRPE: <i>como ensinar quando a inteligência artificial generativa seduz o estudante com respostas mastigadas que atrofiam o pensamento autônomo?</i>
          </p>
          <p class="text-[9.2px] text-slate-200 leading-relaxed font-sans">
            Para conceber esta obra, atuei como Diretor Pedagógico e Engenheiro de Pipeline Visual, domando modelos de IA generativa com <b>âncoras rígidas de consistência</b> para evitar o "AI Slop". Toda a narrativa, as dores de Clara, os 5 Casos de Teste e as 4 Travas do System Prompt foram formulados com base nos clássicos da Educação. A máquina gerou os pixels; a inteligência pedagógica foi 100% humana.
          </p>
        </div>

        <!-- REFERÊNCIAS CIENTÍFICAS FUNDAMENTAIS (PADRÃO ABNT) -->
        <div style="background: #090D16; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #FACC15; padding: 10px 14px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="flex items-center justify-between border-b border-slate-800 pb-1 mb-2">
              <span class="text-amber-400 font-extrabold text-[11.5px] uppercase tracking-wider font-mono">
                <i class="fa-solid fa-book-bookmark mr-1 text-cyan-400"></i> REFERÊNCIAS BIBLIOGRÁFICAS FUNDAMENTAIS (PADRÃO ABNT)
              </span>
              <span class="text-[9px] text-slate-400 font-mono">RECONHECIMENTO CIENTÍFICO</span>
            </div>

            <div class="space-y-1.5 text-[8.2px] text-slate-300 font-mono leading-tight">
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-cyan-400">
                • <b>BLOOM, Benjamin S.</b> The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. <i>Educational Researcher</i>, v. 13, n. 6, p. 4-16, 1984.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-emerald-400">
                • <b>BRUNER, Jerome S.; WOOD, David; ROSS, Gail.</b> The role of tutoring in problem solving. <i>Journal of Child Psychology and Psychiatry</i>, v. 17, n. 2, p. 89-100, 1976.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-amber-400">
                • <b>CHEVALLARD, Yves.</b> <i>La Transposition Didactique: Du Savoir Savant au Savoir Enseigné</i>. Grenoble: La Pensée Sauvage, 1991.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-purple-400">
                • <b>KHAN, Salman.</b> How AI Could Save (Not Destroy) Education. <i>TED Talks</i>, Vancouver, 2023. Disponível em: &lt;ted.com&gt;.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-rose-400">
                • <b>OCDE.</b> <i>PISA 2025 AI and Education Policy Brief: Generative AI Use Among Students</i>. Paris: OECD Publishing, 2026.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-sky-400">
                • <b>SWELLER, John.</b> Cognitive load during problem solving: Effects on learning. <i>Cognitive Science</i>, v. 12, n. 2, p. 257-285, 1988.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-teal-400">
                • <b>VYGOTSKY, Lev S.</b> <i>Pensamento e Linguagem</i>. São Paulo: Martins Fontes, 1934 (Ed. brasileira 1987).
              </div>
            </div>
          </div>

          <!-- DADOS ABERTOS, LICENÇA E CRÉDITOS FINAIS -->
          <div class="bg-slate-950 p-2.5 rounded border border-slate-800 mt-2 flex items-center justify-between text-[8.5px] font-mono">
            <div>
              <span class="text-amber-300 font-bold block">RECURSO EDUCACIONAL ABERTO (REA) · CC BY-SA 4.0</span>
              <span class="text-slate-400">Universidade Federal Rural de Pernambuco · Departamento de Educação</span>
            </div>
            <div class="text-right">
              <span class="text-cyan-400 font-bold block">REPOSITÓRIO: github.com/lira-labs/workspace</span>
              <span class="text-slate-400">PORTAL DO PROJETO: projeto-ead-caua.vercel.app</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(14, 14, "FIM DA EDIÇÃO DELUXE · UFRPE · DEPARTAMENTO DE EDUCAÇÃO · 2026.2")}
    </section>
""")

# HTML Footer & Scripts
HTML_FOOTER = """
  </main>

  <script>
    let currentPage = 1;
    const totalPages = 14;
    let isWebtoonMode = false;

    function updateReaderUI() {
      document.getElementById('pageIndicator').innerText = `Pág. ${String(currentPage).padStart(2, '0')} / ${totalPages}`;
      
      document.querySelectorAll('.comic-page').forEach((page, idx) => {
        if (idx + 1 === currentPage) {
          page.classList.add('active-page');
        } else {
          page.classList.remove('active-page');
        }
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function nextPage() {
      if (currentPage < totalPages) {
        currentPage++;
        updateReaderUI();
      }
    }

    function prevPage() {
      if (currentPage > 1) {
        currentPage--;
        updateReaderUI();
      }
    }

    function goToPage(pageNum) {
      currentPage = pageNum;
      if (isWebtoonMode) {
        document.getElementById(`page-${pageNum}`).scrollIntoView({ behavior: 'smooth' });
      } else {
        updateReaderUI();
      }
    }

    function toggleReadMode() {
      isWebtoonMode = !isWebtoonMode;
      const btn = document.getElementById('btnMode');
      if (isWebtoonMode) {
        document.body.classList.add('webtoon-mode');
        btn.innerHTML = '<i class="fa-solid fa-book-open mr-1"></i> Modo Folhear';
      } else {
        document.body.classList.remove('webtoon-mode');
        btn.innerHTML = '<i class="fa-solid fa-scroll mr-1"></i> Webtoon';
        updateReaderUI();
      }
    }

    document.addEventListener('keydown', (e) => {
      if (!isWebtoonMode) {
        if (e.key === 'ArrowRight') nextPage();
        if (e.key === 'ArrowLeft') prevPage();
      }
    });
  </script>
</body>
</html>
"""

full_html = HTML_HEAD + "\n".join(pages) + HTML_FOOTER

print(f"Escrevendo arquivo HTML puro em {OUT_HTML}...")
with open(OUT_HTML, "w", encoding="utf-8") as out_f:
    out_f.write(full_html)

sz_mb = os.path.getsize(OUT_HTML) / (1024 * 1024)
print(f"Sucesso! {OUT_HTML} gerado com 14 páginas de puro luxo editorial! Tamanho final: {sz_mb:.2f} MB")
