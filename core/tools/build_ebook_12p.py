# -*- coding: utf-8 -*-
"""
Builder para o eBook em Quadrinhos 'Operação Byte Socrático' (12 Páginas A4)
2ª VA · Educação a Distância (UFRPE · 2026.2)
Autor: Cauã da Cunha Lira
Orientador: Prof. Ermeson
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/ebook-hq.html")

def get_b64(filename):
    p = os.path.join(OPT_DIR, filename)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando imagens Base64...")
b64_cover = get_b64("p1_cover_v2.jpg")
b64_p2_caua = get_b64("p2_panel1_caua.jpg")
b64_p2_byte = get_b64("p2_panel3_byte.jpg")
b64_p3_1 = get_b64("p3_panel1.jpg")
b64_p3_2 = get_b64("p3_panel2.jpg")
b64_p3_3 = get_b64("p3_panel3.jpg")
b64_p3_4 = get_b64("p3_panel4.jpg")
b64_p3_5 = get_b64("p3_panel5.jpg")
b64_p4_scanner = get_b64("p4_panel1_scanner_clean.jpg")
b64_p4_criterio3 = get_b64("p4_panel3_criterio3.jpg")
b64_p5_shield = get_b64("p5_panel5_shield.jpg")
b64_p5_case03 = get_b64("p5_panel4_case03.jpg")
b64_p8_surgery = get_b64("p8_panel1_surgery.jpg")
b64_p7_boxes = get_b64("p7_panel2_boxes.jpg")
b64_p7_recipe = get_b64("p7_panel3_recipe_clean.jpg")
b64_p12_epilogue = get_b64("p12_panel1_epilogue.jpg")
print("16 imagens Base64 carregadas com sucesso!")

# Shared HTML Header & Styles
HTML_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Operação Byte Socrático: Guia em Quadrinhos (2ª VA EaD · UFRPE)</title>
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
      background-image: radial-gradient(rgba(15, 23, 42, 0.075) 1px, transparent 0);
      background-size: 10px 10px;
      padding: 5.5mm 6.5mm 4.5mm 6.5mm;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.75);
      border: 3px solid #090D16;
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

    /* Multi-Panel Grid Container */
    .hq-grid {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 3mm;
      width: 100%;
      min-height: 0;
    }

    .hq-row {
      display: flex;
      gap: 3mm;
      width: 100%;
      position: relative;
      min-height: 0;
      overflow: hidden;
    }

    /* Individual Comic Panel Frame */
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

    /* Classic Yellow Comic Narrative Caption Box (Recordatório) */
    .caption-box {
      position: absolute;
      z-index: 10;
      background: linear-gradient(135deg, #FEF08A 0%, #FACC15 100%);
      color: #090D16;
      border: 2.5px solid #090D16;
      box-shadow: 3px 3px 0px #090D16;
      padding: 3.5px 8px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 0.65rem;
      line-height: 1.2;
      text-transform: uppercase;
      letter-spacing: 0.02em;
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

    /* Authentic Comic Speech Balloons with SVG Pointer Tails */
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

    /* Robotic Glitch Balloon (Byte v1.0) */
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

    /* Thought Cloud Balloon */
    .balloon-thought {
      position: absolute;
      z-index: 12;
      background: #F8FAFC;
      color: #1E293B;
      border: 2.5px dashed #0284C7;
      border-radius: 20px;
      padding: 5px 10px;
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

    /* Comic Sound Effects (Onomatopeias) */
    .sfx {
      position: absolute;
      z-index: 14;
      font-family: 'Bangers', cursive;
      letter-spacing: 1px;
      line-height: 1;
      text-transform: uppercase;
      pointer-events: none;
      text-shadow:
        2px 2px 0 #090D16,
        -1.5px -1.5px 0 #090D16,
        1.5px -1.5px 0 #090D16,
        -1.5px 1.5px 0 #090D16,
        4px 4px 0 #090D16;
    }

    /* Score Badge (Unbroken Single Line) */
    .score-badge {
      white-space: nowrap !important;
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.66rem;
      padding: 2px 7px;
      border-radius: 5px;
      border: 2px solid #090D16;
      box-shadow: 2px 2px 0px #090D16;
      letter-spacing: 0;
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
        page-break-inside: avoid !important;
        break-inside: avoid !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 5.5mm 6.5mm 4.5mm 6.5mm !important;
        width: 210mm !important;
        max-width: 210mm !important;
        height: 296mm !important;
        max-height: 296mm !important;
        border: none !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
      }
      .comic-page:last-of-type, #page-12 {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }
    }
  </style>
</head>
<body>

  <!-- Floating Sticky Reader Controls Toolbar -->
  <header class="reader-toolbar sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b-2 border-purple-500/40 px-3 py-2 shadow-2xl">
    <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-2 text-white">
      <div class="flex items-center gap-2">
        <a href="index.html" class="flex items-center gap-1.5 text-xs font-bold text-cyan-400 hover:text-cyan-300 transition-colors bg-slate-900 border border-cyan-500/30 px-2.5 py-1.5 rounded-lg shadow-sm">
          <i class="fa-solid fa-arrow-left"></i> Hub
        </a>
        <div class="flex items-center gap-1.5">
          <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span class="font-extrabold text-sm tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-purple-300 to-cyan-300">
            OPERAÇÃO BYTE SOCRÁTICO
          </span>
          <span class="bg-purple-900/80 text-purple-200 border border-purple-400/40 text-[10px] font-bold px-1.5 py-0.5 rounded uppercase">
            12 PÁGINAS · HQ EXPANDIDA
          </span>
        </div>
      </div>

      <!-- Page Quick-Jump Pills (1 to 12) -->
      <div class="flex items-center gap-1 overflow-x-auto py-0.5">
        <button onclick="goToPage(1)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-purple-600 text-white font-bold whitespace-nowrap">01</button>
        <button onclick="goToPage(2)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">02</button>
        <button onclick="goToPage(3)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">03</button>
        <button onclick="goToPage(4)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">04</button>
        <button onclick="goToPage(5)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">05</button>
        <button onclick="goToPage(6)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">06</button>
        <button onclick="goToPage(7)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">07</button>
        <button onclick="goToPage(8)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">08</button>
        <button onclick="goToPage(9)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">09</button>
        <button onclick="goToPage(10)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">10</button>
        <button onclick="goToPage(11)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">11</button>
        <button onclick="goToPage(12)" class="page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap">12</button>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-1.5">
        <button onclick="prevPage()" class="px-2.5 py-1 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-lg border border-slate-700 transition-colors">
          <i class="fa-solid fa-chevron-left"></i> Ant
        </button>
        <span id="pageIndicator" class="text-xs font-bold text-amber-300 font-mono px-1">Pág. 1 de 12</span>
        <button onclick="nextPage()" class="px-2.5 py-1 text-xs bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-lg transition-colors">
          Próx <i class="fa-solid fa-chevron-right"></i>
        </button>
        <button onclick="toggleReadMode()" id="btnMode" class="ml-1 px-2.5 py-1 text-xs bg-cyan-900/60 hover:bg-cyan-800/80 text-cyan-200 font-bold rounded-lg border border-cyan-500/40 transition-colors">
          <i class="fa-solid fa-scroll mr-1"></i> Webtoon
        </button>
        <a href="assets/ebook-operacao-byte-socratico.pdf" target="_blank" class="px-2.5 py-1 text-xs bg-emerald-700 hover:bg-emerald-600 text-white font-bold rounded-lg transition-colors shadow-sm flex items-center gap-1">
          <i class="fa-solid fa-file-pdf"></i> Baixar PDF
        </a>
      </div>
    </div>
  </header>

  <main class="w-full py-4">
"""

print("HTML_HEAD pronto!")
