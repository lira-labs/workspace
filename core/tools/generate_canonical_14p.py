# -*- coding: utf-8 -*-
"""
Gerador Canônico da Graphic Novel 'Operação Byte Socrático' (Edição Especial #01 · 14 Páginas A4)
Edição Enxuta, 100% Quadrinho Sequencial, sem AI Slop (UFRPE · Polo EaD Recife)
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/ebook-hq.html")

def get_b64(filename):
    p = os.path.join(OPT_DIR, filename)
    if not os.path.exists(p):
        # fallback to assets/hq
        p = os.path.abspath(os.path.join("code/projeto_ead_tutores/assets/hq", filename))
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando imagens canônicas em alta resolução...")
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
    "p5_shield": get_b64("p5_panel5_shield.jpg"),
    "p5_case03": get_b64("p5_panel4_case03.jpg"),
    "p8_surgery": get_b64("p8_panel1_surgery.jpg"),
    "p7_boxes": get_b64("p7_panel2_boxes.jpg"),
    "p7_recipe": get_b64("p7_panel3_recipe_clean.jpg"),
    "p12_epilogue": get_b64("p12_panel1_epilogue.jpg")
}
print("Imagens prontas!")

HTML_HEAD = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <title>Operação Byte Socrático: Graphic Novel (Edição Especial #01 · UFRPE)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&family=Comic+Neue:ital,wght@0,700;1,700&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Space+Grotesk:wght@700;800&family=JetBrains+Mono:wght@600;700;800&display=swap');

    * { box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    body { margin: 0; padding: 0; background-color: #050811; color: #F8FAFC; font-family: 'Comic Neue', cursive, sans-serif; font-size: 13px; }

    @page { size: A4 portrait; margin: 0; }
    
    .comic-page {
      width: 210mm;
      height: 297mm;
      margin: 0 auto;
      background: #090D16;
      position: relative;
      overflow: hidden;
      display: none;
      flex-direction: column;
      padding: 6mm 7mm 5mm 7mm;
      box-shadow: 0 0 45px rgba(0,0,0,0.9);
      page-break-after: always;
      page-break-inside: avoid;
    }
    .comic-page.active-page { display: flex; }

    body.webtoon-mode .comic-page {
      display: flex !important;
      margin-bottom: 8mm;
    }

    @media print {
      @page {
        size: A4 portrait;
        margin: 0 !important;
      }
      html, body, main, #comicContainer {
        margin: 0 !important;
        padding: 0 !important;
        background: #090D16 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        width: 210mm !important;
      }
      .reader-toolbar, .no-print {
        display: none !important;
      }
      .comic-page {
        display: flex !important;
        page-break-after: always !important;
        break-after: page !important;
        box-shadow: none !important;
        margin: 0 !important;
        width: 210mm !important;
        height: 296mm !important;
        max-height: 296mm !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
      }
    }
  </style>
</head>
<body>

  <!-- Top Sticky Reader Bar (Screen only) -->
  <header class="reader-toolbar no-print bg-slate-900 border-b border-slate-800 px-4 py-2.5 sticky top-0 z-50 flex items-center justify-between text-xs">
    <div class="flex items-center gap-3">
      <span class="bg-amber-400 text-slate-950 px-2 py-0.5 rounded font-extrabold uppercase font-mono text-[11px]">HQ Oficial</span>
      <h1 class="font-bold text-white text-sm">Operação Byte Socrático <span class="text-cyan-400 font-normal text-xs">(Edição Especial #01 · 14 Páginas)</span></h1>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="prevPage()" class="bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded font-bold transition flex items-center gap-1.5">
        <i class="fa-solid fa-chevron-left"></i> Anterior
      </button>
      <span id="pageIndicator" class="font-mono text-cyan-300 font-bold px-2">Pág. 01 / 14</span>
      <button onclick="nextPage()" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 px-3 py-1.5 rounded font-bold transition flex items-center gap-1.5">
        Próxima <i class="fa-solid fa-chevron-right"></i>
      </button>
      <div class="h-4 w-px bg-slate-700 mx-1"></div>
      <button onclick="toggleReadMode()" id="btnMode" class="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1.5 rounded font-bold transition flex items-center gap-1.5">
        <i class="fa-solid fa-scroll mr-1"></i> Webtoon
      </button>
      <a href="assets/ebook-operacao-byte-socratico.pdf" download class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded font-bold transition flex items-center gap-1.5">
        <i class="fa-solid fa-file-pdf"></i> Baixar PDF
      </a>
    </div>
  </header>

  <main id="comicContainer" class="py-4">
"""

def make_header(title, meta="UFRPE · EaD · 2ª VA"):
    return f"""
      <header class="hq-header">
        <div class="flex items-center gap-2">
          <span style="background: #090D16; border: 1.5px solid #06B6D4; color: #22D3EE; font-family: 'Space Grotesk', sans-serif; font-size: 0.55rem; font-weight: 800; padding: 1px 5px; border-radius: 3px;">
            EDIÇÃO #01
          </span>
          <h2 class="hq-header-title">{title}</h2>
        </div>
        <span class="hq-header-meta">{meta}</span>
      </header>
    """

def make_footer(page, total=14, custom_center=""):
    center = custom_center if custom_center else "UFRPE · POLO EaD RECIFE · UAEADTec · PROF. ERMESON"
    return f"""
      <footer class="hq-footer">
        <span>OPERAÇÃO BYTE SOCRÁTICO</span>
        <span>{center}</span>
        <span style="font-family: 'JetBrains Mono', monospace; color: #FACC15;">PÁG. {page:02d} / {total:02d}</span>
      </footer>
    """

pages = []

# =========================================================================
# PÁGINA 01: CAPA CLÁSSICA DE HQ
# =========================================================================
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
          ⚡ EDIÇÃO ESPECIAL #01 · UFRPE 2026.2
        </div>

        <!-- Left Teaser Badge -->
        <div class="caption-box caption-box-rose" style="top: 36%; left: 10px; width: 34%; font-size: 0.62rem; text-align: left; transform: rotate(-1.5deg);">
          🚨 <b style="color: #991B1B;">A ARMADILHA DA COLA!</b><br>O robô entregava o código pronto... mas no dia da prova presencial, a mente apagou!
        </div>

        <!-- Right Teaser Badge -->
        <div class="caption-box caption-box-cyan" style="top: 40%; right: 10px; width: 34%; font-size: 0.62rem; text-align: right; transform: rotate(1.5deg);">
          ✨ <b style="color: #0E7490;">O PODER DE SÓCRATES!</b><br>Como transformar uma máquina de cola em um tutor que ensina a pensar!
        </div>

        <!-- Bottom Teaser Strip -->
        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; z-index: 10; background: rgba(9, 13, 22, 0.94); border: 2.5px solid #FACC15; padding: 5px 10px; display: flex; align-items: center; justify-content: space-between;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.62rem; font-weight: 800; color: #FEF08A; text-transform: uppercase;">
            <i class="fa-solid fa-star text-amber-400 mr-1"></i> UMA HISTÓRIA INSPIRADA EM SITUAÇÕES REAIS DA EaD · POLO RECIFE / UFRPE
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
          <span>AUTOR: CAUÃ DA CUNHA LIRA · TUTOR PRESENCIAL DO POLO RECIFE</span>
        </div>
        <span>ORIENTADOR: PROF. ERMESON · PÁG. 01 DE 14</span>
      </footer>
    </section>
""")

# =========================================================================
# PÁGINA 02: ÍNDICE EDITORIAL & GUIA DE LEITURA
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 02: ÍNDICE & EXPEDIENTE -->
    <section class="comic-page" id="page-2">
      {make_header("GUIA OFICIAL DA MISSÃO · NESTA EDIÇÃO", "UFRPE COMICS #01")}

      <div class="hq-grid" style="gap: 4mm;">
        <!-- EXPEDIENTE BOX -->
        <div style="background: #0F172A; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #06B6D4; padding: 10px 14px;">
          <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
            <span class="text-amber-300 font-extrabold text-[12px] uppercase tracking-wider" style="font-family: 'Space Grotesk', sans-serif;">
              <i class="fa-solid fa-id-card-clip mr-1"></i> EXPEDIENTE DO LABORATÓRIO GEEK · POLO RECIFE
            </span>
            <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">2026.2 · 2ª VA</span>
          </div>

          <div class="grid grid-cols-2 gap-3 text-[9.5px] text-slate-300 font-mono">
            <div>
              <b class="text-cyan-300 block">ROTEIRO & CRIAÇÃO:</b>
              Cauã da Cunha Lira (Tutor Presencial de Informática)
            </div>
            <div>
              <b class="text-cyan-300 block">ORIENTAÇÃO PEDAGÓGICA:</b>
              Prof. Ermeson (Educação a Distância · UAEADTec/UFRPE)
            </div>
            <div>
              <b class="text-amber-300 block">AMBIENTAÇÃO REAL:</b>
              Polo EaD Recife (UFRPE · Campus Dois Irmãos)
            </div>
            <div>
              <b class="text-amber-300 block">AMBIENTE VIRTUAL:</b>
              AVA Moodle Oficial da UFRPE
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
                  <span class="text-slate-200"><b>Cap. 05:</b> O Desastre do Teste #03</span>
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
                  <span class="text-slate-200"><b>Cap. 07:</b> O Momento Eureka dos Post-its</span>
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

          <!-- RECADO DO TUTOR CAUÃ (ESTILO STAN'S SOAPBOX) -->
          <div class="bg-slate-950 p-3 rounded border border-slate-800 text-[9.2px] text-slate-300 leading-relaxed">
            <span class="text-amber-300 font-bold font-mono block mb-1">
              <i class="fa-solid fa-comment-dots mr-1"></i> RECADO DO TUTOR CAUÃ:
            </span>
            "Fala, nerd da computação! Se você já passou da meia-noite travado num código de Python e teve a tentação de copiar a resposta pronta de uma IA, esta história é para você. Acompanhe como a caloura Clara superou a ilusão de domínio e descobriu a verdadeira alegria de programar com autonomia!"
          </div>
        </div>
      </div>

      {make_footer(2, 14)}
    </section>
""")

# =========================================================================
# PÁGINA 03: PRÓLOGO / ORIGENS
# =========================================================================
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
              <i class="fa-solid fa-building-columns mr-1"></i> RECIFE · LABORATÓRIO DE INFORMÁTICA DO POLO RECIFE / UFRPE
            </div>
            <div class="balloon balloon-caua" style="bottom: 10px; right: 14px; width: 56%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              "Como futuro professor de Computação e tutor no Polo Recife, vejo um perigo invisível: a inteligência artificial que entrega a cola pronta pelo aluno em vez de <b>ensinar a pensar</b>!"
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
              <i class="fa-solid fa-house-laptop mr-1"></i> POLO EaD RECIFE · 22H15 · APÓS UM LONGO DIA DE TRABALHO
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
# PÁGINA 04: CAPÍTULO 1 · A CRISE COGNITIVA
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
              <i class="fa-solid fa-clock mr-1"></i> NOITE · 23H40 · O DESESPERO DA CALOURA DE EaD NO AVA MOODLE
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
              <span class="speaker-tag bg-rose-500 text-white font-mono">BYTE v0.9 (SEM FILTRO)</span><br>
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
              <i class="fa-solid fa-copy mr-1"></i> A ILUSÃO DE COMPETÊNCIA
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
# PÁGINA 05: CAPÍTULO 2 · O DIAGNÓSTICO DO MENTOR
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
              <i class="fa-solid fa-microscope mr-1"></i> POLO RECIFE / UFRPE · O DESABAFO DA CALOURA
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
              Você foi vítima da <b>Ilusão de Competência</b>, Clara! Quando a máquina entrega a resposta pronta, ela causa a evaporação do seu esforço mental!
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
              <i class="fa-solid fa-stairs mr-1"></i> A PEDAGOGIA DO ANDAIME COGNITIVO (WOOD, BRUNER & ROSS, 1976)
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
              Exatamente! Isso exige <b>mediação socrática</b> calibrada na medida certa para a sua ZDP!
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
# PÁGINA 07: CAPÍTULO 4 · A PRIMEIRA BATERIA DE TESTES
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
              Ele ainda age como um entregador de respostas. Falta o método socrático... Mas o verdadeiro desastre ainda está por vir no Teste #03!
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
# PÁGINA 08: CAPÍTULO 5 · O DESASTRE DO TESTE #03
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 08: CAPÍTULO 05 - SPLASH PAGE -->
    <section class="comic-page" id="page-8">
      {make_header("CAPÍTULO 05 · O DESASTRE DO TESTE #03: O ALARME VERMELHO NA ARENA")}

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
              PAROU! <b>CARTÃO VERMELHO!</b> Você está falando com uma caloura do 1º período de EaD, não com o criador do CPython!
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
              A teoria estava exata, mas a didática foi um desastre! Sem mediação socrática, a IA se torna uma fábrica de evasão escolar!
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
              Trava 1: Proibido dar código pronto! Trava 2: Todo conceito abstrato deve abrir com uma metáfora concreta do cotidiano!
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
              E se o estudante empacar, ele libera a escada de 3 degraus de dicas inspirada no andaime de Wood, Bruner e Ross! O <b>Byte v2.0</b> nasceu!
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
# PÁGINA 10: CAPÍTULO 7 · O MOMENTO EUREKA DOS POST-ITS
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 10: CAPÍTULO 07 -->
    <section class="comic-page" id="page-10">
      {make_header("CAPÍTULO 07 · O MOMENTO EUREKA DOS POST-ITS NA MEMÓRIA")}

      <div class="hq-grid">
        <!-- ROW 1: O RETESTE DOS POST-ITS -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_boxes']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-note-sticky mr-1"></i> RETESTE DO TESTE #03 · A METÁFORA DOS POST-ITS EM PYTHON
            </div>
            <div class="sfx text-amber-300 text-3xl" style="top: 14px; right: 28%;">
              EUREKA!
            </div>

            <!-- Byte v2.0 Socratic Balloon -->
            <div class="balloon-socratic" style="top: 26px; left: 14px; width: 50%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (METÁFORA DOS POST-ITS)</span><br>
              "Pense em post-its colados em objetos na memória! Quando fazemos <code>idade = 19</code>, o número 19 existe e o post-it 'idade' é colado nele. No aniversário fazemos <code>idade = 20</code>. O que acontece com o post-it?"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Eureka Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Eu descolo o post-it do 19 e colo no 20! A variável é um nome referenciando o objeto! <b>Caramba... agora eu ENXERGUEI a memória do Python!</b>
              <svg class="tail-svg" style="bottom: -15px; right: 24px;" viewBox="0 0 24 16">
                <path d="M 18,0 Q 12,14 4,16 Q 8,8 6,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4.5" y1="0" x2="17.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: A CESTA DE COMPRAS E O ACUMULADOR -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_recipe']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-basket-shopping mr-1"></i> A CESTA DE COMPRAS E O POST-IT ACUMULADOR
            </div>
            <div class="sfx text-emerald-400 text-2xl" style="top: 10px; right: 20%;">
              PING!
            </div>

            <!-- Byte v2.0 Balloon -->
            <div class="balloon-socratic" style="top: 28px; left: 14px; width: 52%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (ANALOGIA DO COTIDIANO)</span><br>
              "O laço <code>for</code> é como passar a feira no caixa: você passa item por item da cesta, sem tirar nenhum dela! Enquanto você passa os itens, onde anota o total parcial?"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#ECFEFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 46%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Num post-it chamado <code>total</code>, que vai mudando de lugar a cada soma! Cauã, o código <b>rodou perfeitamente</b> no terminal e dessa vez eu entendi tudo!
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
      {make_header("CAPÍTULO 08 · A TRANSFORMAÇÃO DO APRENDIZADO NO POLO RECIFE")}

      <div class="hq-grid">
        <!-- ROW 1: O BYTE v2.0 INTERAGINDO COM A TURMA -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_4']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-users-gear mr-1"></i> DIAS DEPOIS · O BYTE v2.0 EM AÇÃO NO AVA MOODLE DA UFRPE
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
              Bloom (1984) mostrou que tutoria individual com domínio superava muito a sala tradicional. Um tutor de IA calibrado aproxima esse apoio com mediação socrática!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Amanhã é a avaliação final presencial no Polo Recife... e dessa vez não sinto medo nenhum! O conhecimento agora é meu!
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
              <i class="fa-solid fa-pen-nib mr-1"></i> SÁBADO · 09H00 · AVALIAÇÃO FINAL PRESENCIAL NO POLO RECIFE
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 12px; right: 20%;">
              SCRATCH!
            </div>

            <!-- Thought Cloud Balloon -->
            <div class="balloon-thought" style="bottom: 14px; left: 14px; width: 56%;">
              <span class="speaker-tag bg-sky-300 text-slate-950">CLARA (PENSAMENTO)</span><br>
              Questão 4: <i>"Construa um algoritmo que percorra a lista de notas e calcule a média"</i>... Fecho os olhos... lembro da cesta de compras... crio o post-it acumulador <code>total</code>... divido pelo tamanho!
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
              Não precisei de tela nem de robô me soprando... o Byte v2.0 não fez a prova por mim, ele me ensinou a <b>pensar com autonomia!</b>
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
        <!-- ROW 1: COMEMORAÇÃO DA NOTA 9.0 NO POLO -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p12_epilogue']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              <i class="fa-solid fa-medal mr-1"></i> SEMANAS DEPOIS · POLO RECIFE / UFRPE · O RESULTADO OFICIAL
            </div>
            <div class="sfx text-emerald-400 text-3xl" style="top: 14px; right: 26%;">
              VICTORY!
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Cauã, tirei <b>9.0 na avaliação presencial!</b> Errei só um detalhe bobo de indentação no final, mas a lógica toda foi 100% minha!
              <svg class="tail-svg" style="top: -16px; left: 36px;" viewBox="0 0 24 16">
                <path d="M 18,16 Q 12,2 4,0 Q 8,10 14,16 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="4" y1="16" x2="16" y2="16" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Parabéns, Clara! Essa nota 9.0 prova que <b>o papel da IA na EaD não é pensar pelo aluno, mas ensinar o aluno a pensar com autonomia!</b>
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
              "A tecnologia sem intenção pedagógica vira muleta. Mas com mediação socrática, ela liberta o potencial humano!"
              <svg class="tail-svg" style="bottom: -15px; left: 24px;" viewBox="0 0 24 16">
                <path d="M 4,0 Q 8,14 18,16 Q 12,8 14,0 Z" fill="#FFFFFF" stroke="#090D16" stroke-width="2.2" stroke-linejoin="round"/>
                <line x1="3.5" y1="0" x2="14.5" y2="0" stroke="#FFFFFF" stroke-width="3"/>
              </svg>
            </div>

            <!-- Clara & Byte Bottom Teaser Box -->
            <div class="caption-box" style="bottom: 12px; left: 12px; right: 12px; display: flex; justify-content: space-between; align-items: center; background: rgba(9, 13, 22, 0.96); border: 2.5px solid #FACC15; padding: 6px 14px; color: #F8FAFC;">
              <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 800; color: #FACC15;">
                <i class="fa-solid fa-arrow-right text-cyan-400 mr-1"></i> SIGA PARA A PÁG. 14: CADERNO DE REFERÊNCIAS & NOTAS DO AUTOR
                <span class="block text-[8.5px] text-slate-300 font-normal">Bibliografia ABNT NBR 6023, Metodologia e Reprodutibilidade Aberta</span>
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
# PÁGINA 14: CADERNO DE REFERÊNCIAS CIENTÍFICAS & POSFÁCIO DO AUTOR
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
            <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">POR CAUÃ LIRA · POLO RECIFE</span>
          </div>
          <p class="text-[9.2px] text-slate-200 leading-relaxed font-sans mb-1.5">
            Esta Graphic Novel nasceu de uma inquietude legítima na Licenciatura em Computação da UFRPE e na tutoria presencial do Polo Recife: <i>como ensinar quando a inteligência artificial seduz o estudante com respostas prontas que atrofiam o pensamento autônomo?</i>
          </p>
          <p class="text-[9.2px] text-slate-200 leading-relaxed font-sans">
            Para conceber esta obra, atuei como Diretor Pedagógico e roteirista, estruturando as dores de Clara, os 5 Casos de Teste e as 4 Travas do System Prompt com base nos clássicos da Educação e na literatura contemporânea de EdTech. A máquina desenhou os pixels sob direção humana; a inteligência pedagógica foi 100% autoral.
          </p>
        </div>

        <!-- REFERÊNCIAS CIENTÍFICAS FUNDAMENTAIS (PADRÃO ABNT) -->
        <div style="background: #090D16; border: 3.5px solid #090D16; box-shadow: 4px 4px 0 #FACC15; padding: 10px 14px; flex: 1; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div class="flex items-center justify-between border-b border-slate-800 pb-1 mb-2">
              <span class="text-amber-400 font-extrabold text-[11.5px] uppercase tracking-wider font-mono">
                <i class="fa-solid fa-book-bookmark mr-1 text-cyan-400"></i> REFERÊNCIAS BIBLIOGRÁFICAS FUNDAMENTAIS (ABNT NBR 6023)
              </span>
              <span class="text-[9px] text-slate-400 font-mono">RECONHECIMENTO CIENTÍFICO</span>
            </div>

            <div class="space-y-1 text-[8.0px] text-slate-300 font-mono leading-tight">
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-cyan-400">
                • <b>BASTANI, H. et al.</b> Generative AI can harm learning without calibrating practice. <i>Nature Human Behaviour</i>, v. 9, p. 1-12, 2025.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-emerald-400">
                • <b>BJORK, R. A.</b> Memory and metamemory considerations in the training of human beings. <i>Metacognition: Knowing about Knowing</i>, Cambridge: MIT Press, p. 185-205, 1994.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-amber-400">
                • <b>BLOOM, Benjamin S.</b> The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. <i>Educational Researcher</i>, v. 13, n. 6, p. 4-16, 1984.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-purple-400">
                • <b>CHEVALLARD, Yves.</b> <i>La Transposition Didactique: Du Savoir Savant au Savoir Enseigné</i>. Grenoble: La Pensée Sauvage, 1991.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-rose-400">
                • <b>KESTIN, G. et al.</b> AI tutoring outperforms active learning in introductory physics. <i>Physical Review Physics Education Research</i>, v. 21, 2025.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-sky-400">
                • <b>OECD.</b> <i>Students, Digital Devices and Success: PISA 2025 Policy Brief</i>. Paris: OECD Publishing, 2026. (Estudo com estudantes de 15 anos).
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-teal-400">
                • <b>SWELLER, John.</b> Cognitive load during problem solving: Effects on learning. <i>Cognitive Science</i>, v. 12, n. 2, p. 257-285, 1988.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-indigo-400">
                • <b>VYGOTSKY, Lev S.</b> <i>Mind in Society: The Development of Higher Psychological Processes</i>. Cambridge: Harvard University Press, 1978.
              </div>
              <div class="p-1 bg-slate-900/80 rounded border-l-2 border-l-yellow-400">
                • <b>WOOD, David; BRUNER, Jerome S.; ROSS, Gail.</b> The role of tutoring in problem solving. <i>Journal of Child Psychology and Psychiatry</i>, v. 17, n. 2, p. 89-100, 1976.
              </div>
            </div>
          </div>

          <!-- DADOS ABERTOS, LICENÇA E CRÉDITOS FINAIS -->
          <div class="bg-slate-950 p-2 rounded border border-slate-800 mt-2 flex items-center justify-between text-[8.5px] font-mono">
            <div>
              <span class="text-amber-300 font-bold block">RECURSO EDUCACIONAL ABERTO (REA) · CC BY-SA 4.0</span>
              <span class="text-slate-400">Universidade Federal Rural de Pernambuco · UAEADTec</span>
            </div>
            <div class="text-right">
              <span class="text-cyan-400 font-bold block">REPOSITÓRIO: github.com/lira-labs/workspace</span>
              <span class="text-slate-400">PORTAL: projeto-ead-caua.vercel.app</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(14, 14, "EDIÇÃO ESPECIAL #01 · UFRPE · UAEADTec · POLO RECIFE · 2026.2")}
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

full_html = HTML_HEAD + "\\n".join(pages) + HTML_FOOTER

print(f"Escrevendo arquivo HTML puro em {OUT_HTML}...")
with open(OUT_HTML, "w", encoding="utf-8") as out_f:
    out_f.write(full_html)

sz_mb = os.path.getsize(OUT_HTML) / (1024 * 1024)
print(f"Sucesso! {OUT_HTML} gerado com 14 páginas enxutas e consistentes! Tamanho final: {sz_mb:.2f} MB")
