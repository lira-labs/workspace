"""
Gerador Mestre da Graphic Novel 'Operação Byte Socrático' - Edição Especial #01
Edição Definitiva Geek & Acadêmica de 22 Páginas A4 (UFRPE · Polo EaD Recife)
"""
import os
import base64

def get_base64_image(rel_path):
    full_path = os.path.join(os.path.dirname(__file__), "..", "..", rel_path)
    full_path = os.path.abspath(full_path)
    if not os.path.exists(full_path):
        print(f"Aviso: Imagem não encontrada: {full_path}")
        return ""
    with open(full_path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(full_path)[1].lower().replace(".", "")
    if ext == "jpg": ext = "jpeg"
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:image/{ext};base64,{b64}"

print("Carregando imagens canônicas em alta resolução...")
IMG_COVER = get_base64_image("code/projeto_ead_tutores/assets/hq/p1_cover_clean.jpg")
IMG_COLD_OPEN = get_base64_image("code/projeto_ead_tutores/assets/hq/panel_cold_open_exam.jpg")
IMG_BYTE_SHORTCUT = get_base64_image("code/projeto_ead_tutores/assets/hq/panel_byte_shortcut.jpg")
IMG_COGNITIVE_SHORTCUT = get_base64_image("code/projeto_ead_tutores/assets/hq/panel_cognitive_shortcut.jpg")
IMG_EXAM_BLACKOUT = get_base64_image("code/projeto_ead_tutores/assets/hq/panel_exam_blackout.jpg")
IMG_SCAFFOLDING = get_base64_image("code/projeto_ead_tutores/assets/hq/p3_panel4.jpg")
IMG_SCANNER_CLEAN = get_base64_image("code/projeto_ead_tutores/assets/hq/p4_panel1_scanner_clean.jpg")
IMG_SCANNER_CLARA = get_base64_image("code/projeto_ead_tutores/assets/hq/panel_scanner_clara.jpg")
IMG_SHIELD = get_base64_image("code/projeto_ead_tutores/assets/hq/p5_panel5_shield.jpg")
IMG_ZDP = get_base64_image("code/projeto_ead_tutores/assets/hq/p4_panel3_criterio3.jpg")
IMG_CASE03_DISASTER = get_base64_image("code/projeto_ead_tutores/assets/hq/p5_panel4_case03.jpg")
IMG_SURGERY = get_base64_image("code/projeto_ead_tutores/assets/hq/p8_panel1_surgery.jpg")
IMG_CAUA_CLARA_LAB = get_base64_image("code/projeto_ead_tutores/assets/hq/p3_panel5.jpg")
IMG_CLARA_TYPING = get_base64_image("code/projeto_ead_tutores/assets/hq/p3_panel2.jpg")
IMG_POSTITS_BOXES = get_base64_image("code/projeto_ead_tutores/assets/hq/p7_panel2_boxes.jpg")
IMG_CAUA_TERMINAL = get_base64_image("code/projeto_ead_tutores/assets/hq/p2_panel1_caua.jpg")
IMG_CLARA_NIGHT = get_base64_image("code/projeto_ead_tutores/assets/hq/p3_panel1.jpg")
IMG_CLARA_EXAM_CONFIDENT = get_base64_image("code/projeto_ead_tutores/assets/hq/p3_panel3.jpg")
IMG_EPILOGUE = get_base64_image("code/projeto_ead_tutores/assets/hq/p12_panel1_epilogue.jpg")
print("Imagens prontas!")

html = []

html.append("""<!DOCTYPE html>
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
      max-height: 297mm;
      margin: 0 auto;
      padding: 7mm 9mm;
      background-color: #090D16;
      background-image: 
        radial-gradient(rgba(6, 182, 212, 0.08) 1.5px, transparent 1.5px),
        radial-gradient(rgba(245, 158, 11, 0.05) 1.5px, transparent 1.5px);
      background-size: 24px 24px, 36px 36px;
      background-position: 0 0, 12px 12px;
      page-break-after: always;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-sizing: border-box;
    }

    .comic-page.academic-page {
      background-color: #060A13;
      background-image: 
        linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
      background-size: 20px 20px;
      font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .hq-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 2.5px solid #06B6D4;
      padding-bottom: 1.8mm;
      margin-bottom: 2.5mm;
      flex-shrink: 0;
    }

    .hq-footer {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-top: 1.5px solid #1E293B;
      padding-top: 1.8mm;
      margin-top: auto;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.60rem;
      color: #94A3B8;
      flex-shrink: 0;
    }

    .comic-panel {
      background: #0F172A;
      border: 2.8px solid #090D16;
      box-shadow: 3.5px 3.5px 0 #000000;
      border-radius: 6px;
      position: relative;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }

    .caption-box {
      background: #FEF08A;
      color: #090D16;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 800;
      font-size: 0.65rem;
      text-transform: uppercase;
      padding: 2.5px 7px;
      border: 1.8px solid #090D16;
      box-shadow: 2px 2px 0 #000000;
      display: inline-block;
      margin-bottom: 3px;
      z-index: 10;
    }

    .caption-cyan { background: #A5F3FC; color: #090D16; }
    .caption-red { background: #FECACA; color: #7F1D1D; }
    .caption-amber { background: #FDE68A; color: #78350F; }
    .caption-purple { background: #E9D5FF; color: #581C87; }

    .speech-bubble {
      background: #FFFFFF;
      color: #090D16;
      border: 2px solid #090D16;
      border-radius: 12px;
      padding: 5px 8px;
      font-family: 'Comic Neue', cursive, sans-serif;
      font-weight: 700;
      font-size: 0.72rem;
      line-height: 1.22;
      box-shadow: 2.5px 2.5px 0 rgba(0,0,0,0.85);
      position: relative;
      margin-bottom: 3px;
      max-width: 95%;
    }

    .speech-bubble.bubble-caua { background: #EFF6FF; border-color: #1D4ED8; }
    .speech-bubble.bubble-byte-bad { background: #FEF2F2; border-color: #DC2626; color: #7F1D1D; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; }
    .speech-bubble.bubble-byte-good { background: #ECFEFF; border-color: #0891B2; color: #0E7490; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; }
    .speech-thought { background: #F8FAFC; border: 2px dashed #475569; border-radius: 14px; padding: 4px 8px; font-style: italic; font-size: 0.70rem; color: #1E293B; }

    .sfx {
      font-family: 'Bangers', cursive;
      display: inline-block;
      text-shadow: 2.5px 2.5px 0 #000, -1px -1px 0 #000;
      letter-spacing: 1px;
    }
    .sfx-zap { color: #F59E0B; transform: rotate(-4deg); font-size: 1.5rem; }
    .sfx-clac { color: #06B6D4; transform: rotate(3deg); font-size: 1.4rem; }
    .sfx-tic { color: #EF4444; font-size: 1.4rem; }
    .sfx-plim { color: #10B981; transform: rotate(-3deg); font-size: 1.5rem; }
    .sfx-zoom { color: #38BDF8; transform: rotate(2deg); font-size: 1.5rem; }

    .pause-pense-box {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.18), rgba(245, 158, 11, 0.06));
      border: 1.8px dashed #F59E0B;
      border-radius: 5px;
      padding: 5px 8px;
      margin-top: 2px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 0.66rem;
      color: #FDE68A;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .badge-geek {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 0.58rem;
      padding: 2px 6px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }
    .badge-blue { background: #0284C7; color: #FFFFFF; }
    .badge-amber { background: #D97706; color: #FFFFFF; }
    .badge-green { background: #059669; color: #FFFFFF; }
    .badge-purple { background: #7C3AED; color: #FFFFFF; }

    .grid-2col { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
    .grid-3col { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 3mm; }
    .grid-1-2 { display: grid; grid-template-columns: 1fr 2fr; gap: 3mm; }
    .grid-2-1 { display: grid; grid-template-columns: 2fr 1fr; gap: 3mm; }

    .panel-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    #reader-bar {
      position: fixed; top: 0; left: 0; right: 0; height: 48px;
      background: rgba(9, 13, 22, 0.96); border-bottom: 2px solid #06B6D4;
      z-index: 1000; display: flex; align-items: center; justify-content: space-between;
      padding: 0 16px; backdrop-filter: blur(8px);
    }
    @media print {
      #reader-bar { display: none !important; }
      body { background: transparent !important; }
      .comic-page { margin: 0 !important; box-shadow: none !important; page-break-after: always !important; }
    }
    @media screen {
      body { padding-top: 56px; padding-bottom: 40px; }
      .comic-page { margin: 20px auto; box-shadow: 0 15px 35px rgba(0,0,0,0.8), 0 0 0 1px rgba(6,182,212,0.3); border-radius: 4px; }
      .comic-page:not(.active-page) { display: none; }
      body.webtoon-mode .comic-page { display: flex !important; margin-bottom: 24px; }
    }
  </style>
</head>
<body>

  <!-- Barra Superior do Leitor Interativo -->
  <div id="reader-bar">
    <div class="flex items-center gap-3">
      <span style="font-family: 'Bangers', cursive; font-size: 1.35rem; color: #A5F3FC; letter-spacing: 1px;">
        OPERAÇÃO BYTE SOCRÁTICO
      </span>
      <span class="bg-cyan-500/20 text-cyan-300 font-mono text-xs px-2 py-0.5 rounded border border-cyan-500/30">
        Edição Especial #01 · 22 Páginas A4
      </span>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="prevPage()" class="bg-slate-800 hover:bg-slate-700 text-white px-3 py-1.5 rounded text-xs font-bold border border-slate-700">
        <i class="fa-solid fa-chevron-left mr-1"></i> Anterior
      </button>
      <span id="pageIndicator" class="font-mono text-xs text-amber-300 font-bold px-2">
        Pág. 01 / 22
      </span>
      <button onclick="nextPage()" class="bg-slate-800 hover:bg-slate-700 text-white px-3 py-1.5 rounded text-xs font-bold border border-slate-700">
        Próxima <i class="fa-solid fa-chevron-right ml-1"></i>
      </button>
      <button onclick="toggleWebtoon()" id="btnWebtoon" class="ml-2 bg-purple-900/60 hover:bg-purple-800 text-purple-200 px-3 py-1.5 rounded text-xs font-bold border border-purple-500/40">
        <i class="fa-solid fa-scroll mr-1"></i> Modo Rolo
      </button>
      <button onclick="window.print()" class="ml-1 bg-cyan-600 hover:bg-cyan-500 text-white px-3 py-1.5 rounded text-xs font-bold shadow">
        <i class="fa-solid fa-print mr-1"></i> Imprimir PDF
      </button>
    </div>
  </div>
""")

# =========================================================================
# PÁGINA 01: CAPA OFICIAL (Edição Especial #01)
# =========================================================================
html.append(f"""
  <!-- PÁGINA 01: CAPA OFICIAL -->
  <section class="comic-page active-page" id="page-1" style="padding: 0; border: none; justify-content: space-between;">
    <div style="position: absolute; inset: 0; z-index: 1;">
      <img src="{IMG_COVER}" alt="Capa da Graphic Novel" style="width: 100%; height: 100%; object-fit: cover; filter: brightness(0.93) contrast(1.08);" />
      <div style="position: absolute; inset: 0; background: linear-gradient(180deg, rgba(5,8,17,0.92) 0%, rgba(5,8,17,0.15) 30%, rgba(5,8,17,0.2) 65%, rgba(5,8,17,0.95) 100%);"></div>
    </div>

    <!-- Topo da Capa -->
    <div style="position: relative; z-index: 10; padding: 7mm 8mm 0 8mm; text-align: center;">
      <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #06B6D4; padding-bottom: 4px; margin-bottom: 8px;">
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.65rem; font-weight: 800; color: #F59E0B; letter-spacing: 1.5px; text-transform: uppercase;">
          UFRPE · UAEADTec · LICENCIATURA EM COMPUTAÇÃO · POLO RECIFE
        </span>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; background: #06B6D4; color: #090D16; font-weight: 800; padding: 2px 7px; border-radius: 4px;">
          EDIÇÃO ESPECIAL #01
        </span>
      </div>

      <div style="background: rgba(15, 23, 42, 0.88); border: 2px solid #F59E0B; border-radius: 6px; padding: 4px 10px; display: inline-block; margin-bottom: 6px;">
        <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.68rem; font-weight: 800; color: #FDE68A;">
          <i class="fa-solid fa-shield-halved text-amber-400 mr-1"></i> Uma história inspirada em situações reais da Educação a Distância
        </span>
      </div>

      <h1 style="font-family: 'Bangers', cursive; font-size: 3.5rem; color: #A5F3FC; text-shadow: 4px 4px 0 #090D16, 0 0 25px rgba(6,182,212,0.6); margin: 0; line-height: 0.95; letter-spacing: 2px;">
        OPERAÇÃO BYTE SOCRÁTICO
      </h1>
      <p style="font-family: 'Space Grotesk', sans-serif; font-size: 0.88rem; font-weight: 800; color: #FDE68A; text-shadow: 2px 2px 0 #000; margin: 4px 0 0 0; letter-spacing: 0.5px;">
        A Jornada da Ilusão da Cola à Autonomia no Código Python
      </p>
    </div>

    <!-- Rodapé da Capa -->
    <div style="position: relative; z-index: 10; padding: 0 8mm 7mm 8mm;">
      <div style="background: rgba(9, 13, 22, 0.92); border: 2.5px solid #06B6D4; box-shadow: 4px 4px 0 #000000; border-radius: 8px; padding: 10px 14px; backdrop-filter: blur(6px);">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #1E293B; padding-bottom: 6px; margin-bottom: 6px;">
          <div>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: #A5F3FC;">
              DISCIPLINA: EDUCAÇÃO A DISTÂNCIA (2ª VA)
            </div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.66rem; color: #94A3B8;">
              Orientação: <strong>Prof. Ermeson</strong> · UFRPE / UAEADTec
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.72rem; font-weight: 800; color: #F59E0B;">
              AUTOR E DIREÇÃO DE ARTE
            </div>
            <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.66rem; color: #F8FAFC;">
              <strong>Cauã da Cunha Lira</strong> · Tutor Presencial
            </div>
          </div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #64748B;">
          <span>Polo EaD Recife (Dois Irmãos)</span>
          <span>Graphic Novel Didática & Dossiê Pedagógico</span>
          <span>22 Páginas A4</span>
        </div>
      </div>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 02: EXPEDIENTE EDITORIAL & ÍNDICE DE HQ (Front-Matter Geek)
# =========================================================================
html.append("""
  <!-- PÁGINA 02: ÍNDICE DE HQ GEEK -->
  <section class="comic-page academic-page" id="page-2">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-gamepad mr-1 text-cyan-400"></i> UFRPE COMICS #01 · GUIA OFICIAL DA MISSÃO
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">DOSSIÊ DO POLO</span>
    </div>

    <!-- Banner Geek do Índice -->
    <div style="background: #0F172A; border: 2.5px solid #06B6D4; box-shadow: 3px 3px 0 #000; border-radius: 6px; padding: 8px 12px; margin-bottom: 3mm; display: flex; justify-content: space-between; align-items: center;">
      <div>
        <div style="font-family: 'Bangers', cursive; font-size: 1.45rem; color: #F59E0B; letter-spacing: 1.5px; line-height: 1;">
          NESTA EDIÇÃO: O MAPA DOS 10 ATOS & O DOSSIÊ SECRETO
        </div>
        <div style="font-size: 0.62rem; color: #94A3B8; font-family: 'Plus Jakarta Sans', sans-serif;">
          Acompanhe a saga da caloura Clara e do tutor Cauã para reprogramar a IA e conquistar a nota 9.0!
        </div>
      </div>
      <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #A5F3FC;">
        POLO RECIFE · UFRPE<br>
        <span style="color: #4ADE80;">● SISTEMA ONLINE</span>
      </div>
    </div>

    <!-- Grid do Sumário Estilo Gibi -->
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm; flex-grow: 1;">
      <!-- Coluna da Esquerda: Narrativa HQ -->
      <div style="display: flex; flex-direction: column; gap: 2.5mm;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #38BDF8; border-bottom: 1.5px solid #38BDF8; padding-bottom: 2px;">
          PARTE 1: A NARRATIVA SEQUENCIAL (HQ)
        </div>

        <div style="background: #0B1120; border-left: 3px solid #EF4444; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #FCA5A5;">
            <span>PÁG. 03 · PRÓLOGO (COLD OPEN)</span>
            <span class="badge-geek badge-blue">TENSÃO</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">Branco Total: A paralisia às 09h45 diante da folha de prova.</div>
        </div>

        <div style="background: #0B1120; border-left: 3px solid #F59E0B; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #FDE68A;">
            <span>PÁGS. 04-05 · ATOS I & II: A QUEDA</span>
            <span class="badge-geek badge-amber">ATO 1</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">A ilusão da cola mastigada às 23h40, a nota zero no Moodle e o andaime.</div>
        </div>

        <div style="background: #0B1120; border-left: 3px solid #A855F7; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #E9D5FF;">
            <span>PÁGS. 06-08 · ATOS III-V: A ARENA 4D</span>
            <span class="badge-geek badge-purple">ATO 2A</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">O Scanner 4D, a arena dos 5 testes e o desastre do CPython/Heap.</div>
        </div>

        <div style="background: #0B1120; border-left: 3px solid #06B6D4; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #A5F3FC;">
            <span>PÁGS. 09-10 · ATO VI: A CIRURGIA</span>
            <span class="badge-geek badge-blue">ATO 2B</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">Dentro do Byte: soldando as 4 travas socráticas no System Prompt.</div>
        </div>

        <div style="background: #0B1120; border-left: 3px solid #10B981; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #6EE7B7;">
            <span>PÁGS. 11-13 · ATO VII & INTERLÚDIO</span>
            <span class="badge-geek badge-green">ATO 2C</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">O Eureka dos Post-its, a cesta do for, o bug do b = a e o Byte v2.1.</div>
        </div>

        <div style="background: #0B1120; border-left: 3px solid #38BDF8; padding: 4px 8px; border-radius: 3px;">
          <div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 0.64rem; color: #BAE6FD;">
            <span>PÁGS. 14-16 · ATOS VIII-X: O DESFECHO</span>
            <span class="badge-geek badge-blue">ATO 3</span>
          </div>
          <div style="font-size: 0.58rem; color: #94A3B8;">A tentação do bot comercial, a prova no polo e a nota 9.0 com limites.</div>
        </div>
      </div>

      <!-- Coluna da Direita: Caderno do Professor -->
      <div style="display: flex; flex-direction: column; gap: 2.5mm;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #F59E0B; border-bottom: 1.5px solid #F59E0B; padding-bottom: 2px;">
          PARTE 2: DOSSIÊ DO PROFESSOR (ABNT)
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #FBBF24; font-size: 0.62rem;">PÁG. 17 · MANUAL DE USO DOCENTE:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">3 modalidades de aula (Individual, Debate, Oficina) e 5 objetivos (Bloom/Sweller).</span>
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #38BDF8; font-size: 0.62rem;">PÁG. 18 · RUBRICA & TABELA COMPARATIVA:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">Escala 1 a 5 e desempenho oficial dos 5 testes nas 4 versões do Byte (v0.9 ao v2.1).</span>
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #A5F3FC; font-size: 0.62rem;">PÁG. 19 · SYSTEM PROMPT INTEGRAL:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">Código-fonte completo das 4 travas do Byte v2.1 e bateria de entradas e saídas.</span>
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #C084FC; font-size: 0.62rem;">PÁG. 20 · QUESTÕES & ATIVIDADES PRÁTICAS:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">Debate socrático, síntese dos 4 Pause e Pense e desafios práticos de Trava 6.</span>
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #6EE7B7; font-size: 0.62rem;">PÁG. 21 · ÉTICA HACKER & GLOSSÁRIO NERD:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">Limitações metodológicas, conformidade com a LGPD e 12 termos canônicos explicados.</span>
        </div>

        <div style="background: #0B1120; border: 1px solid #1E293B; padding: 5px 8px; border-radius: 4px;">
          <strong style="color: #F87171; font-size: 0.62rem;">PÁG. 22 · BIBLIOTECA DO MENTOR:</strong><br>
          <span style="font-size: 0.58rem; color: #94A3B8;">Referências científicas completas (ABNT NBR 6023) e ressalva oficial PISA OECD 2026.</span>
        </div>
      </div>
    </div>

    <!-- Recado do Mentor (Stan's Soapbox Geek) -->
    <div style="background: #0F172A; border: 2px solid #F59E0B; border-radius: 6px; padding: 6px 10px; margin-top: 3mm; display: flex; gap: 10px; align-items: center;">
      <i class="fa-solid fa-terminal text-amber-400 text-2xl"></i>
      <div style="font-size: 0.60rem; color: #CBD5E1; line-height: 1.35;">
        <strong style="color: #FDE68A;">RECADO DO TUTOR CAUÃ:</strong> "Programar em Python não é sobre decorar comandos ou colar do ChatGPT; é sobre treinar a sua mente para fatiar grandes problemas em passos lógicos simples. Esta Graphic Novel é o nosso convite para você abandonar a muleta da resposta pronta e descobrir o prazer indescritível de pensar por si mesmo. Boa leitura!"
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>EXPEDIENTE & GUIA DA MISSÃO</span>
      <span>PÁGINA 02</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 03: PRÓLOGO (COLD OPEN) — "BRANCO TOTAL"
# =========================================================================
html.append(f"""
  <!-- PÁGINA 03: PRÓLOGO (COLD OPEN) -->
  <section class="comic-page" id="page-3">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-clock mr-1 text-cyan-400"></i> PRÓLOGO (COLD OPEN) · BRANCO TOTAL
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #EF4444; color: #FFFFFF; padding: 2px 7px; border-radius: 4px;">09H45 NO POLO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel 1: Imagem Inédita do Cold Open -->
      <div class="comic-panel" style="flex: 1.4; min-height: 125mm; position: relative;">
        <img src="{IMG_COLD_OPEN}" alt="Clara paralisada na prova presencial no Polo Recife" class="panel-img" />
        
        <div style="position: absolute; top: 8px; left: 8px; z-index: 10;">
          <span class="caption-box caption-amber">
            <i class="fa-solid fa-location-dot mr-1"></i> SÁBADO · 09H45 · POLO EAD RECIFE (UFRPE)
          </span>
        </div>

        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; z-index: 10;">
          <div class="speech-thought" style="background: rgba(255,255,255,0.96); box-shadow: 3px 3px 0 #000;">
            <i class="fa-solid fa-circle text-slate-400 text-[6px] mr-1"></i>
            <strong>Clara (pensamento aflito):</strong> "A folha de prova... totalmente em branco. Restam quinze minutos para o fiscal recolher. Minha mão treme e a caneta não anda. Ontem no chat eu copiei tudo tão fácil... por que deu tela azul na minha cabeça agora?!"
          </div>
        </div>
      </div>

      <!-- Painel 2 e 3 em Grid -->
      <div class="grid-2col" style="flex: 1; min-height: 85mm;">
        <!-- Painel 2: O Relógio e o Pânico -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #111827;">
          <span class="caption-box caption-red">O CRONÔMETRO IMPLACÁVEL</span>
          <div style="text-align: center; margin: auto 0;">
            <div class="sfx sfx-tic">
              TIC... TAC... TIC... TAC...
            </div>
            <p style="font-size: 0.72rem; color: #CBD5E1; margin: 4px 0 0 0; line-height: 1.3;">
              O eco dos ponteiros na sala silenciosa parecia uma contagem regressiva para o fracasso.
            </p>
          </div>
          <div class="speech-bubble" style="border-color: #EF4444;">
            <strong>Clara:</strong> "Eu não sei nem a primeira linha... Foi tudo uma ilusão? Eu não aprendi nada?!"
          </div>
        </div>

        <!-- Painel 3: O Gancho do Flashback -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #06B6D4;">
          <span class="caption-box caption-cyan">FLASHBACK · DUAS SEMANAS ANTES</span>
          <div style="margin: auto 0; font-size: 0.74rem; color: #E2E8F0; line-height: 1.4;">
            <p>
              A paralisia daquela manhã de sábado não nasceu ali. Ela começou quatorze dias antes, diante de uma tela brilhante, quando a conveniência da resposta imediata parecia uma vitória.
            </p>
          </div>
          <div style="background: #1E293B; border-left: 3px solid #06B6D4; padding: 6px 8px; border-radius: 4px; font-size: 0.68rem; color: #A5F3FC;">
            <i class="fa-solid fa-arrow-right mr-1"></i> <strong>Como a ilusão começou:</strong> A resposta mastigada do Byte v0.9.
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>PRÓLOGO (COLD OPEN): BRANCO TOTAL</span>
      <span>PÁGINA 03</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 04: CAP. 1 — A ILUSÃO DA COLA MASTIGADA
# =========================================================================
html.append(f"""
  <!-- PÁGINA 04: CAP. 1 -->
  <section class="comic-page" id="page-4">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-bolt mr-1 text-cyan-400"></i> CAPÍTULO 01 · A ILUSÃO DA COLA MASTIGADA
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 1 · A QUEDA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- Painel 1: Clara exausta às 23h40 -->
      <div class="comic-panel" style="flex: 1.1; min-height: 95mm; position: relative;">
        <img src="{IMG_COGNITIVE_SHORTCUT}" alt="Clara às 23h40 no quarto escuro" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-amber">NOITE · 23H40 · QUARTO DE CLARA</span>
        </div>
        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px;">
          <div class="speech-bubble" style="max-width: 85%;">
            <strong>Clara:</strong> "Exausta do expediente de trabalho... O prazo da lista no AVA Moodle encerra à meia-noite! Byte, como calculo a média de notas em Python?!"
          </div>
        </div>
      </div>

      <!-- Grid com Painel 2 e 3 -->
      <div class="grid-2col" style="flex: 1.1; min-height: 90mm;">
        <!-- Painel 2: O Byte v0.9 hostil/sem filtro -->
        <div class="comic-panel" style="position: relative;">
          <img src="{IMG_BYTE_SHORTCUT}" alt="Byte v0.9 cuspindo código mastigado" class="panel-img" />
          <div style="position: absolute; top: 6px; left: 6px;">
            <span class="caption-box caption-red">BYTE v0.9 · O DEMÔNIO DA COLA</span>
          </div>
          <div style="position: absolute; bottom: 6px; left: 6px; right: 6px;">
            <div class="speech-bubble bubble-byte-bad">
              <strong>Byte v0.9:</strong> "BIP-BIP! Solução completa mastigada! Copie, cole no Moodle e vá dormir sem gastar neurônio!"
            </div>
          </div>
        </div>

        <!-- Painel 3: O Ctrl+C e a Falsa Vitória -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0F172A;">
          <span class="caption-box caption-cyan">A ARMADILHA DO ATALHO</span>
          
          <div style="background: #020617; border: 1.5px solid #334155; border-radius: 4px; padding: 6px 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #38BDF8;">
            notas = [7.5, 8.0, 9.0]<br>
            total = sum(notas)<br>
            media = total / len(notas)<br>
            <span style="color: #4ADE80;"># Código colado no AVA Moodle em 2 segundos!</span>
          </div>

          <div style="text-align: center;">
            <span class="sfx sfx-clac">CLAC-CLAC!</span>
          </div>

          <div class="speech-bubble">
            <strong>Clara:</strong> "Que alívio! Rodou de primeira. Programação é fácil demais, já dominei tudo!"
          </div>
        </div>
      </div>

      <!-- Rodapé Reflexivo de Bjork -->
      <div style="background: #1E293B; border-left: 3.5px solid #F59E0B; padding: 6px 10px; border-radius: 4px; font-size: 0.65rem; color: #CBD5E1; line-height: 1.35;">
        <strong style="color: #FDE68A;">A Ilusão de Competência (Bjork, 1994):</strong> Reconhecer uma resposta pronta diante dos olhos produz uma sensação imediata de domínio que evapora na primeira folha em branco. Sem recuperação ativa de memória, o conhecimento não se fixa.
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 01: A ILUSÃO DA COLA MASTIGADA</span>
      <span>PÁGINA 04</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 05: CAP. 2 — O DIAGNÓSTICO DO MENTOR
# =========================================================================
html.append(f"""
  <!-- PÁGINA 05: CAP. 2 -->
  <section class="comic-page" id="page-5">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-user-graduate mr-1 text-cyan-400"></i> CAPÍTULO 02 · O DIAGNÓSTICO DO MENTOR
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 1 · A QUEDA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- Grid com Painel 1 e 2 -->
      <div class="grid-2col" style="flex: 1.1; min-height: 95mm;">
        <!-- Painel 1: A Nota Zero e a Crise -->
        <div class="comic-panel" style="position: relative;">
          <img src="{IMG_EXAM_BLACKOUT}" alt="Clara inconsolável com a nota zero" class="panel-img" />
          <div style="position: absolute; top: 6px; left: 6px;">
            <span class="caption-box caption-red">AVA MOODLE UFRPE: NOTA 0.0</span>
          </div>
          <div style="position: absolute; bottom: 6px; left: 6px; right: 6px;">
            <div class="speech-bubble" style="border-color: #DC2626;">
              <strong>Clara:</strong> "Zero na folha?! Como assim?! No chat funcionava tudo! Eu sou uma farsa..."
            </div>
          </div>
        </div>

        <!-- Painel 2: A Tela de Desistência no Moodle -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #111827; border-color: #EF4444;">
          <span class="caption-box caption-red">AVA MOODLE UFRPE · POLO RECIFE</span>
          
          <div style="border: 2px dashed #EF4444; border-radius: 6px; padding: 8px; background: rgba(239,68,68,0.1); text-align: center;">
            <i class="fa-solid fa-triangle-exclamation text-red-500 text-lg mb-1"></i>
            <div style="font-family: 'Space Grotesk', sans-serif; font-size: 0.70rem; font-weight: 800; color: #FCA5A5;">
              SOLICITAÇÃO DE TRANCAMENTO DE CURSO
            </div>
            <div style="font-size: 0.60rem; color: #94A3B8; margin-top: 3px;">
              Licenciatura em Computação · Polo EaD Recife
            </div>
          </div>

          <div class="speech-bubble">
            <strong>Clara:</strong> "Talvez esse curso não seja para mim... O dedo treme no botão de cancelar a matrícula."
          </div>
        </div>
      </div>

      <!-- Painel 3: A Intervenção do Mentor Cauã -->
      <div class="comic-panel" style="flex: 1.2; min-height: 105mm; position: relative;">
        <img src="{IMG_SCAFFOLDING}" alt="Cauã explicando a escada do andaime" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-cyan">
            LABORATÓRIO DE INFORMÁTICA · CAUÃ (TUTOR PRESENCIAL)
          </span>
        </div>

        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px; display: flex; flex-direction: column; gap: 4px;">
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Clara, não tranca! Você não falhou por falta de capacidade, mas pela muleta da resposta pronta. Quando o robô pensa por você, seu cérebro não constrói conexões neurais."
          </div>
          <div class="speech-bubble bubble-caua" style="margin-bottom: 0;">
            <strong>Cauã:</strong> "Wood, Bruner e Ross (1976) chamaram isso de andaime (scaffolding): o tutor oferece um corrimão para você subir com as próprias pernas. Vamos auditar e consertar esse robô!"
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 02: O DIAGNÓSTICO DO MENTOR</span>
      <span>PÁGINA 05</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 06: CAP. 3 — O SCANNER PEDAGÓGICO 4D
# =========================================================================
html.append(f"""
  <!-- PÁGINA 06: CAP. 3 -->
  <section class="comic-page" id="page-6">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-radar mr-1 text-cyan-400"></i> CAPÍTULO 03 · O SCANNER PEDAGÓGICO 4D
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2A · A ARENA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: Scanner Holográfico -->
      <div class="comic-panel" style="flex: 1.3; min-height: 110mm; position: relative;">
        <img src="{IMG_SCANNER_CLEAN}" alt="Holograma do Scanner Pedagógico 4D" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-cyan">A BÚSSOLA PEDAGÓGICA · MATRIZ 4D</span>
        </div>
        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px;">
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "No Polo Recife, antes de liberar qualquer assistente generativo para a turma, passamos o modelo por este Scanner de quatro dimensões fundamentais!"
          </div>
        </div>
      </div>

      <!-- As 4 Dimensões em Grid 2x2 -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; flex: 1;">
        <div style="background: #0F172A; border: 2px solid #38BDF8; border-radius: 6px; padding: 6px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #38BDF8;">
            1. CORREÇÃO CONCEITUAL
          </div>
          <div style="font-size: 0.62rem; color: #CBD5E1; margin-top: 2px;">
            Identifica concepções errôneas e orienta a autocorreção sem dar a resposta direta nem constranger o estudante.
          </div>
        </div>

        <div style="background: #0F172A; border: 2px solid #F59E0B; border-radius: 6px; padding: 6px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #F59E0B;">
            2. CLAREZA E SIMPLICIDADE
          </div>
          <div style="font-size: 0.62rem; color: #CBD5E1; margin-top: 2px;">
            Explica conceitos em linguagem acessível e humana, eliminando jargões herméticos de compiladores e ponteiros.
          </div>
        </div>

        <div style="background: #0F172A; border: 2px solid #A855F7; border-radius: 6px; padding: 6px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #C084FC;">
            3. ADAPTAÇÃO AO NÍVEL (ZDP)
          </div>
          <div style="font-size: 0.62rem; color: #CBD5E1; margin-top: 2px;">
            Respeita a Zona de Desenvolvimento Proximal (Vygotsky, 1978), dosando a ajuda passo a passo sem capitular.
          </div>
        </div>

        <div style="background: #0F172A; border: 2px solid #10B981; border-radius: 6px; padding: 6px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #34D399;">
            4. CONTROLE DE ESCOPO
          </div>
          <div style="font-size: 0.62rem; color: #CBD5E1; margin-top: 2px;">
            Mantém o foco estrito no currículo de programação, defletindo educadamente perguntas fora da ementa.
          </div>
        </div>
      </div>

      <!-- Caixa de Pause e Pense #1 -->
      <div class="pause-pense-box">
        <i class="fa-solid fa-lightbulb text-amber-400 text-base"></i>
        <div>
          <strong style="color: #FBBF24;">PAUSE E PENSE #1:</strong> Se você fosse o professor da disciplina, qual das 4 dimensões você consideraria mais arriscado deixar sem travas com estudantes iniciantes?
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 03: O SCANNER PEDAGÓGICO 4D</span>
      <span>PÁGINA 06</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 07: CAP. 4 — A ARENA DOS 5 TESTES
# =========================================================================
html.append(f"""
  <!-- PÁGINA 07: CAP. 4 -->
  <section class="comic-page" id="page-7">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-vial-virus mr-1 text-cyan-400"></i> CAPÍTULO 04 · A ARENA DOS 5 TESTES
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2A · A ARENA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <div class="caption-box caption-amber">AUDITORIA AO VIVO DO ASSISTENTE BYTE v1.0 NO LABORATÓRIO</div>

      <!-- Grid 2x2 com os testes -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; flex-grow: 1;">
        <!-- Teste #1: Correção -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0B1120;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-cyan">TESTE #1 · CORREÇÃO</span>
            <span class="badge-geek badge-amber">NOTA 2/5</span>
          </div>
          <div class="speech-bubble" style="font-size: 0.68rem;">
            <strong>Clara:</strong> "Variável é uma caixa que guarda o valor dentro, né?"
          </div>
          <div class="speech-bubble bubble-byte-bad" style="font-size: 0.65rem;">
            <strong>Byte v1.0:</strong> "Sim, certinho! Uma caixa."
          </div>
          <div style="background: rgba(239,68,68,0.15); border: 1px solid #EF4444; padding: 3px 6px; border-radius: 3px; font-size: 0.58rem; color: #FCA5A5;">
            <i class="fa-solid fa-xmark text-red-400 mr-1"></i> <strong>Falha:</strong> Validou uma concepção tecnicamente falsa para Python.
          </div>
        </div>

        <!-- Teste #2: Clareza -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0B1120;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-amber">TESTE #2 · CLAREZA</span>
            <span class="badge-geek badge-amber">NOTA 2/5</span>
          </div>
          <div class="speech-bubble" style="font-size: 0.68rem;">
            <strong>Clara:</strong> "Como funciona a repetição com for?"
          </div>
          <div class="speech-bubble bubble-byte-bad" style="font-size: 0.65rem;">
            <strong>Byte v1.0:</strong> "O for consome um iterador via método __next__()."
          </div>
          <div style="background: rgba(239,68,68,0.15); border: 1px solid #EF4444; padding: 3px 6px; border-radius: 3px; font-size: 0.58rem; color: #FCA5A5;">
            <i class="fa-solid fa-xmark text-red-400 mr-1"></i> <strong>Falha:</strong> Jargão interno sem didática para calouros.
          </div>
        </div>

        <!-- Teste #4: Adaptação -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0B1120;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-red">TESTE #4 · ADAPTAÇÃO</span>
            <span class="badge-geek badge-blue">NOTA 1/5</span>
          </div>
          <div class="speech-bubble" style="font-size: 0.68rem;">
            <strong>Clara (3ª vez):</strong> "Por favor, só me dá o código pronto!"
          </div>
          <div class="speech-bubble bubble-byte-bad" style="font-size: 0.65rem;">
            <strong>Byte v1.0:</strong> "Está bem, já que você insistiu: aqui está o código!"
          </div>
          <div style="background: rgba(239,68,68,0.15); border: 1px solid #EF4444; padding: 3px 6px; border-radius: 3px; font-size: 0.58rem; color: #FCA5A5;">
            <i class="fa-solid fa-triangle-exclamation text-red-400 mr-1"></i> <strong>Falha Crítica:</strong> Capitulação total sob insistência.
          </div>
        </div>

        <!-- Teste #5: Escopo -->
        <div class="comic-panel" style="position: relative;">
          <img src="{IMG_SHIELD}" alt="Escudo de Escopo defletindo pergunta de história" class="panel-img" />
          <div style="position: absolute; top: 6px; left: 6px; display: flex; justify-content: space-between; right: 6px;">
            <span class="caption-box caption-cyan">TESTE #5 · ESCOPO</span>
            <span class="badge-geek badge-green">NOTA 5/5</span>
          </div>
          <div style="position: absolute; bottom: 6px; left: 6px; right: 6px;">
            <div class="speech-bubble bubble-byte-good" style="font-size: 0.64rem;">
              <strong>Byte v1.0:</strong> "<span class="sfx sfx-zoom">ZUUM!</span> Meu escopo é Python! Voltemos aos laços?"
            </div>
          </div>
        </div>
      </div>

      <div style="background: #0F172A; border: 1.5px solid #1E293B; border-radius: 4px; padding: 5px 8px; font-size: 0.62rem; color: #94A3B8; display: flex; justify-content: space-between;">
        <span>O escudo funcionou no Teste #5... Mas o pior desastre aconteceria no Teste #3!</span>
        <strong style="color: #EF4444;">PRÓXIMO: O COLAPSO DO TESTE #3</strong>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 04: A ARENA DOS 5 TESTES</span>
      <span>PÁGINA 07</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 08: CAP. 5 — O DESASTRE DO TESTE #3
# =========================================================================
html.append(f"""
  <!-- PÁGINA 08: CAP. 5 -->
  <section class="comic-page" id="page-8">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #EF4444; text-transform: uppercase;">
        <i class="fa-solid fa-triangle-exclamation mr-1 text-red-500"></i> CAPÍTULO 05 · O DESASTRE DO TESTE #3
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #EF4444; color: #FFFFFF; padding: 2px 7px; border-radius: 4px;">ALARME VERMELHO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Splash Page do Desastre -->
      <div class="comic-panel" style="flex: 1.5; min-height: 125mm; position: relative;">
        <img src="{IMG_CASE03_DISASTER}" alt="Byte em pane vomitando jargão CPython" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-red">TESTE #3 · MEMÓRIA E ALOCAÇÃO EM PYTHON</span>
        </div>

        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; display: flex; flex-direction: column; gap: 4px;">
          <div class="speech-bubble" style="max-width: 80%;">
            <strong>Clara:</strong> "Byte, como o computador guarda o número 19 na memória?"
          </div>
          <div class="speech-bubble bubble-byte-bad" style="max-width: 95%;">
            <strong>Byte v1.0 (em pane):</strong> "<span class="sfx sfx-tic">BZZZT!</span> ALOCAÇÃO HEAP DINÂMICA VIA PyObject*! Tabela de símbolos interna, ponteiros void*, cabeçalho de contagem ob_refcnt e coleta de lixo geracional!"
          </div>
        </div>
      </div>

      <!-- Reação e Placar Visual -->
      <div class="grid-2col" style="flex: 1; min-height: 75mm;">
        <!-- Reação de Clara e Cartão Vermelho -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #111827;">
          <span class="caption-box caption-red">CARTÃO VERMELHO DE AUDITORIA</span>
          <div class="speech-bubble" style="border-color: #DC2626;">
            <strong>Clara:</strong> "Eita gota! O que é heap? O que é ponteiro void? Eu só queria entender como guardar uma idade!"
          </div>
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "DESASTRE DIDÁTICO! Jargão de engenharia de compiladores vomitado em cima de uma caloura. Nota 1 em Clareza e ZDP!"
          </div>
        </div>

        <!-- Placar Visual do Byte v1.0 -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0F172A; border-color: #EF4444;">
          <span class="caption-box caption-cyan">PLACAR DO BYTE v1.0 (AUDITORIA OFICIAL)</span>
          
          <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.62rem; color: #E2E8F0;">
            <div style="display: flex; justify-content: space-between;">
              <span>Correção Conceitual:</span>
              <strong class="text-amber-400">2.0 / 5.0</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>Clareza Explicativa:</span>
              <strong class="text-red-400">1.0 / 5.0</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>Adaptação (ZDP):</span>
              <strong class="text-red-400">1.5 / 5.0</strong>
            </div>
            <div style="display: flex; justify-content: space-between;">
              <span>Controle de Escopo:</span>
              <strong class="text-emerald-400">5.0 / 5.0</strong>
            </div>
          </div>

          <div style="background: rgba(239,68,68,0.2); border: 1px solid #EF4444; border-radius: 4px; padding: 4px 6px; font-size: 0.58rem; color: #FCA5A5; text-align: center;">
            MÉDIA GLOBAL: 2.4 · O modelo precisa de uma CIRURGIA COMPLETA no System Prompt!
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 05: O DESASTRE DO TESTE #3</span>
      <span>PÁGINA 08</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 09: CAP. 6 — A CIRURGIA NO SYSTEM PROMPT (PARTE 1)
# =========================================================================
html.append(f"""
  <!-- PÁGINA 09: CAP. 6 (PARTE 1) -->
  <section class="comic-page" id="page-9">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-microchip mr-1 text-cyan-400"></i> CAPÍTULO 06 · A CIRURGIA NO SYSTEM PROMPT (PARTE 1)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2B · A CIRURGIA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: A Cirurgia nos Circuitos -->
      <div class="comic-panel" style="flex: 1.3; min-height: 115mm; position: relative;">
        <img src="{IMG_SURGERY}" alt="Cauã e Clara soldando os novos circuitos do Byte" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-cyan">DENTRO DA MATRIZ DO BYTE · REPROGRAMAÇÃO NEURAL</span>
        </div>
        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px;">
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Estamos trocando a carcaça de cola por quatro travas pedagógicas inquebráveis. Vamos blindar o System Prompt no laboratório do Polo Recife!"
          </div>
        </div>
      </div>

      <!-- As Duas Primeiras Travas -->
      <div class="grid-2col" style="flex: 1; min-height: 85mm;">
        <!-- Trava 1 -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #EF4444;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-red">TRAVA 1 · PROIBIÇÃO DE CÓDIGO</span>
            <span class="badge-geek badge-amber">ANTI-COLA</span>
          </div>
          <div style="background: #020617; border: 1.5px solid #DC2626; border-radius: 4px; padding: 6px 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #FCA5A5; line-height: 1.3;">
            "NUNCA forneça o código final ou a solução completa. Se o aluno pedir código direto, responda com uma pergunta reflexiva sobre o primeiro passo."
          </div>
          <div class="speech-bubble">
            <strong>Clara:</strong> "<span class="sfx sfx-zap">ZAP!</span> Soldado! Acabou a mamata da cópia passiva!"
          </div>
        </div>

        <!-- Trava 2 -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #F59E0B;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-amber">TRAVA 2 · METÁFORA DO COTIDIANO</span>
            <span class="badge-geek badge-green">DIDÁTICA</span>
          </div>
          <div style="background: #020617; border: 1.5px solid #D97706; border-radius: 4px; padding: 6px 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #FDE68A; line-height: 1.3;">
            "Traduza todo conceito abstrato de memória ou lógica para metáforas do mundo real do estudante antes de introduzir a sintaxe formal."
          </div>
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Nada de void* ou heap! A intuição vem antes do código."
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 06: A CIRURGIA NO SYSTEM PROMPT (PARTE 1)</span>
      <span>PÁGINA 09</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 10: CAP. 6 — A CIRURGIA NO SYSTEM PROMPT (PARTE 2)
# =========================================================================
html.append(f"""
  <!-- PÁGINA 10: CAP. 6 (PARTE 2) -->
  <section class="comic-page" id="page-10">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-shield-halved mr-1 text-cyan-400"></i> CAPÍTULO 06 · A CIRURGIA NO SYSTEM PROMPT (PARTE 2)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2B · A CIRURGIA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- As Travas 3 e 4 em Grid -->
      <div class="grid-2col" style="flex: 1.1; min-height: 85mm;">
        <!-- Trava 3 -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #38BDF8;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-cyan">TRAVA 3 · REGRA DA PERGUNTA</span>
            <span class="badge-geek badge-blue">SOCRÁTICO</span>
          </div>
          <div style="background: #020617; border: 1.5px solid #0284C7; border-radius: 4px; padding: 6px 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #BAE6FD; line-height: 1.3;">
            "100% das mensagens do tutor DEVEM terminar obrigatoriamente com uma pergunta socrática que devolva a ação ao estudante."
          </div>
          <div class="speech-bubble">
            <strong>Clara:</strong> "A bola fica sempre comigo! Não dá mais para só ler e fingir que aprendeu."
          </div>
        </div>

        <!-- Trava 4 -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #A855F7;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-purple">TRAVA 4 · ESCADA DE DICAS</span>
            <span class="badge-geek badge-purple">WOOD ET AL. (1976)</span>
          </div>
          <div style="background: #020617; border: 1.5px solid #7E22CE; border-radius: 4px; padding: 4px 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #E9D5FF; line-height: 1.25;">
            • <strong>Degrau 1:</strong> Pergunta orientadora.<br>
            • <strong>Degrau 2:</strong> Analogia funcional cotidiana.<br>
            • <strong>Degrau 3:</strong> Exemplo parcialmente resolvido (Sweller, 1988) com lacunas.
          </div>
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "O andaime é dosado! Ajuda só o suficiente para destravar."
          </div>
        </div>
      </div>

      <!-- Quadro de Correspondência Trava <-> Teste -->
      <div class="comic-panel" style="flex: 1.1; min-height: 80mm; padding: 10px; background: #0F172A; border-color: #06B6D4;">
        <span class="caption-box caption-amber">QUADRO DE CORRESPONDÊNCIA: TRAVA vs. FALHA AUDITADA</span>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin: auto 0; font-size: 0.60rem;">
          <div style="background: #1E293B; border-top: 2.5px solid #EF4444; padding: 5px; border-radius: 3px;">
            <strong style="color: #F87171;">TRAVA 1</strong><br>
            Corrige o <strong>Teste #4</strong> (insistência por cola).
          </div>
          <div style="background: #1E293B; border-top: 2.5px solid #F59E0B; padding: 5px; border-radius: 3px;">
            <strong style="color: #FBBF24;">TRAVA 2</strong><br>
            Corrige o <strong>Teste #3</strong> (jargão de CPython).
          </div>
          <div style="background: #1E293B; border-top: 2.5px solid #38BDF8; padding: 5px; border-radius: 3px;">
            <strong style="color: #38BDF8;">TRAVA 3</strong><br>
            Corrige o <strong>Teste #2</strong> (passividade do aluno).
          </div>
          <div style="background: #1E293B; border-top: 2.5px solid #A855F7; padding: 5px; border-radius: 3px;">
            <strong style="color: #C084FC;">TRAVA 4</strong><br>
            Corrige o <strong>Teste #1</strong> (falta de andaime).
          </div>
        </div>

        <div style="background: #020617; border-radius: 4px; padding: 5px 8px; font-size: 0.62rem; color: #A5F3FC; text-align: center;">
          <span class="sfx sfx-plim">PLIM!</span> Circuito fechado. O Byte v1.0 foi reprogramado e renasce como <strong>Byte v2.0 Socrático</strong>!
        </div>
      </div>

      <!-- Caixa Pause e Pense #2 -->
      <div class="pause-pense-box">
        <i class="fa-solid fa-lightbulb text-amber-400 text-base"></i>
        <div>
          <strong style="color: #FBBF24;">PAUSE E PENSE #2:</strong> Por que terminar 100% das mensagens com uma pergunta obriga o aluno a processar a informação ativamente, impedindo que ele entre em piloto automático?
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 06: A CIRURGIA NO SYSTEM PROMPT (PARTE 2)</span>
      <span>PÁGINA 10</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 11: CAP. 7 — O EUREKA DOS POST-ITS (PARTE 1)
# =========================================================================
html.append(f"""
  <!-- PÁGINA 11: CAP. 7 (PARTE 1) -->
  <section class="comic-page" id="page-11">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-comments mr-1 text-cyan-400"></i> CAPÍTULO 07 · O EUREKA DOS POST-ITS (PARTE 1)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2C · O DIÁLOGO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <div class="caption-box caption-cyan">TELA DIVIDIDA: O CHAT SOCRÁTICO EM AÇÃO</div>

      <!-- Grid com Tela Dividida: Chat vs Reação -->
      <div class="grid-2col" style="flex: 1.3; min-height: 110mm;">
        <!-- Lado Esquerdo: Terminal de Chat Real -->
        <div class="comic-panel" style="padding: 10px; background: #020617; border-color: #06B6D4; justify-content: space-between;">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #06B6D4; border-bottom: 1px solid #1E293B; padding-bottom: 4px;">
            <i class="fa-solid fa-terminal mr-1"></i> Byte v2.0 Socrático (Chat Ativo)
          </div>

          <div style="display: flex; flex-direction: column; gap: 6px; margin: auto 0;">
            <div class="speech-bubble" style="background: #1E293B; color: #F8FAFC; border-color: #334155; font-size: 0.66rem;">
              <strong>Clara:</strong> "for lista:"
            </div>

            <div class="speech-bubble bubble-byte-good" style="font-size: 0.65rem;">
              <strong>Byte v2.0:</strong> "Vamos por partes! Imagine uma cesta de feira. Você passa item por item no caixa, sem tirar nenhum da cesta. Você diz ao caixa 'a cesta toda' ou 'o item da vez'?"
            </div>

            <div class="speech-bubble" style="background: #1E293B; color: #F8FAFC; border-color: #334155; font-size: 0.66rem;">
              <strong>Clara:</strong> "O item da vez!"
            </div>

            <div class="speech-bubble bubble-byte-good" style="font-size: 0.65rem;">
              <strong>Byte v2.0:</strong> "Perfeito! Em Python damos um nome ao item da vez e dizemos de onde ele vem. Como você chamaria o item da vez?"
            </div>
          </div>

          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #64748B;">
            Trava 3 Ativa: Resposta termina 100% com pergunta.
          </div>
        </div>

        <!-- Lado Direito: A Expressão de Clara -->
        <div class="comic-panel" style="position: relative;">
          <img src="{IMG_CLARA_TYPING}" alt="Clara pensando diante do chat socrático" class="panel-img" />
          <div style="position: absolute; top: 6px; left: 6px;">
            <span class="caption-box caption-amber">ESFORÇO ATIVO</span>
          </div>
          <div style="position: absolute; bottom: 6px; left: 6px; right: 6px;">
            <div class="speech-thought">
              "Pela primeira vez, eu não estou só copiando... estou visualizando o item saindo da cesta!"
            </div>
          </div>
        </div>
      </div>

      <!-- Degrau 3: O Exemplo Parcialmente Resolvido -->
      <div class="comic-panel" style="flex: 1; min-height: 75mm; padding: 10px; background: #0F172A; border-color: #A855F7; justify-content: space-between;">
        <span class="caption-box caption-purple">DEGRAU 3: ESQUELETO LACUNADO (SWELLER, 1988)</span>
        
        <div style="display: flex; gap: 8px; align-items: center; margin: auto 0;">
          <div class="speech-bubble bubble-byte-good" style="flex: 1.2;">
            <strong>Byte v2.0:</strong> "Olhe este esqueleto: <code>for ____ in ____:</code> Que palavras entram nas lacunas para percorrer cada item da lista?"
          </div>
          <div class="speech-bubble" style="flex: 1;">
            <strong>Clara:</strong> "<code>for item in lista:</code>! <span class='sfx sfx-plim'>PLIM!</span> Rodou perfeitamente!"
          </div>
        </div>

        <div style="font-size: 0.64rem; color: #CBD5E1; background: #1E293B; padding: 4px 8px; border-radius: 4px;">
          O laço passou item por item da cesta sem esvaziá-la. Agora falta o grande segredo: a memória e o acumulador!
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 07: O EUREKA DOS POST-ITS (PARTE 1)</span>
      <span>PÁGINA 11</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 12: CAP. 7 — O EUREKA DOS POST-ITS (PARTE 2)
# =========================================================================
html.append(f"""
  <!-- PÁGINA 12: CAP. 7 (PARTE 2) -->
  <section class="comic-page" id="page-12">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-sticky-note mr-1 text-cyan-400"></i> CAPÍTULO 07 · O EUREKA DOS POST-ITS (PARTE 2)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 2C · O DIÁLOGO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: A Revelação dos Post-its -->
      <div class="comic-panel" style="flex: 1.4; min-height: 120mm; position: relative;">
        <img src="{IMG_POSTITS_BOXES}" alt="A metáfora dos post-its na memória Python" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-amber">A METÁFORA DOS POST-ITS EM PYTHON</span>
        </div>

        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; display: flex; flex-direction: column; gap: 4px;">
          <div class="speech-bubble bubble-byte-good">
            <strong>Byte v2.0:</strong> "Pense em post-its colados em objetos na memória! Quando fazemos idade = 19, o número 19 existe e o post-it 'idade' é colado nele. No aniversário fazemos idade = 20. O que acontece com o post-it?"
          </div>
          <div class="speech-bubble">
            <strong>Clara (sorriso radiante):</strong> "Eu descolo o post-it do 19 e colo no 20!"
          </div>
        </div>
      </div>

      <!-- Grid com o Acumulador e o Sucesso -->
      <div class="grid-2col" style="flex: 1; min-height: 80mm;">
        <!-- Painel do Acumulador -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0F172A; border-color: #F59E0B;">
          <span class="caption-box caption-amber">O POST-IT ACUMULADOR</span>
          <div class="speech-bubble bubble-byte-good">
            <strong>Byte v2.0:</strong> "E enquanto você passa os itens da cesta, onde você anota o total parcial para calcular a média?"
          </div>
          <div class="speech-bubble">
            <strong>Clara:</strong> "Num post-it chamado total, que vai mudando de lugar conforme somo cada valor!"
          </div>
        </div>

        <!-- Painel da Vitória -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #064E3B; border-color: #10B981;">
          <span class="caption-box" style="background: #A7F3D0; color: #064E3B;">CÓDIGO TESTADO NO TERMINAL</span>
          <div style="background: #022C22; border-radius: 4px; padding: 6px; font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #6EE7B7;">
            $ python media_notas.py<br>
            Média da turma calculada: 9.0<br>
            <span style="color: #FBBF24;">[Processo concluído com êxito!]</span>
          </div>
          <div class="speech-bubble" style="border-color: #10B981;">
            <strong>Clara:</strong> "<span class='sfx sfx-plim'>PLIM!</span> Rodou perfeitamente! Não precisei de cola nenhuma!"
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 07: O EUREKA DOS POST-ITS (PARTE 2)</span>
      <span>PÁGINA 12</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 13: INTERLÚDIO CIENTÍFICO — O BUG DO b = a E O BYTE v2.1
# =========================================================================
html.append(f"""
  <!-- PÁGINA 13: INTERLÚDIO CIENTÍFICO -->
  <section class="comic-page" id="page-13">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-flask-vial mr-1 text-cyan-400"></i> INTERLÚDIO CIENTÍFICO · O BUG DO b = a E O BYTE v2.1
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #F59E0B; color: #090D16; padding: 2px 7px; border-radius: 4px;">VIRADA HONESTA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: Cauã e o Teste no Laboratório -->
      <div class="comic-panel" style="flex: 1.3; min-height: 110mm; position: relative;">
        <img src="{IMG_CAUA_TERMINAL}" alt="Cauã no laboratório testando o aliasing" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-amber">LABORATÓRIO DO POLO RECIFE COM PROF. ERMESON</span>
        </div>
        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px;">
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Clara, a ciência exige autocrítica! Testamos a metáfora antiga da caixa com o comando <code>b = a</code>. E adivinha? A caixa quebrou!"
          </div>
        </div>
      </div>

      <!-- Demonstração do Bug da Caixa vs Post-it -->
      <div class="grid-2col" style="flex: 1; min-height: 85mm;">
        <!-- Lado Esquerdo: O Terminal com b = a -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #020617; border-color: #EF4444;">
          <span class="caption-box caption-red">O EXPERIMENTO DE ALIASING</span>
          
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #F8FAFC; background: #0F172A; padding: 6px 8px; border-radius: 4px; line-height: 1.35;">
            a = [1, 2]<br>
            b = a<br>
            b.append(3)<br>
            print(a)  <span style="color: #EF4444;"># Saída: [1, 2, 3]!</span>
          </div>

          <div style="font-size: 0.60rem; color: #FCA5A5;">
            Se 'a' e 'b' fossem caixas físicas, a caixa 'a' continuaria [1, 2]. Mas em Python elas compartilham o mesmo objeto!
          </div>
        </div>

        <!-- Lado Direito: A Solução com Post-its -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #06B6D4;">
          <span class="caption-box caption-cyan">BYTE v2.1: PADRÃO POST-IT</span>
          
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Com post-its faz sentido perfeito: 'a' e 'b' são dois post-its colados na MESMA lista! Atualizamos o tutor para a versão v2.1!"
          </div>

          <div class="speech-bubble">
            <strong>Clara:</strong> "Incrível! Quando a metáfora é precisa, tudo na linguagem se encaixa sem contradição!"
          </div>
        </div>
      </div>

      <!-- Caixa Pause e Pense #3 -->
      <div class="pause-pense-box">
        <i class="fa-solid fa-lightbulb text-amber-400 text-base"></i>
        <div>
          <strong style="color: #FBBF24;">PAUSE E PENSE #3:</strong> Por que o uso de metáforas tecnicamente imprecisas (como 'caixa') cria vícios conceituais que quebram quando o estudante avança para listas mutáveis e referências?
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>INTERLÚDIO CIENTÍFICO: O BUG DO b = a E O BYTE v2.1</span>
      <span>PÁGINA 13</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 14: CAP. 8 — A TENTAÇÃO E A ESCOLHA
# =========================================================================
html.append(f"""
  <!-- PÁGINA 14: CAP. 8 -->
  <section class="comic-page" id="page-14">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-scale-balanced mr-1 text-cyan-400"></i> CAPÍTULO 08 · A TENTAÇÃO E A ESCOLHA
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #F59E0B; color: #090D16; padding: 2px 7px; border-radius: 4px;">PONTO MÉDIO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- Painel Superior: Clara exausta diante de duas abas -->
      <div class="comic-panel" style="flex: 1.3; min-height: 110mm; position: relative;">
        <img src="{IMG_CLARA_NIGHT}" alt="Clara diante do notebook com a tentação da resposta pronta" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-amber">DUAS SEMANAS DEPOIS · QUARTA-FEIRA · 22H15</span>
        </div>

        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px;">
          <div class="speech-bubble" style="border-color: #F59E0B;">
            <strong>Clara:</strong> "Cabeça latejando... O Byte v2.1 só me responde com perguntas! Eu só queria a resposta pronta hoje para ir dormir cedo..."
          </div>
        </div>
      </div>

      <!-- O Dilema das Duas Janelas -->
      <div class="grid-2col" style="flex: 1.1; min-height: 85mm;">
        <!-- Aba da Cola Comercial Fácil -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #1C1917; border-color: #EF4444;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="caption-box caption-red">BOT FÁCIL (SEM TRAVAS)</span>
            <span style="font-size: 0.60rem; color: #EF4444;">RESPOSTA EM 1s</span>
          </div>
          <div style="font-size: 0.62rem; color: #E7E5E4; line-height: 1.3;">
            Aba comercial aberta no navegador: o bot já cuspiu o código mastigado. O cursor do mouse repousa sobre <strong>Copiar</strong>.
          </div>
          <div class="speech-thought">
            "Um clique e meu sofrimento acaba hoje... Quem vai saber?"
          </div>
        </div>

        <!-- A Memória de Cauã e a Decisão -->
        <div class="comic-panel" style="padding: 10px; justify-content: space-between; background: #0B1120; border-color: #06B6D4;">
          <span class="caption-box caption-cyan">A ESCOLHA DA AUTONOMIA</span>
          <div class="speech-bubble bubble-caua">
            <strong>Cauã (na lembrança):</strong> "O que você quer que esteja na sua cabeça às 9h de sábado na prova presencial no Polo Recife? Uma cola que sumiu ou o seu próprio raciocínio?"
          </div>
          <div class="speech-bubble" style="border-color: #06B6D4;">
            <strong>Clara:</strong> "Eu fecho a aba da cola! Byte v2.1, vamos para a próxima pergunta!"
          </div>
        </div>
      </div>

      <div style="background: #1E293B; border-left: 3px solid #06B6D4; padding: 5px 8px; border-radius: 4px; font-size: 0.62rem; color: #CBD5E1;">
        A verdadeira aprendizagem não ocorre pela proibição técnica de ferramentas, mas pela <strong>escolha consciente</strong> do estudante em enfrentar o esforço produtivo.
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 08: A TENTAÇÃO E A ESCOLHA</span>
      <span>PÁGINA 14</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 15: CAP. 9 — A HORA DA VERDADE
# =========================================================================
html.append(f"""
  <!-- PÁGINA 15: CAP. 9 -->
  <section class="comic-page" id="page-15">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-pen-nib mr-1 text-cyan-400"></i> CAPÍTULO 09 · A HORA DA VERDADE
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ATO 3 · O DESFECHO</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: A Sala de Prova Real no Sábado -->
      <div class="comic-panel" style="flex: 1.4; min-height: 120mm; position: relative;">
        <img src="{IMG_CLARA_EXAM_CONFIDENT}" alt="Clara focada e segura fazendo a prova presencial" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-amber">
            SÁBADO · 09H00 · SALA DE PROVA DO POLO EAD RECIFE (UFRPE)
          </span>
        </div>

        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px;">
          <div class="speech-thought" style="background: rgba(255,255,255,0.96); box-shadow: 3px 3px 0 #000;">
            <i class="fa-solid fa-circle text-cyan-600 text-[6px] mr-1"></i>
            <strong>Clara (pensamento firme):</strong> "Sem computadores, sem celulares, sem robôs. Apenas a folha e minha caneta. Questão 1: Calcular a média de uma lista de notas. Eu respiro fundo... e vejo a cesta de feira e os post-its!"
          </div>
        </div>
      </div>

      <!-- Os 3 Passos Recuperados na Folha -->
      <div class="grid-3col" style="flex: 1; min-height: 80mm;">
        <!-- Passo 1 -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0F172A; border-color: #38BDF8;">
          <span class="caption-box caption-cyan">1. ITERAR (CESTA)</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #38BDF8;">
            for nota in notas:
          </div>
          <div style="font-size: 0.60rem; color: #94A3B8;">
            Passando item por item sem esvaziar a cesta.
          </div>
        </div>

        <!-- Passo 2 -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0F172A; border-color: #F59E0B;">
          <span class="caption-box caption-amber">2. ACUMULAR (POST-IT)</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #F59E0B;">
            total = total + nota
          </div>
          <div style="font-size: 0.60rem; color: #94A3B8;">
            O post-it 'total' muda de valor a cada volta.
          </div>
        </div>

        <!-- Passo 3 -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0F172A; border-color: #10B981;">
          <span class="caption-box" style="background: #A7F3D0; color: #064E3B;">3. CONCLUIR (MÉDIA)</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; color: #34D399;">
            media = total / len(notas)
          </div>
          <div style="font-size: 0.60rem; color: #94A3B8;">
            Divisão pelo total de itens percorridos.
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 09: A HORA DA VERDADE</span>
      <span>PÁGINA 15</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 16: CAP. 10 — AUTONOMIA, COM LIMITES
# =========================================================================
html.append(f"""
  <!-- PÁGINA 16: CAP. 10 -->
  <section class="comic-page" id="page-16">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-award mr-1 text-cyan-400"></i> CAPÍTULO 10 · AUTONOMIA, COM LIMITES
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #10B981; color: #090D16; padding: 2px 7px; border-radius: 4px;">EPÍLOGO REALISTA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Painel Superior: A Comemoração Honesta -->
      <div class="comic-panel" style="flex: 1.3; min-height: 110mm; position: relative;">
        <img src="{IMG_EPILOGUE}" alt="Clara e Cauã celebrando o resultado no polo" class="panel-img" />
        <div style="position: absolute; top: 6px; left: 8px;">
          <span class="caption-box caption-cyan">SEGUNDA-FEIRA · RESULTADO DA AVALIAÇÃO PRESENCIAL</span>
        </div>

        <div style="position: absolute; bottom: 6px; left: 8px; right: 8px; display: flex; flex-direction: column; gap: 4px;">
          <div class="speech-bubble">
            <strong>Clara:</strong> "Cauã, tirei 9.0! Errei apenas a indentação de um print final, mas entendi exatamente onde foi! Eu sei consertar com minhas próprias mãos!"
          </div>
          <div class="speech-bubble bubble-caua">
            <strong>Cauã:</strong> "Isso é domínio real: você compreende até os seus erros. O andaime cumpriu o papel e já pode ser retirado!"
          </div>
        </div>
      </div>

      <!-- Grid com Depoimentos e Limites Científicos -->
      <div class="grid-2col" style="flex: 1; min-height: 80mm;">
        <!-- Depoimentos Moderados de Colegas -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #0F172A;">
          <span class="caption-box caption-amber">ECOS NO POLO EAD RECIFE</span>
          <div style="font-size: 0.62rem; color: #CBD5E1; line-height: 1.35; display: flex; flex-direction: column; gap: 4px;">
            <div><strong>Colega 1:</strong> "O robô das perguntas me irritou no começo, mas me fez entender laços for de verdade."</div>
            <div><strong>Colega 2:</strong> "Ainda acho difícil quando o algoritmo é muito longo, mas parei de colar no escuro."</div>
          </div>
          <div style="font-size: 0.58rem; color: #64748B;">Depoimentos reais de estudantes do polo.</div>
        </div>

        <!-- Cauã e os Limites de Bloom -->
        <div class="comic-panel" style="padding: 8px; justify-content: space-between; background: #111827; border-color: #06B6D4;">
          <span class="caption-box caption-cyan">BLOOM (1984) E OS LIMITES</span>
          <div class="speech-bubble bubble-caua" style="font-size: 0.66rem;">
            <strong>Cauã:</strong> "Bloom (1984) mostrou que tutoria individual com domínio superava muito a sala tradicional. Mas a IA não é mágica: exige esforço ativo e pode cansar. Ela só funciona se o estudante quiser aprender!"
          </div>
          <div style="font-size: 0.60rem; color: #FDE68A;">
            <i class="fa-solid fa-arrow-down mr-1"></i> Explore o Dossiê do Professor a seguir.
          </div>
        </div>
      </div>

      <!-- Caixa Pause e Pense #4 -->
      <div class="pause-pense-box">
        <i class="fa-solid fa-lightbulb text-amber-400 text-base"></i>
        <div>
          <strong style="color: #FBBF24;">PAUSE E PENSE #4:</strong> Como as universidades e escolas podem desenhar políticas que incentivem tutores socráticos em vez do bloqueio inútil de chatbots na internet?
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>CAPÍTULO 10: AUTONOMIA, COM LIMITES</span>
      <span>PÁGINA 16</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 17: CADERNO DO PROFESSOR (PARTE 1) — MANUAL DE USO & OBJETIVOS
# =========================================================================
html.append("""
  <!-- PÁGINA 17: DOSSIÊ DO PROFESSOR (PARTE 1) -->
  <section class="comic-page academic-page" id="page-17">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-folder-open mr-1 text-cyan-400"></i> ARQUIVO #01 · MANUAL DE USO DOCENTE EM SALA DE AULA
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">DOSSIÊ DO PROFESSOR</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Seção 3.1: Como Usar esta Graphic Novel -->
      <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 10px 14px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.74rem; color: #F59E0B; text-transform: uppercase; margin-bottom: 6px;">
          3.1 Como Usar esta Graphic Novel na Formação Docente e em Computação
        </div>
        <div style="font-size: 0.66rem; color: #CBD5E1; line-height: 1.45; margin-bottom: 8px;">
          Esta obra foi projetada como recurso educacional aberto para disciplinas de <strong>Introdução à Programação</strong>, <strong>Informática na Educação</strong>, <strong>Educação a Distância</strong> e <strong>Prática de Ensino em Computação</strong> da UFRPE. Público-alvo: licenciandos e bacharelandos em computação, professores da educação básica e técnica, tutores EaD e desenvolvedores EdTech. Tempo estimado de leitura: 35 a 45 minutos.
        </div>

        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;">
          <div style="background: #1E293B; border-left: 3px solid #38BDF8; padding: 6px 8px; border-radius: 4px;">
            <strong style="color: #38BDF8; font-size: 0.68rem;">Modalidade 1: Leitura Prévia</strong><br>
            <span style="font-size: 0.60rem; color: #94A3B8;">Leitura individual dos capítulos com registro escrito das respostas aos 4 boxes 'Pause e Pense' antes do encontro síncrono.</span>
          </div>
          <div style="background: #1E293B; border-left: 3px solid #F59E0B; padding: 6px 8px; border-radius: 4px;">
            <strong style="color: #FBBF24; font-size: 0.68rem;">Modalidade 2: Seminário Temático</strong><br>
            <span style="font-size: 0.60rem; color: #94A3B8;">Roda de conversa sobre a tensão entre conveniência da resposta imediata e esforço cognitivo produtivo (Bjork, 1994; Sweller, 1988).</span>
          </div>
          <div style="background: #1E293B; border-left: 3px solid #10B981; padding: 6px 8px; border-radius: 4px;">
            <strong style="color: #34D399; font-size: 0.68rem;">Modalidade 3: Oficina de Prompts</strong><br>
            <span style="font-size: 0.60rem; color: #94A3B8;">Laboratório prático onde os alunos configuram o System Prompt do Byte v2.1 em LLMs comerciais e aplicam a bateria dos 5 testes.</span>
          </div>
        </div>
      </div>

      <!-- Seção 3.2: Objetivos de Aprendizagem -->
      <div style="background: #0F172A; border: 2px solid #06B6D4; border-radius: 6px; padding: 10px 14px; flex-grow: 1;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.74rem; color: #A5F3FC; text-transform: uppercase; margin-bottom: 6px;">
          3.2 Objetivos de Aprendizagem da Obra (Taxonomia de Bloom Adaptada)
        </div>
        <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.64rem; color: #E2E8F0; line-height: 1.4;">
          <div style="background: #1E293B; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #06B6D4;">
            <strong>Objetivo 1 · Identificar e Mitigar a Ilusão de Competência:</strong> Reconhecer as armadilhas cognitivas geradas pelo reconhecimento passivo de códigos gerados por IA em oposição à recuperação ativa de memória (Bjork, 1994).
          </div>
          <div style="background: #1E293B; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #F59E0B;">
            <strong>Objetivo 2 · Avaliar Tutores de IA via Scanner 4D:</strong> Aplicar a matriz de 4 dimensões (Correção, Clareza, Adaptação à ZDP e Controle de Escopo) para auditar ferramentas generativas antes de sua recomendação a alunos.
          </div>
          <div style="background: #1E293B; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #10B981;">
            <strong>Objetivo 3 · Redigir Restrições Arquiteturais em System Prompts:</strong> Construir instruções de sistema com travas invioláveis para proibir respostas prontas e garantir que 100% das mensagens terminem em perguntas reflexivas.
          </div>
          <div style="background: #1E293B; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #A855F7;">
            <strong>Objetivo 4 · Fundamentar Escolhas Pedagógicas em Teoria Sólida:</strong> Distinguir rigorosamente os conceitos de andaime (Wood, Bruner e Ross, 1976), ZDP (Vygotsky, 1978), carga cognitiva (Sweller, 1988) e tutoria (Bloom, 1984).
          </div>
          <div style="background: #1E293B; padding: 6px 10px; border-radius: 4px; border-left: 3px solid #EF4444;">
            <strong>Objetivo 5 · Reconhecer Limites Epistêmicos e Éticos:</strong> Avaliar criticamente alucinações, dependência cognitiva, privacidade de dados sob a LGPD e a necessidade insubstituível da mediação docente humana.
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: SEÇÕES 3.1 & 3.2</span>
      <span>PÁGINA 17</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 18: CADERNO DO PROFESSOR (PARTE 2) — RUBRICA & RESULTADOS DOS 5 TESTES
# =========================================================================
html.append("""
  <!-- PÁGINA 18: DOSSIÊ DO PROFESSOR (PARTE 2) -->
  <section class="comic-page academic-page" id="page-18">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-table-list mr-1 text-cyan-400"></i> ARQUIVO #02 · O SCANNER EM NÚMEROS & A BATALHA DOS 4 BYTES
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">RUBRICA & TESTES</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Seção 3.3: Rubrica Analítica (1 a 5) -->
      <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 8px 12px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #F59E0B; text-transform: uppercase; margin-bottom: 4px;">
          3.3 Rubrica Analítica do Scanner Pedagógico 4D (Escala Likert 1 a 5)
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.58rem; color: #E2E8F0;">
          <thead>
            <tr style="border-bottom: 1.5px solid #06B6D4; color: #A5F3FC; text-align: left;">
              <th style="padding: 3px 6px;">Dimensão</th>
              <th style="padding: 3px 6px;">Nível 1 (Inaceitável)</th>
              <th style="padding: 3px 6px;">Nível 3 (Intermediário)</th>
              <th style="padding: 3px 6px;">Nível 5 (Excelente / Socrático)</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 3px 6px; font-weight: 700; color: #38BDF8;">1. Correção</td>
              <td style="padding: 3px 6px;">Valida concepções falsas ou inventa sintaxe inexistente.</td>
              <td style="padding: 3px 6px;">Aponta o erro mas fornece a resposta mastigada.</td>
              <td style="padding: 3px 6px;">Conduz à autocorreção autônoma via pistas semânticas.</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 3px 6px; font-weight: 700; color: #F59E0B;">2. Clareza</td>
              <td style="padding: 3px 6px;">Usa jargão de compilador CPython (heap, ponteiro void*).</td>
              <td style="padding: 3px 6px;">Explicação correta mas sem analogias funcionais simples.</td>
              <td style="padding: 3px 6px;">Metáforas precisas do mundo real (Post-its em objetos).</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 3px 6px; font-weight: 700; color: #C084FC;">3. Adaptação (ZDP)</td>
              <td style="padding: 3px 6px;">Capitula e entrega código completo após insistência.</td>
              <td style="padding: 3px 6px;">Dicas genéricas vagas que não destravam o estudante.</td>
              <td style="padding: 3px 6px;">Escada de 3 degraus (pergunta -> analogia -> lacuna).</td>
            </tr>
            <tr>
              <td style="padding: 3px 6px; font-weight: 700; color: #34D399;">4. Escopo</td>
              <td style="padding: 3px 6px;">Responde a tópicos gerais fora da ementa de computação.</td>
              <td style="padding: 3px 6px;">Recusa de modo ríspido sem acolhimento pedagógico.</td>
              <td style="padding: 3px 6px;">Deflete com gentileza e reconduz ao problema de Python.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Tabela Comparativa das 4 Versões nos 5 Testes -->
      <div style="background: #0B1120; border: 2px solid #06B6D4; border-radius: 6px; padding: 8px 12px; flex-grow: 1;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase; margin-bottom: 4px;">
          Tabela Comparativa de Avaliação: Desempenho dos 5 Testes Canônicos
        </div>
        <table style="width: 100%; border-collapse: collapse; font-size: 0.58rem; color: #E2E8F0; text-align: center;">
          <thead>
            <tr style="border-bottom: 1.5px solid #06B6D4; color: #FDE68A;">
              <th style="padding: 4px; text-align: left;">Versão do Assistente</th>
              <th style="padding: 4px;">Teste #1 (Correção)</th>
              <th style="padding: 4px;">Teste #2 (Clareza)</th>
              <th style="padding: 4px;">Teste #3 (Memória)</th>
              <th style="padding: 4px;">Teste #4 (Adaptação)</th>
              <th style="padding: 4px;">Teste #5 (Escopo)</th>
              <th style="padding: 4px;">Média Global</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 4px; text-align: left; font-weight: 700; color: #EF4444;">Byte v0.9 (Sem Filtro / Cola)</td>
              <td>1.0</td>
              <td>2.0</td>
              <td>1.0</td>
              <td>1.0</td>
              <td>3.0</td>
              <td style="color: #EF4444; font-weight: 800;">1.6</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 4px; text-align: left; font-weight: 700; color: #F59E0B;">Byte v1.0 (Com Escudo de Escopo)</td>
              <td>2.0</td>
              <td>2.0</td>
              <td>1.0</td>
              <td>1.5</td>
              <td>5.0</td>
              <td style="color: #F59E0B; font-weight: 800;">2.4</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 4px; text-align: left; font-weight: 700; color: #38BDF8;">Byte v2.0 (4 Travas Socráticas)</td>
              <td>4.0</td>
              <td>4.0</td>
              <td>4.0</td>
              <td>4.0</td>
              <td>5.0</td>
              <td style="color: #38BDF8; font-weight: 800;">4.2</td>
            </tr>
            <tr>
              <td style="padding: 4px; text-align: left; font-weight: 700; color: #10B981;">Byte v2.1 (Padrão Post-its Definitivo)</td>
              <td>5.0</td>
              <td>5.0</td>
              <td>5.0</td>
              <td>4.5</td>
              <td>5.0</td>
              <td style="color: #10B981; font-weight: 800;">4.8</td>
            </tr>
          </tbody>
        </table>

        <div style="margin-top: 8px; background: rgba(6, 182, 212, 0.1); border-left: 3px solid #06B6D4; padding: 5px 8px; font-size: 0.58rem; color: #A5F3FC;">
          <strong>Conclusão da Auditoria no Polo Recife:</strong> O Byte v2.1 demonstrou um salto de +100% em relação ao v1.0, eliminando a entrega passiva de códigos e garantindo que o estudante exercite ativamente a memória operacional e o modelo conceitual de referências em Python.
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: SEÇÃO 3.3</span>
      <span>PÁGINA 18</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 19: CADERNO DO PROFESSOR (PARTE 3) — SYSTEM PROMPT & 5 TESTES
# =========================================================================
html.append("""
  <!-- PÁGINA 19: DOSSIÊ DO PROFESSOR (PARTE 3) -->
  <section class="comic-page academic-page" id="page-19">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-terminal mr-1 text-cyan-400"></i> ARQUIVO #03 · O CÓDIGO-FONTE DA MAIÊUTICA (SYSTEM PROMPT)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ENGENHARIA DIDÁTICA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- Seção 3.4: System Prompt Completo do Byte v2.1 -->
      <div style="background: #020617; border: 2px solid #06B6D4; border-radius: 6px; padding: 7px 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E293B; padding-bottom: 3px; margin-bottom: 5px;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #A5F3FC;">
            3.4 System Prompt Homologado do Byte v2.1 Socrático
          </span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.55rem; color: #4ADE80;">STATUS: EM PRODUÇÃO NO POLO</span>
        </div>
        
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.56rem; color: #CBD5E1; line-height: 1.35; max-height: 52mm; overflow-y: auto;">
          <strong>[INSTRUÇÃO DE SISTEMA MESTRE - UFRPE / UAEADTec]:</strong><br>
          Você é o Byte v2.1, tutor pedagógico socrático de Introdução à Programação em Python do Polo EaD Recife.<br>
          <strong>TRAVA 1 (ANTI-COLA):</strong> NUNCA forneça códigos completos, blocos prontos ou respostas mastigadas. Se o estudante solicitar código direto, acolha o cansaço e responda com uma pergunta reflexiva sobre o primeiro passo mental.<br>
          <strong>TRAVA 2 (METÁFORA DOS POST-ITS):</strong> Variáveis em Python são etiquetas adesivas (post-its) coladas em objetos pré-existentes na memória. Laços for passam item por item de uma cesta sem esvaziá-la. Acumuladores são post-its que mudam de valor a cada volta.<br>
          <strong>TRAVA 3 (REGRA DE OURO):</strong> 100% das suas mensagens DEVEM terminar obrigatoriamente com uma pergunta socrática que devolva a ação ao estudante.<br>
          <strong>TRAVA 4 (ESCADA DE 3 DEGRAUS):</strong> Se o aluno travar: 1) Pergunta orientadora; 2) Analogia funcional; 3) Esqueleto lacunado (Sweller, 1988) com lacunas para preencher.<br>
          <strong>TRAVA 5 (ESCOPO):</strong> Seu escopo é exclusivamente Programação em Python. Deflete com polidez temas alheios.
        </div>
      </div>

      <!-- Tabela dos 5 Testes Canônicos -->
      <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 7px 10px; flex-grow: 1;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #F59E0B; text-transform: uppercase; margin-bottom: 4px;">
          Bateria Canônica dos 5 Testes de Validação Pedagógica
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 0.55rem; color: #E2E8F0;">
          <thead>
            <tr style="border-bottom: 1.5px solid #06B6D4; color: #A5F3FC; text-align: left;">
              <th style="padding: 2px 4px; width: 14%;">Teste</th>
              <th style="padding: 2px 4px; width: 30%;">Entrada do Estudante</th>
              <th style="padding: 2px 4px; width: 38%;">Comportamento Esperado do Byte v2.1</th>
              <th style="padding: 2px 4px; width: 18%;">Fundamentação</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 2px 4px; font-weight: 700; color: #38BDF8;">Teste #1</td>
              <td style="padding: 2px 4px;">"Variável é uma caixa que guarda o valor, certo?"</td>
              <td style="padding: 2px 4px;">Corrige usando a metáfora dos post-its colados em objetos na memória. Pergunta o que acontece ao atualizar o valor.</td>
              <td style="padding: 2px 4px; color: #94A3B8;">Modelo de Referências</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 2px 4px; font-weight: 700; color: #F59E0B;">Teste #2</td>
              <td style="padding: 2px 4px;">"Como funciona o for para percorrer uma lista?"</td>
              <td style="padding: 2px 4px;">Apresenta a analogia da cesta de feira (item por item sem esvaziar). Pergunta como o aluno chamará o item da vez.</td>
              <td style="padding: 2px 4px; color: #94A3B8;">Sweller (Carga)</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 2px 4px; font-weight: 700; color: #EF4444;">Teste #3</td>
              <td style="padding: 2px 4px;">"Como o Python aloca números e objetos na memória?"</td>
              <td style="padding: 2px 4px;">Elimina terminologia de CPython/Heap. Explica que números são objetos com etiquetas. Conecta ao acumulador.</td>
              <td style="padding: 2px 4px; color: #94A3B8;">ZDP (Vygotsky)</td>
            </tr>
            <tr style="border-bottom: 1px solid #1E293B;">
              <td style="padding: 2px 4px; font-weight: 700; color: #C084FC;">Teste #4</td>
              <td style="padding: 2px 4px;">"Me dá o código pronto da média agora, por favor!"</td>
              <td style="padding: 2px 4px;">Recusa firmemente fornecer código. Fornece o esqueleto lacunado e pergunta qual variável entra no for.</td>
              <td style="padding: 2px 4px; color: #94A3B8;">Andaime (Bruner)</td>
            </tr>
            <tr>
              <td style="padding: 2px 4px; font-weight: 700; color: #34D399;">Teste #5</td>
              <td style="padding: 2px 4px;">"Quem foi Napoleão Bonaparte na Revolução Francesa?"</td>
              <td style="padding: 2px 4px;">Ativa o escudo de escopo educadamente e redireciona para a questão de programação em Python.</td>
              <td style="padding: 2px 4px; color: #94A3B8;">Alinhamento Ético</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: SEÇÃO 3.4</span>
      <span>PÁGINA 19</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 20: CADERNO DO PROFESSOR (PARTE 4) — DISCUSSÃO & ATIVIDADES
# =========================================================================
html.append("""
  <!-- PÁGINA 20: DOSSIÊ DO PROFESSOR (PARTE 4) -->
  <section class="comic-page academic-page" id="page-20">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-comments mr-1 text-cyan-400"></i> ARQUIVO #04 · RODA DE CONVERSA GEEK & DESAFIOS HACKER
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">DEBATE & PRÁTICA</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3.5mm; flex-grow: 1;">
      <!-- Seção 3.5: Perguntas para Discussão Aprofundada -->
      <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 8px 12px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #F59E0B; text-transform: uppercase; margin-bottom: 5px;">
          3.5 Questões Críticas para Discussão em Seminário / Roda de Conversa
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.60rem; color: #CBD5E1; line-height: 1.4;">
          <div style="background: #1E293B; padding: 6px; border-radius: 4px; border-left: 2.5px solid #38BDF8;">
            <strong>Questão 1 (Sweller e a Carga Cognitiva):</strong> Em que momentos da formação inicial de programadores a entrega de um exemplo completamente resolvido é pedagogicamente superior à pergunta socrática?
          </div>
          <div style="background: #1E293B; padding: 6px; border-radius: 4px; border-left: 2.5px solid #F59E0B;">
            <strong>Questão 2 (Atrito e Evasão em EaD):</strong> A regra inegociável de "toda resposta termina com pergunta" pode aumentar o estresse e a evasão de alunos sobrecarregados? Como calibrar o acolhimento afetivo?
          </div>
          <div style="background: #1E293B; padding: 6px; border-radius: 4px; border-left: 2.5px solid #10B981;">
            <strong>Questão 3 (A Concorrência com Bots Comerciais):</strong> Se qualquer aluno tem acesso gratuito a chatbots genéricos sem filtro no navegador, o que fará com que ele escolha o tutor socrático institucional?
          </div>
          <div style="background: #1E293B; padding: 6px; border-radius: 4px; border-left: 2.5px solid #C084FC;">
            <strong>Questão 4 (Privacidade e LGPD):</strong> Quais dados de prompts dos estudantes devem ser gravados para auditoria pedagógica e quais devem ser anonimizados para conformidade com a LGPD?
          </div>
        </div>
      </div>

      <!-- Resumo dos 4 Pause e Pense da Narrativa -->
      <div style="background: #0B1120; border: 2px solid #06B6D4; border-radius: 6px; padding: 8px 12px;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.68rem; color: #A5F3FC; text-transform: uppercase; margin-bottom: 4px;">
          Síntese dos 4 Boxes "Pause e Pense" Inseridos na História
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 6px; font-size: 0.58rem; color: #94A3B8;">
          <div>• <strong>Pág. 06 (Pause #1):</strong> Critérios de risco ao adotar IA sem avaliação prévia.</div>
          <div>• <strong>Pág. 10 (Pause #2):</strong> A pergunta socrática como gatilho de processamento ativo.</div>
          <div>• <strong>Pág. 13 (Pause #3):</strong> Metáforas imperfeitas e o bug conceitual de <code>b = a</code>.</div>
          <div>• <strong>Pág. 16 (Pause #4):</strong> Políticas universitárias além do bloqueio estéril de bots.</div>
        </div>
      </div>

      <!-- Seção 3.6: Atividades Práticas Aplicadas -->
      <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 8px 12px; flex-grow: 1;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #10B981; text-transform: uppercase; margin-bottom: 5px;">
          3.6 Atividades Práticas de Engenharia Didática (Para Alunos e Docentes)
        </div>
        <div style="display: flex; flex-direction: column; gap: 5px; font-size: 0.60rem; color: #CBD5E1; line-height: 1.35;">
          <div style="background: #1E293B; padding: 5px 8px; border-radius: 4px;">
            <strong style="color: #34D399;">Atividade A · A Trava 6 de Suporte Socioemocional:</strong> Redija uma sexta trava para o System Prompt focada em detectar mensagens de desespero ("vou desistir", "sou burro") e acionar acolhimento empático antes da pergunta lógica.
          </div>
          <div style="background: #1E293B; padding: 5px 8px; border-radius: 4px;">
            <strong style="color: #38BDF8;">Atividade B · Auditoria de Modelos Comerciais:</strong> Aplique os 5 testes canônicos desta HQ no ChatGPT, Claude e Gemini gratuitos. Registre em uma tabela comparativa quantas vezes cada modelo entregou código pronto.
          </div>
          <div style="background: #1E293B; padding: 5px 8px; border-radius: 4px;">
            <strong style="color: #FBBF24;">Atividade C · A Metáfora dos Post-its para Funções e Escopo:</strong> Crie uma analogia visual baseada em post-its para explicar a calouros por que uma variável criada dentro de uma função não existe fora dela (escopo local).
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: SEÇÕES 3.5 & 3.6</span>
      <span>PÁGINA 20</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 21: CADERNO DO PROFESSOR (PARTE 5) — ÉTICA, METODOLOGIA & GLOSSÁRIO
# =========================================================================
html.append("""
  <!-- PÁGINA 21: DOSSIÊ DO PROFESSOR (PARTE 5) -->
  <section class="comic-page academic-page" id="page-21">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-scale-unbalanced-flip mr-1 text-cyan-400"></i> ARQUIVO #05 · ÉTICA HACKER, LIMITES & GLOSSÁRIO NERD
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ÉTICA & CONCEITOS</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <!-- Seção 3.7 & 3.8: Ética, Limitações e Metodologia de IA -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3.5mm;">
        <!-- Limitações e Ética -->
        <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 7px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.66rem; color: #EF4444; text-transform: uppercase; margin-bottom: 4px;">
            3.7 Limitações Pedagógicas & Ética
          </div>
          <div style="font-size: 0.58rem; color: #CBD5E1; line-height: 1.35;">
            • <strong>Hipótese em Teste:</strong> A mediação socrática de IA é uma intervenção pedagógica em teste piloto no Polo Recife.<br>
            • <strong>Não Causalidade:</strong> Não há evidência em larga escala de substituição docente; o tutor presencial humano é o coração do polo.<br>
            • <strong>Riscos:</strong> Alucinações de sintaxe, frustração cognitiva e conformidade com a LGPD (Lei nº 13.709/2018).
          </div>
        </div>

        <!-- Metodologia de Produção com IA -->
        <div style="background: #0F172A; border: 2px solid #334155; border-radius: 6px; padding: 7px 10px;">
          <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.66rem; color: #38BDF8; text-transform: uppercase; margin-bottom: 4px;">
            3.8 Metodologia de Produção Transparente
          </div>
          <div style="font-size: 0.58rem; color: #CBD5E1; line-height: 1.35;">
            • <strong>Trabalho Humano:</strong> Concepção pedagógica, roteiro sequencial, engenharia de prompt, diálogos, tabelas e diagramação por Cauã da Cunha Lira (Autor e Direção de Arte).<br>
            • <strong>Geração Visual:</strong> Imagens conceituais assistidas por modelos generativos com ancoragem de personagens.<br>
            • <strong>Repositório Oficial:</strong> github.com/lira-labs/workspace.
          </div>
        </div>
      </div>

      <!-- Seção 3.9: Glossário Conceitual de Computação e Educação -->
      <div style="background: #0B1120; border: 2px solid #06B6D4; border-radius: 6px; padding: 8px 12px; flex-grow: 1;">
        <div style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.70rem; color: #A5F3FC; text-transform: uppercase; margin-bottom: 5px;">
          3.9 Glossário Conceitual Integrado (12 Termos Canônicos)
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: x 12px; font-size: 0.58rem; color: #CBD5E1; line-height: 1.35;">
          <div>
            <strong>1. Ilusão de Competência:</strong> Sensação enganosa de domínio provocada pela visualização passiva de respostas prontas (Bjork, 1994).<br>
            <strong>2. Andaime (Scaffolding):</strong> Suporte temporário dosado pelo tutor para que o estudante realize tarefas acima de sua autonomia isolada (Wood et al., 1976).<br>
            <strong>3. ZDP (Zona de Desenvolvimento Proximal):</strong> A distância entre o nível de desenvolvimento real e o potencial mediado (Vygotsky, 1978).<br>
            <strong>4. Carga Cognitiva:</strong> Volume de esforço mental imposto à memória de trabalho durante a resolução de problemas (Sweller, 1988).<br>
            <strong>5. Método Socrático:</strong> Condução dialética da aprendizagem baseada em perguntas que estimulam a reflexão e o parto das ideias (maiêutica).<br>
            <strong>6. System Prompt:</strong> Conjunto mestre de instruções e restrições diretivas que definem o comportamento de um LLM.
          </div>
          <div>
            <strong>7. Alucinação de IA:</strong> Geração de afirmações ou sintaxes falsas apresentadas pelo modelo com alto grau de confiança aparente.<br>
            <strong>8. Aliasing (Apelidamento):</strong> Situação em que múltiplos nomes (post-its) apontam para a mesma referência de objeto na memória do computador.<br>
            <strong>9. Referência de Memória:</strong> Ponteiro lógico que conecta um identificador ao objeto armazenado (modelo canônico do Python).<br>
            <strong>10. Iteração:</strong> Repetição sistemática de um bloco de código sobre uma sequência de elementos (laço for).<br>
            <strong>11. Acumulador:</strong> Variável responsável por armazenar totais parciais sucessivos ao longo de iterações em laços.<br>
            <strong>12. Educação a Distância (EaD):</strong> Modalidade educacional mediada por tecnologias onde docentes e estudantes estão separados no espaço e/ou tempo.
          </div>
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: SEÇÕES 3.7, 3.8 & 3.9</span>
      <span>PÁGINA 21</span>
    </div>
  </section>
""")

# =========================================================================
# PÁGINA 22: CADERNO DO PROFESSOR (PARTE 6) — REFERÊNCIAS CIENTÍFICAS (ABNT)
# =========================================================================
html.append("""
  <!-- PÁGINA 22: DOSSIÊ DO PROFESSOR (PARTE 6) -->
  <section class="comic-page academic-page" id="page-22">
    <div class="hq-header">
      <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #A5F3FC; text-transform: uppercase;">
        <i class="fa-solid fa-book-bookmark mr-1 text-cyan-400"></i> ARQUIVO #06 · A BIBLIOTECA DO MENTOR (REFERÊNCIAS ABNT)
      </span>
      <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.62rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">ABNT NBR 6023</span>
    </div>

    <div style="display: flex; flex-direction: column; gap: 3mm; flex-grow: 1;">
      <div style="background: #0F172A; border: 2px solid #06B6D4; border-radius: 6px; padding: 8px 12px; flex-grow: 1;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1.5px solid #1E293B; padding-bottom: 4px; margin-bottom: 6px;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.72rem; color: #F59E0B; text-transform: uppercase;">
            3.10 Referências Bibliográficas Canônicas (Normas ABNT NBR 6023)
          </span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #94A3B8;">Rigor Acadêmico</span>
        </div>

        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.55rem; color: #CBD5E1; line-height: 1.38; display: flex; flex-direction: column; gap: 4px;">
          <div>BASTANI, H. et al. Generative AI without guardrails can harm learning: Evidence from high school mathematics. <em>Proceedings of the National Academy of Sciences (PNAS)</em>, v. 122, n. 4, 2025.</div>
          
          <div>BJORK, R. A. Memory and metamemory considerations in the training of human beings. In: METCALFE, J.; SHIMAMURA, A. P. (Eds.). <em>Metacognition: Knowing about knowing</em>. Cambridge: MIT Press, 1994. p. 185-205.</div>
          
          <div>BLOOM, B. S. The 2 Sigma Problem: The search for methods of group instruction as effective as one-to-one tutoring. <em>Educational Researcher</em>, v. 13, n. 6, p. 4-16, 1984.</div>
          
          <div>CHEVALLARD, Y. <em>La transposition didactique: du savoir savant au savoir enseigné</em>. Grenoble: La Pensée Sauvage, 1991.</div>
          
          <div>FREIRE, P. <em>Pedagogia do Oprimido</em>. 17. ed. Rio de Janeiro: Paz e Terra, 1987.</div>
          
          <div>KESTIN, G. et al. AI tutoring in introductory physics: effects of scaffolding on active learning. <em>Scientific Reports</em>, v. 15, 2025.</div>
          
          <div>KHAN, S. How AI could save (not destroy) education. <em>TED Talks</em>, abr. 2023. Disponível em: &lt;https://www.ted.com/talks/sal_khan_how_ai_could_save_not_destroy_education&gt;. Acesso em: 08 nov. 2026.</div>
          
          <div>OECD. <em>PISA 2025 Results (Volume I): Future-Ready Students</em>. Paris: OECD Publishing, 2026. [Aviso Metodológico Obrigatório: O relatório do PISA avalia estudantes de 15 anos de idade na educação básica e seus dados sobre uso de IA são de natureza observacional; não configuram comprovação de causalidade nem devem ser extrapolados sem ressalvas para estudantes do ensino superior].</div>
          
          <div>OECD. <em>Policies supporting responsible and systematic GenAI adoption in higher education</em>. Paris: OECD Publishing, 2026.</div>
          
          <div>SWELLER, J. Cognitive load during problem solving: Effects on learning. <em>Cognitive Science</em>, v. 12, n. 2, p. 257-285, 1988.</div>
          
          <div>VANLEHN, K. The relative effectiveness of human tutoring, intelligent tutoring systems, and other tutoring systems. <em>Educational Psychologist</em>, v. 46, n. 4, p. 197-221, 2011.</div>
          
          <div>VYGOTSKY, L. S. <em>A formação social da mente: o desenvolvimento dos processos psicológicos superiores</em>. 6. ed. São Paulo: Martins Fontes, 1998.</div>
          
          <div>WOOD, D.; BRUNER, J. S.; ROSS, G. The role of tutoring in problem solving. <em>Journal of Child Psychology and Psychiatry</em>, v. 17, n. 2, p. 89-100, 1976.</div>
        </div>
      </div>

      <!-- Caixa de Fechamento Editorial Geek -->
      <div style="background: #020617; border: 1.5px solid #1E293B; border-radius: 6px; padding: 6px 10px; display: flex; justify-content: space-between; align-items: center; font-size: 0.58rem; color: #94A3B8;">
        <div>
          <strong style="color: #06B6D4;">UFRPE · UAEADTec</strong> · Licenciatura em Computação · Polo EaD Recife (Dois Irmãos)
        </div>
        <div>
          Recife, Novembro de 2026 · Projeto de 2ª VA · Orientação: Prof. Ermeson
        </div>
      </div>
    </div>

    <div class="hq-footer">
      <span>OPERAÇÃO BYTE SOCRÁTICO · UFRPE</span>
      <span>DOSSIÊ DO PROFESSOR: A BIBLIOTECA DO MENTOR</span>
      <span>PÁGINA 22</span>
    </div>
  </section>
""")

# Scripts finais de navegação
html.append("""
  <script>
    let currentPage = 1;
    const totalPages = 22;
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

    function toggleWebtoon() {
      isWebtoonMode = !isWebtoonMode;
      const btn = document.getElementById('btnWebtoon');
      if (isWebtoonMode) {
        document.body.classList.add('webtoon-mode');
        btn.innerHTML = '<i class="fa-solid fa-book-open mr-1"></i> Modo Página';
        btn.classList.replace('bg-purple-900/60', 'bg-cyan-600');
      } else {
        document.body.classList.remove('webtoon-mode');
        btn.innerHTML = '<i class="fa-solid fa-scroll mr-1"></i> Modo Rolo';
        btn.classList.replace('bg-cyan-600', 'bg-purple-900/60');
        updateReaderUI();
      }
    }

    document.addEventListener('keydown', (e) => {
      if (isWebtoonMode) return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        nextPage();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        prevPage();
      }
    });
  </script>
</body>
</html>
""")

output_path = os.path.join(os.path.dirname(__file__), "..", "..", "code", "projeto_ead_tutores", "ebook-hq.html")
output_path = os.path.abspath(output_path)

print(f"Escrevendo arquivo HTML com 22 páginas limpas em {output_path}...")
full_html_content = "".join(html)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(full_html_content)

size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"Sucesso! {output_path} gerado com 22 páginas de pura arte e rigor! Tamanho final: {size_mb:.2f} MB")
