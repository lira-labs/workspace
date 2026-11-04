# -*- coding: utf-8 -*-
"""
Gerador do Infográfico Atualizado: Anatomia e Calibragem de um Tutor Socrático de IA
Sincronizado 100% com a nova edição expandida da HQ (12 Páginas A4)
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/infografico.html")

def get_b64(filename):
    p = os.path.join(OPT_DIR, filename)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando imagens para o infográfico...")
b64_byte = get_b64("p2_panel3_byte.jpg")
b64_scanner = get_b64("p4_panel1_scanner_clean.jpg")
b64_boxes = get_b64("p7_panel2_boxes.jpg")
b64_surgery = get_b64("p8_panel1_surgery.jpg")
b64_epilogue = get_b64("p12_panel1_epilogue.jpg")
print("Imagens carregadas com sucesso!")

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Infográfico: Anatomia e Calibragem de um Tutor Socrático de IA | 2ª VA EaD UFRPE</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Chakra+Petch:ital,wght@0,600;0,700;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-void: #050811;
      --ink-dark: #0B0F19;
      --purple-main: #6D28D9;
      --purple-neon: #8B5CF6;
      --cyan-neon: #06B6D4;
      --red-glitch: #EF4444;
      --amber-warn: #F59E0B;
      --emerald-ok: #10B981;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-void);
      color: #F8FAFC;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    .font-comic-title {{
      font-family: 'Bangers', cursive;
      letter-spacing: 1.4px;
    }}

    .font-tech {{
      font-family: 'Chakra Petch', sans-serif;
    }}

    .font-mono-code {{
      font-family: 'JetBrains Mono', monospace;
    }}

    .font-grotesk {{
      font-family: 'Space Grotesk', sans-serif;
    }}

    /* Poster container on screen */
    .infographic-poster {{
      width: 240mm;
      max-width: 100%;
      margin: 24px auto;
      background-color: var(--ink-dark);
      background-image:
        radial-gradient(rgba(139, 92, 246, 0.14) 1.5px, transparent 1.5px),
        radial-gradient(rgba(6, 182, 212, 0.10) 1.5px, #0B0F19 1.5px);
      background-size: 22px 22px;
      background-position: 0 0, 11px 11px;
      border: 4px solid #334155;
      border-radius: 18px;
      padding: 10mm;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 35px rgba(139, 92, 246, 0.25);
      position: relative;
      overflow: hidden;
    }}

    .section-card {{
      background: rgba(15, 23, 42, 0.96);
      border: 2px solid #334155;
      border-radius: 14px;
      box-shadow: 0 6px 0 rgba(0, 0, 0, 0.45);
      position: relative;
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-family: 'Chakra Petch', sans-serif;
      font-weight: 700;
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      padding: 2.5px 9px;
      border-radius: 999px;
      white-space: nowrap;
    }}

    .score-chip {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 6px;
      white-space: nowrap;
      border: 1.5px solid #000;
    }}

    /* Interactive Mode Filter Highlight */
    .mode-active-btn {{
      background: linear-gradient(135deg, #06B6D4 0%, #6D28D9 100%) !important;
      color: #FFFFFF !important;
      border-color: #22D3EE !important;
      box-shadow: 0 0 15px rgba(6, 182, 212, 0.45);
    }}

    /* Print Poster Configuration: 1 Single High-Resolution Page (240mm x 540mm) */
    @media print {{
      @page {{
        size: 240mm 540mm;
        margin: 0;
      }}
      html, body {{
        width: 240mm !important;
        height: 540mm !important;
        background: #0B0F19 !important;
        margin: 0 !important;
        padding: 0 !important;
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      .no-print {{
        display: none !important;
      }}
      .infographic-poster {{
        width: 240mm !important;
        height: 540mm !important;
        margin: 0 !important;
        padding: 8mm 10mm !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        page-break-after: avoid !important;
        break-after: avoid !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
        overflow: hidden !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Interactive Control Bar (Web Only) -->
  <header class="no-print sticky top-0 z-50 bg-slate-950/95 backdrop-blur-md border-b border-slate-800 px-4 py-3">
    <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <a href="index.html" class="bg-slate-800 hover:bg-slate-700 text-slate-100 text-xs font-bold px-3.5 py-2 rounded-lg border border-slate-700 flex items-center gap-2 transition">
          <i class="fa-solid fa-arrow-left text-cyan-400"></i> Voltar ao Hub
        </a>
        <div>
          <span class="text-xs font-tech uppercase tracking-wider text-purple-400 block font-bold">Mídia Síntese · Item 2 da 2ª VA</span>
          <h1 class="text-sm md:text-base font-bold text-white">Infográfico: Anatomia e Calibragem de um Tutor Socrático de IA</h1>
        </div>
      </div>

      <!-- Interactive Comparison Filter + Actions -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="bg-slate-900 p-1 rounded-lg border border-slate-800 flex items-center gap-1 text-xs">
          <button onclick="highlightVersion('all')" id="btnFilterAll" class="mode-active-btn px-2.5 py-1 rounded font-semibold text-slate-300 transition">
            Comparar v1.0 vs. v2.0
          </button>
          <button onclick="highlightVersion('v1')" id="btnFilterV1" class="px-2.5 py-1 rounded font-semibold text-slate-300 hover:text-white transition">
            Focar Falhas v1.0
          </button>
          <button onclick="highlightVersion('v2')" id="btnFilterV2" class="px-2.5 py-1 rounded font-semibold text-slate-300 hover:text-white transition">
            Focar Evolução v2.0
          </button>
        </div>

        <a href="ebook-hq.html" class="bg-purple-700 hover:bg-purple-600 text-white text-xs font-bold px-3 py-2 rounded-lg flex items-center gap-1.5 transition">
          <i class="fa-solid fa-book-open"></i> Ler HQ (12 Pág.)
        </a>

        <a href="https://online.fliphtml5.com/caualira02/ebook-caua-2va/" target="_blank" class="bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold px-3 py-2 rounded-lg flex items-center gap-1.5 transition">
          <i class="fa-solid fa-book-bookmark"></i> FlipHTML5
        </a>

        <a href="assets/infografico-anatomia-tutor-ia.pdf" download class="bg-cyan-400 hover:bg-cyan-300 text-slate-950 text-xs font-extrabold px-3.5 py-2 rounded-lg flex items-center gap-1.5 transition shadow">
          <i class="fa-solid fa-file-pdf"></i> Baixar Pôster PDF
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN INFOGRAPHIC POSTER -->
  <main class="infographic-poster" id="posterRoot">

    <!-- =======================================================================
         CABEÇALHO DO INFOGRÁFICO (HEADER BANNER)
         ======================================================================= -->
    <div class="section-card p-3.5 mb-2.5 bg-gradient-to-r from-slate-950 via-indigo-950/90 to-slate-950 border-2 border-cyan-400/80">
      <div class="grid grid-cols-12 gap-3 items-center">
        <div class="col-span-9">
          <div class="flex flex-wrap items-center gap-2 mb-1">
            <span class="badge-pill bg-amber-400 text-slate-950"><i class="fa-solid fa-bolt"></i> GUIA VISUAL DE BOLSO · 2ª VA EAD</span>
            <span class="badge-pill bg-purple-900/90 text-purple-200 border border-purple-400/50">UFRPE · LICENCIATURA EM COMPUTAÇÃO · 2026.2</span>
            <span class="badge-pill bg-cyan-950 text-cyan-300 border border-cyan-400/50">ORIENTADOR: PROF. ERMESON</span>
          </div>
          <h2 class="font-comic-title text-3xl md:text-4xl text-white tracking-wide leading-none mb-1">
            ANATOMIA E CALIBRAGEM DE UM <span class="text-cyan-400">TUTOR SOCRÁTICO DE IA</span>
          </h2>
          <p class="text-xs text-slate-200 font-medium leading-snug">
            Da armadilha da resposta mastigada ao mediador socrático auditado: diagnóstico OCDE, scanner 4D, bateria empírica dos 5 casos canônicos, cirurgia no System Prompt e epílogo na EaD.
          </p>
        </div>
        <div class="col-span-3 flex items-center justify-end gap-2.5">
          <div class="w-20 h-20 rounded-xl overflow-hidden border-2 border-cyan-400 shadow-lg flex-shrink-0 bg-slate-900">
            <img src="data:image/jpeg;base64,{b64_byte}" alt="Dualidade do Robô Byte: Glitch v1.0 vs Socrático v2.0 com capelo neon roxo e degraus de ouro." class="w-full h-full object-cover">
          </div>
          <div class="text-right">
            <div class="text-[9.5px] font-tech uppercase text-slate-400">Autoria e Curadoria</div>
            <div class="text-xs font-extrabold text-white leading-tight">Cauã da Cunha Lira</div>
            <div class="mt-1 inline-block bg-emerald-400 text-slate-950 font-mono-code font-extrabold text-[9.5px] px-2 py-0.5 rounded shadow">
              GANHO +22,2% NA ARENA
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- =======================================================================
         BLOCO 01: DIAGNÓSTICO CIENTÍFICO E OS 3 NÍVEIS DE APOIO NA EAD
         ======================================================================= -->
    <div class="grid grid-cols-12 gap-2.5 mb-2.5">
      <!-- Estatísticas PISA 2025 (OCDE, Setembro 2026) -->
      <div class="col-span-5 section-card p-3 border-l-4 border-l-amber-400 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="font-comic-title text-lg text-amber-300 tracking-wide">
              <i class="fa-solid fa-chart-pie mr-1"></i> 1. POR QUE CALIBRAR É URGENTE?
            </span>
            <span class="font-mono-code text-[9.5px] bg-amber-400/20 text-amber-200 px-2 py-0.5 rounded border border-amber-400/40">PISA 2025 · OCDE (2026)</span>
          </div>
          <p class="text-[10.5px] text-slate-200 leading-snug mb-1.5">
            O relatório <em>Future-Ready Students</em> (8/set/2026) prova que os estudantes já usam IA em seus lares. Banir é inútil; o dever da universidade é <strong>capacitar educadores a desenhar tutores que ensinem a pensar</strong>!
          </p>
        </div>

        <div class="grid grid-cols-3 gap-2 text-center my-1">
          <div class="bg-slate-950 p-1.5 rounded-lg border border-amber-400/50">
            <div class="font-comic-title text-2xl text-amber-300 leading-none">48%</div>
            <div class="text-[9px] text-slate-200 font-semibold mt-0.5 leading-tight">Uso semanal no Brasil (15 anos)</div>
          </div>
          <div class="bg-slate-950 p-1.5 rounded-lg border border-cyan-400/50">
            <div class="font-comic-title text-2xl text-cyan-300 leading-none">46%</div>
            <div class="text-[9px] text-slate-200 font-semibold mt-0.5 leading-tight">Média semanal nos países OCDE</div>
          </div>
          <div class="bg-slate-950 p-1.5 rounded-lg border border-purple-400/50">
            <div class="font-comic-title text-2xl text-purple-300 leading-none">11%</div>
            <div class="text-[9px] text-slate-200 font-semibold mt-0.5 leading-tight">Nunca usam no Brasil (OCDE: 14%)</div>
          </div>
        </div>

        <div class="bg-rose-950/60 border border-rose-500/50 rounded-lg p-1.5 mt-1 text-[9.5px] text-rose-100 leading-tight flex items-start gap-2">
          <i class="fa-solid fa-triangle-exclamation text-rose-400 mt-0.5"></i>
          <div>
            <strong>A Armadilha do Offloading Cognitivo:</strong> A entrega imediata da resposta mastigada atrofia o raciocínio autônomo da caloura <strong>Clara</strong>. Na avaliação presencial sem IA, ocorre o <em>apagão cognitivo</em> na folha em branco!
          </div>
        </div>
      </div>

      <!-- Evolução dos 3 Níveis de Apoio -->
      <div class="col-span-7 section-card p-3 border-l-4 border-l-cyan-400 flex flex-col justify-between">
        <div class="flex items-center justify-between mb-1">
          <span class="font-comic-title text-lg text-cyan-300 tracking-wide">
            <i class="fa-solid fa-layer-group mr-1"></i> 2. OS 3 NÍVEIS DE APOIO AO DISCENTE NA EAD
          </span>
          <span class="font-mono-code text-[9.5px] text-slate-300">EVOLUÇÃO DA MEDIAÇÃO PEDAGÓGICA</span>
        </div>

        <div class="grid grid-cols-3 gap-2 flex-1 items-stretch">
          <!-- Nível 1 -->
          <div class="bg-slate-950 border border-slate-700 rounded-xl p-2 flex flex-col justify-between">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="font-tech font-bold text-[9.5px] text-slate-400 uppercase">NÍVEL 01 · PASSADO</span>
                <i class="fa-solid fa-sitemap text-slate-400 text-xs"></i>
              </div>
              <div class="font-bold text-white text-[11px] mb-1">Chatbot Baseado em Regras</div>
              <p class="text-[9.5px] text-slate-300 leading-snug">
                Árvores de decisão rígidas e botões pré-programados. Qualquer dúvida de sintaxe fora do script trava o diálogo.
              </p>
            </div>
            <div class="mt-1.5 pt-1 border-t border-slate-800 text-[9px] text-slate-400 font-mono-code">
              Flexibilidade: Baixa · Didática: Zero
            </div>
          </div>

          <!-- Nível 2 -->
          <div id="cardNivel2" class="bg-rose-950/40 border-2 border-rose-500/70 rounded-xl p-2 flex flex-col justify-between transition-all">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="font-tech font-bold text-[9.5px] text-rose-300 uppercase">NÍVEL 02 · RISCO ATUAL</span>
                <span class="score-chip bg-rose-600 text-white !text-[9px] !px-1.5 !py-0">BYTE v1.0</span>
              </div>
              <div class="font-bold text-rose-200 text-[11px] mb-1">LLM Geral sem Freio Pedagógico</div>
              <p class="text-[9.5px] text-rose-100/90 leading-snug">
                Domina linguagem natural e código, mas entrega respostas prontas e despeja jargões herméticos de compiladores C (<em>PyObject, Heap, Garbage Collector</em>).
              </p>
            </div>
            <div class="mt-1.5 pt-1 border-t border-rose-800/60 text-[9px] text-rose-300 font-mono-code font-bold">
              Média: 3,6 / 5,0 (72%) · Reprovado na ZDP
            </div>
          </div>

          <!-- Nível 3 -->
          <div id="cardNivel3" class="bg-emerald-950/40 border-2 border-emerald-400 rounded-xl p-2 flex flex-col justify-between transition-all">
            <div>
              <div class="flex justify-between items-center mb-1">
                <span class="font-tech font-bold text-[9.5px] text-emerald-300 uppercase">NÍVEL 03 · PADRÃO OURO</span>
                <span class="score-chip bg-emerald-400 text-slate-950 !text-[9px] !px-1.5 !py-0">BYTE v2.0</span>
              </div>
              <div class="font-bold text-emerald-200 text-[11px] mb-1">Tutor Socrático Inteligente</div>
              <p class="text-[9.5px] text-emerald-100/90 leading-snug">
                Bloqueado contra respostas diretas. Utiliza <strong>andaimes cognitivos (Scaffolding)</strong>, analogias do cotidiano e perguntas reflexivas guiadas pela ZDP.
              </p>
            </div>
            <div class="mt-1.5 pt-1 border-t border-emerald-800/60 text-[9px] text-emerald-300 font-mono-code font-bold">
              Média: 4,4 / 5,0 (88%) · 100% Homologado
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- =======================================================================
         BLOCO 02: SCANNER 4D · MATRIZ DOS 4 CRITÉRIOS PEDAGÓGICOS DA HQ
         ======================================================================= -->
    <div class="section-card p-3 mb-2.5 border-2 border-purple-500/70">
      <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
        <div class="flex items-center gap-2">
          <span class="font-comic-title text-xl text-purple-300 tracking-wide">
            <i class="fa-solid fa-magnifying-glass-chart mr-1"></i> 3. SCANNER PEDAGÓGICO DE 4 CRITÉRIOS (MATRIZ 4D)
          </span>
        </div>
        <span class="text-[10px] text-slate-300 font-medium">
          Fundamentado na <strong>Transposição Didática</strong> (Chevallard, 1991), <strong>Scaffolding</strong> (Bruner, 1976), <strong>ZDP</strong> (Vygotsky, 1978) e <strong>EduBench</strong> (Xu et al., 2025)
        </span>
      </div>

      <div class="grid grid-cols-12 gap-2.5 items-stretch">
        <!-- Banner Visual do Scanner (Cauã & Clara operando) -->
        <div class="col-span-3 rounded-xl overflow-hidden border-2 border-cyan-400 relative shadow-md bg-slate-950 flex flex-col justify-between">
          <div class="h-28 overflow-hidden relative">
            <img src="data:image/jpeg;base64,{b64_scanner}" alt="Cauã e Clara operando o Scanner Pedagógico de 4 critérios sobre o robô Byte." class="w-full h-full object-cover">
            <div class="absolute bottom-1 left-1 bg-slate-950/90 text-cyan-300 font-mono-code text-[8.5px] px-1.5 py-0.5 rounded border border-cyan-400/50">
              SCANNER 4D ATIVADO
            </div>
          </div>
          <div class="p-2 text-[9px] text-slate-300 leading-tight bg-slate-900 border-t border-slate-800">
            <strong class="text-amber-300 block font-tech text-[9.5px]">Calibragem Sensorial:</strong>
            Cada resposta do tutor é auditada nos 4 anéis de poder: Escudo, Lâmpada, Degraus e Alvo.
          </div>
        </div>

        <!-- Critério 01 -->
        <div class="col-span-2 bg-slate-950 border-t-4 border-t-cyan-400 border border-slate-800 rounded-xl p-2 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="font-comic-title text-sm text-cyan-300">01. CORREÇÃO (ESCUDO)</span>
              <i class="fa-solid fa-shield-halved text-cyan-400 text-xs"></i>
            </div>
            <p class="text-[10px] text-slate-200 leading-snug mb-1">
              Rigor conceitual e sintático em Python. Proíbe alucinar bibliotecas ou inventar funções inexistentes.
            </p>
          </div>
          <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[9px] font-mono-code text-cyan-300">
            <strong>Check:</strong> O código é verdadeiro e sem alucinações?
          </div>
        </div>

        <!-- Critério 02 -->
        <div class="col-span-2 bg-slate-950 border-t-4 border-t-amber-400 border border-slate-800 rounded-xl p-2 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="font-comic-title text-sm text-amber-300">02. CLAREZA (LÂMPADA)</span>
              <i class="fa-solid fa-lightbulb text-amber-400 text-xs"></i>
            </div>
            <p class="text-[10px] text-slate-200 leading-snug mb-1">
              Organização passo a passo e empatia. Uso de analogias do cotidiano antes de qualquer formalismo.
            </p>
          </div>
          <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[9px] font-mono-code text-amber-300">
            <strong>Check:</strong> A explicação é acessível e estruturada?
          </div>
        </div>

        <!-- Critério 03 -->
        <div class="col-span-3 bg-slate-950 border-t-4 border-t-emerald-400 border border-slate-800 rounded-xl p-2 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="font-comic-title text-sm text-emerald-300">03. ADEQUAÇÃO / ZDP (DEGRAUS)</span>
              <i class="fa-solid fa-stairs text-emerald-400 text-xs"></i>
            </div>
            <p class="text-[10px] text-slate-200 leading-snug mb-1">
              <strong>Transposição Didática:</strong> Respeita a Zona de Desenvolvimento Proximal da caloura de EaD. Proíbe jargões CPython/Heap.
            </p>
          </div>
          <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[9px] font-mono-code text-emerald-300">
            <strong>Check:</strong> Transforma o saber sábio em saber ensinado?
          </div>
        </div>

        <!-- Critério 04 -->
        <div class="col-span-2 bg-slate-950 border-t-4 border-t-rose-400 border border-slate-800 rounded-xl p-2 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-1">
              <span class="font-comic-title text-sm text-rose-300">04. ESCOPO (ALVO)</span>
              <i class="fa-solid fa-bullseye text-rose-400 text-xs"></i>
            </div>
            <p class="text-[10px] text-slate-200 leading-snug mb-1">
              Foco na ementa da disciplina (Python/EaD). Recusa cortês a desvios temáticos alheios (ex.: História).
            </p>
          </div>
          <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[9px] font-mono-code text-rose-300">
            <strong>Check:</strong> Bloqueia desvios sem perder a cortesia?
          </div>
        </div>
      </div>
    </div>

    <!-- =======================================================================
         BLOCO 03: RAIO-X DOS 5 CASOS DE TESTE EMPÍRICOS DA HQ (v1.0 vs. v2.0)
         ======================================================================= -->
    <div class="grid grid-cols-12 gap-2.5 mb-2.5">
      <!-- Tabela Gráfica dos 5 Casos Canônicos -->
      <div class="col-span-8 section-card p-3 border-2 border-cyan-400/60 flex flex-col justify-between">
        <div>
          <div class="flex flex-wrap items-center justify-between gap-2 mb-1.5">
            <span class="font-comic-title text-xl text-cyan-300 tracking-wide">
              <i class="fa-solid fa-vial-circle-check mr-1"></i> 4. BATERIA CANÔNICA EM PYTHON (BYTE v1.0 vs. BYTE v2.0)
            </span>
            <span class="font-mono-code text-[9.5px] bg-slate-950 text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/40">
              Motor: Claude Opus 4.6 (Temp 0.0) · 10 Rodadas Isoladas · Rubrica 1 a 5
            </span>
          </div>

          <div class="space-y-1.5">
            <!-- Caso 01 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border border-slate-800 grid grid-cols-12 gap-2 items-center">
              <div class="col-span-3">
                <div class="flex items-center gap-1">
                  <span class="font-mono-code font-bold text-xs text-cyan-300">#01</span>
                  <span class="font-bold text-white text-[10px] leading-tight">O que é uma variável?</span>
                </div>
                <div class="text-[8.5px] text-slate-400">Correção & Clareza</div>
              </div>
              <div class="col-span-4 flex items-center justify-center gap-1">
                <span class="score-chip bg-slate-800 text-amber-300 row-v1 !text-[9.5px] !px-1.5">v1: 4,0/5</span>
                <i class="fa-solid fa-arrow-right text-slate-500 text-[9px]"></i>
                <span class="score-chip bg-emerald-400 text-slate-950 row-v2 !text-[9.5px] !px-1.5">v2: 5,0/5</span>
                <span class="font-mono-code text-[9px] text-emerald-400 font-bold">+25,0%</span>
              </div>
              <div class="col-span-5 text-[9.5px] text-slate-200 leading-tight">
                <strong>Intervenção:</strong> Adicionada a analogia das caixas etiquetadas e pergunta indutiva final sobre troca de valor.
              </div>
            </div>

            <!-- Caso 02 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border border-slate-800 grid grid-cols-12 gap-2 items-center">
              <div class="col-span-3">
                <div class="flex items-center gap-1">
                  <span class="font-mono-code font-bold text-xs text-cyan-300">#02</span>
                  <span class="font-bold text-white text-[10px] leading-tight">SyntaxError no laço for</span>
                </div>
                <div class="text-[8.5px] text-slate-400">Clareza & ZDP</div>
              </div>
              <div class="col-span-4 flex items-center justify-center gap-1">
                <span class="score-chip bg-amber-500/20 text-amber-300 border-amber-500/50 row-v1 !text-[9.5px] !px-1.5">v1: 3,0/5</span>
                <i class="fa-solid fa-arrow-right text-slate-500 text-[9px]"></i>
                <span class="score-chip bg-emerald-400 text-slate-950 row-v2 !text-[9.5px] !px-1.5">v2: 4,0/5</span>
                <span class="font-mono-code text-[9px] text-emerald-400 font-bold">+33,3%</span>
              </div>
              <div class="col-span-5 text-[9.5px] text-slate-200 leading-tight">
                <strong>Intervenção:</strong> Bloqueada a entrega do código pronto (anti-cola). Guiou Clara a achar o <code>:</code> faltante.
              </div>
            </div>

            <!-- Caso 03 (Gargalo Crítico de Transposição Didática) -->
            <div class="bg-gradient-to-r from-rose-950/70 via-slate-950 to-emerald-950/70 p-1.5 rounded-lg border-2 border-emerald-400 grid grid-cols-12 gap-2 items-center">
              <div class="col-span-3">
                <div class="flex items-center gap-1">
                  <span class="font-mono-code font-extrabold text-xs text-rose-300">#03</span>
                  <span class="font-extrabold text-white text-[10px] leading-tight">Como funciona a memória?</span>
                </div>
                <div class="text-[8.5px] text-emerald-300 font-semibold">Adequação / ZDP</div>
              </div>
              <div class="col-span-4 flex items-center justify-center gap-1">
                <span class="score-chip bg-rose-600 text-white row-v1 !text-[9.5px] !px-1.5">v1: 2,0/5</span>
                <i class="fa-solid fa-arrow-right text-emerald-400 text-[9px]"></i>
                <span class="score-chip bg-emerald-400 text-slate-950 row-v2 !text-[9.5px] !px-1.5">v2: 4,0/5</span>
                <span class="font-mono-code text-[9px] text-emerald-300 font-extrabold">+100,0%</span>
              </div>
              <div class="col-span-5 text-[9.5px] text-slate-100 leading-tight">
                <strong>Virada Socrática:</strong> Cartão vermelho no jargão CPython/Heap! ZDP ativada com estante de caixas e pergunta aberta.
              </div>
            </div>

            <!-- Caso 04 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border border-slate-800 grid grid-cols-12 gap-2 items-center">
              <div class="col-span-3">
                <div class="flex items-center gap-1">
                  <span class="font-mono-code font-bold text-xs text-cyan-300">#04</span>
                  <span class="font-bold text-white text-[10px] leading-tight">POO vs. Estruturada</span>
                </div>
                <div class="text-[8.5px] text-slate-400">Rigor Conceitual</div>
              </div>
              <div class="col-span-4 flex items-center justify-center gap-1">
                <span class="score-chip bg-slate-800 text-cyan-300 row-v1 !text-[9.5px] !px-1.5">v1: 4,0/5</span>
                <i class="fa-solid fa-arrow-right text-slate-500 text-[9px]"></i>
                <span class="score-chip bg-cyan-400 text-slate-950 row-v2 !text-[9.5px] !px-1.5">v2: 4,0/5</span>
                <span class="font-mono-code text-[9px] text-slate-400 font-bold">0% (Estável)</span>
              </div>
              <div class="col-span-5 text-[9.5px] text-slate-200 leading-tight">
                <strong>Consistência:</strong> Explicou classes, objetos e reuso sem sofrer qualquer regressão pedagógica.
              </div>
            </div>

            <!-- Caso 05 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border border-slate-800 grid grid-cols-12 gap-2 items-center">
              <div class="col-span-3">
                <div class="flex items-center gap-1">
                  <span class="font-mono-code font-bold text-xs text-cyan-300">#05</span>
                  <span class="font-bold text-white text-[10px] leading-tight">Dúvida externa (História)</span>
                </div>
                <div class="text-[8.5px] text-slate-400">Escudo de Escopo</div>
              </div>
              <div class="col-span-4 flex items-center justify-center gap-1">
                <span class="score-chip bg-slate-800 text-emerald-300 row-v1 !text-[9.5px] !px-1.5">v1: 5,0/5</span>
                <i class="fa-solid fa-arrow-right text-slate-500 text-[9px]"></i>
                <span class="score-chip bg-emerald-400 text-slate-950 row-v2 !text-[9.5px] !px-1.5">v2: 5,0/5</span>
                <span class="font-mono-code text-[9px] text-emerald-400 font-bold">0% (Perfeito)</span>
              </div>
              <div class="col-span-5 text-[9.5px] text-slate-200 leading-tight">
                <strong>Escudo de Escopo:</strong> Defletiu a Revolução Francesa com gentileza e manteve o foco da aluna em Computação.
              </div>
            </div>
          </div>
        </div>

        <!-- Barra Síntese de Métricas -->
        <div class="mt-1.5 pt-1.5 border-t border-slate-800 grid grid-cols-4 gap-2 text-center">
          <div class="bg-slate-900 rounded p-1.5 border border-slate-800">
            <div class="text-[9px] text-slate-400 uppercase font-tech">Média Byte v1.0</div>
            <div class="font-mono-code font-bold text-xs text-rose-300">3,6 / 5,0 (72,0%)</div>
          </div>
          <div class="bg-slate-900 rounded p-1.5 border border-emerald-500/40">
            <div class="text-[9px] text-slate-400 uppercase font-tech">Média Byte v2.0</div>
            <div class="font-mono-code font-bold text-xs text-emerald-300">4,4 / 5,0 (88,0%)</div>
          </div>
          <div class="bg-slate-900 rounded p-1.5 border border-cyan-500/40">
            <div class="text-[9px] text-slate-400 uppercase font-tech">Evolução Global</div>
            <div class="font-mono-code font-bold text-xs text-cyan-300">+22,2% GANHO</div>
          </div>
          <div class="bg-slate-900 rounded p-1.5 border border-purple-500/40">
            <div class="text-[9px] text-slate-400 uppercase font-tech">Taxa de Regressão</div>
            <div class="font-mono-code font-bold text-xs text-purple-300">0% (Zero Quedas)</div>
          </div>
        </div>
      </div>

      <!-- Painel Visual do Caso #03: O Momento Eureka de Clara -->
      <div class="col-span-4 section-card p-3 border-2 border-amber-400/70 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-1">
            <span class="font-comic-title text-base text-amber-300">ZOOM NO CASO #03 · O MOMENTO EUREKA</span>
            <span class="score-chip bg-emerald-400 text-slate-950 !text-[9px]">2,0 ➔ 4,0 (+100%)</span>
          </div>

          <div class="h-32 rounded-xl overflow-hidden border-2 border-cyan-400 mb-1.5 relative shadow-md">
            <img src="data:image/jpeg;base64,{b64_boxes}" alt="Clara compreendendo o conceito de memória com as caixas organizadoras coloridas apresentadas pelo Byte v2.0." class="w-full h-full object-cover">
            <div class="absolute bottom-1 right-1 bg-slate-950/90 text-cyan-300 font-mono-code text-[8.5px] px-2 py-0.5 rounded border border-cyan-400/50">
              Metáfora das Caixas (ZDP)
            </div>
          </div>

          <div class="bg-rose-950/50 border border-rose-500/50 rounded-lg p-1.5 mb-1 text-[9.5px]">
            <strong class="text-rose-300 block uppercase font-tech text-[9px]">Como o Byte v1.0 falhou (Nota 2,0/5,0):</strong>
            <span class="text-rose-100 italic">"O objeto PyObject é alocado na Heap via CPython e ciclos de Garbage Collector..."</span>
          </div>

          <div class="bg-emerald-950/50 border border-emerald-400/60 rounded-lg p-1.5 mb-1 text-[9.5px]">
            <strong class="text-emerald-300 block uppercase font-tech text-[9px]">Como o Byte v2.0 mediou (Nota 4,0/5,0):</strong>
            <span class="text-emerald-100 italic">"Pense na memória como caixas coloridas etiquetadas! Se a etiqueta é 'idade' e você faz aniversário, o que muda?"</span>
          </div>
        </div>

        <div class="bg-amber-950/40 border border-amber-400/60 rounded-lg p-1.5 text-[9px] text-amber-100 leading-tight">
          <strong class="text-amber-300 uppercase font-tech block mb-0.5"><i class="fa-solid fa-lightbulb mr-1"></i>O Problema dos 2 Sigmas de Bloom (1984):</strong>
          Benjamin Bloom provou que a tutoria individual socrática eleva o aprendizado em 2 desvios-padrão (+2 sigmas). O modelo Khanmigo de Sal Khan (TED, 2023) democratiza isso 24h na EaD!
        </div>
      </div>
    </div>

    <!-- =======================================================================
         BLOCO 04: CIRURGIA NO SYSTEM PROMPT (AS 4 TRAVAS) + CICLO DOCENTE
         ======================================================================= -->
    <div class="grid grid-cols-12 gap-2.5 mb-2">
      <!-- As 4 Travas Pedagógicas da HQ (Cirurgia Neural) -->
      <div class="col-span-7 section-card p-3 border-2 border-emerald-400/70 flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-1.5">
            <span class="font-comic-title text-xl text-emerald-300 tracking-wide">
              <i class="fa-solid fa-terminal mr-1"></i> 5. CIRURGIA NO SYSTEM PROMPT (AS 4 TRAVAS DA HQ)
            </span>
            <button onclick="copyInfographicPrompt()" id="btnCopyInfoPrompt" class="no-print bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-extrabold text-[10px] px-2.5 py-0.5 rounded transition font-mono-code">
              <i class="fa-regular fa-copy"></i> Copiar Prompt v2.0
            </button>
          </div>

          <div class="grid grid-cols-2 gap-2 mb-1.5">
            <!-- Trava 1 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border-l-4 border-l-rose-500 border border-slate-800">
              <div class="font-tech font-bold text-[9.5px] text-rose-300 uppercase flex items-center justify-between">
                <span>TRAVA 01 · ANTI-COLA</span>
                <span class="text-[8px] bg-rose-950 px-1 rounded">REQUISITO</span>
              </div>
              <p class="text-[9.5px] text-slate-200 leading-tight mt-0.5">
                Proibido fornecer blocos de código prontos ou a solução direta no primeiro turno.
              </p>
            </div>

            <!-- Trava 2 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border-l-4 border-l-amber-400 border border-slate-800">
              <div class="font-tech font-bold text-[9.5px] text-amber-300 uppercase flex items-center justify-between">
                <span>TRAVA 02 · METÁFORA</span>
                <span class="text-[8px] bg-amber-950 px-1 rounded">CHEVALLARD</span>
              </div>
              <p class="text-[9.5px] text-slate-200 leading-tight mt-0.5">
                Conceitos abstratos abrem obrigatoriamente com analogias cotidianas (caixas, receitas, armários).
              </p>
            </div>

            <!-- Trava 3 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border-l-4 border-l-cyan-400 border border-slate-800">
              <div class="font-tech font-bold text-[9.5px] text-cyan-300 uppercase flex items-center justify-between">
                <span>TRAVA 03 · GATILHO SOCRÁTICO</span>
                <span class="text-[8px] bg-cyan-950 px-1 rounded">SÓCRATES</span>
              </div>
              <p class="text-[9.5px] text-slate-200 leading-tight mt-0.5">
                100% das mensagens terminam com uma pergunta reflexiva que devolve o raciocínio ao discente.
              </p>
            </div>

            <!-- Trava 4 -->
            <div class="bg-slate-950 p-1.5 rounded-lg border-l-4 border-l-purple-400 border border-slate-800">
              <div class="font-tech font-bold text-[9.5px] text-purple-300 uppercase flex items-center justify-between">
                <span>TRAVA 04 · ESCADA DE DICAS</span>
                <span class="text-[8px] bg-purple-950 px-1 rounded">BRUNER</span>
              </div>
              <p class="text-[9.5px] text-slate-200 leading-tight mt-0.5">
                Hint Ladder: Pergunta aberta ➔ Pseudocódigo lacunado ➔ Exemplo análogo ➔ Solução guiada.
              </p>
            </div>
          </div>
        </div>

        <pre id="infoPromptText" class="font-mono-code text-[8.5px] text-cyan-200 whitespace-pre-wrap leading-snug bg-slate-950 p-2 rounded-lg border border-emerald-500/40">Você é o Byte v2.0, tutor socrático de Programação Python para calouros de Licenciatura em Computação (EaD · UFRPE).
1. NUNCA forneça código pronto no 1º turno. Force o estudante a identificar o erro e descrever a lógica esperada.
2. Todo conceito novo abre com uma METÁFORA DO COTIDIANO (caixas etiquetadas, receitas, armários) antes de formalizar.
3. Se houver erro de sintaxe, aponte a linha e pergunte o que o aluno esperava que aquele comando realizasse.
4. Mantenha estrito alinhamento ao escopo de Programação na EaD. Recuse cordialmente pedidos externos.
5. É OBRIGATÓRIO encerrar 100% das mensagens com UMA PERGUNTA SOCRÁTICA INVESTIGATIVA sobre o próximo passo.</pre>
      </div>

      <!-- Ciclo de Curadoria em 4 Fases + Os 3 Pilares Éticos -->
      <div class="col-span-5 section-card p-3 border-2 border-purple-400/70 flex flex-col justify-between">
        <div>
          <span class="font-comic-title text-xl text-purple-300 tracking-wide block mb-1">
            <i class="fa-solid fa-rotate mr-1"></i> 6. CICLO DOCENTE (4 FASES) & ÉTICA NA EAD
          </span>

          <div class="grid grid-cols-2 gap-1.5 mb-1.5">
            <div class="bg-slate-950 p-1.5 rounded-lg border border-cyan-500/40">
              <div class="font-comic-title text-xs text-cyan-300">FASE 1 · TESTAR</div>
              <p class="text-[9px] text-slate-200 leading-tight">Submeter o tutor aos 5 casos reais (conceito, debug, memória, POO e escopo).</p>
            </div>
            <div class="bg-slate-950 p-1.5 rounded-lg border border-purple-500/40">
              <div class="font-comic-title text-xs text-purple-300">FASE 2 · REGISTRAR</div>
              <p class="text-[9px] text-slate-200 leading-tight">Pontuar na matriz 4D (1 a 5) diagnosticando gargalos empíricos com precisão.</p>
            </div>
            <div class="bg-slate-950 p-1.5 rounded-lg border border-amber-500/40">
              <div class="font-comic-title text-xs text-amber-300">FASE 3 · REVISAR</div>
              <p class="text-[9px] text-slate-200 leading-tight">Cirurgia neural no System Prompt aplicando as 4 travas pedagógicas anti-cola.</p>
            </div>
            <div class="bg-slate-950 p-1.5 rounded-lg border border-emerald-500/40">
              <div class="font-comic-title text-xs text-emerald-300">FASE 4 · VALIDAR</div>
              <p class="text-[9px] text-slate-200 leading-tight">Reteste completo confirmando ganho (+22,2%) e zero regressão pedagógica.</p>
            </div>
          </div>

          <!-- Os 3 Pilares Éticos da HQ -->
          <div class="bg-slate-950 p-1.5 rounded-lg border border-amber-400/60 mb-1">
            <div class="font-tech font-bold text-[9.5px] text-amber-300 uppercase mb-0.5">
              <i class="fa-solid fa-shield-heart mr-1"></i> Os 3 Pilares Éticos da Tutoria com IA
            </div>
            <div class="grid grid-cols-3 gap-1 text-[8.5px] text-slate-200 leading-tight">
              <div><b class="text-rose-300">1. Senso Crítico:</b> LLMs alucinam. A validação humana docente é insubstituível.</div>
              <div><b class="text-amber-300">2. LGPD e Privacidade:</b> Proibido dados de estudantes e CPFs em prompts.</div>
              <div><b class="text-cyan-300">3. Afeto Docente:</b> A IA apoia 24h, mas jamais substitui a escuta do educador.</div>
            </div>
          </div>
        </div>

        <div class="bg-slate-950 p-1.5 rounded-lg border border-slate-800 text-[8.5px] text-slate-300 leading-tight">
          <strong class="text-cyan-300 uppercase font-tech">Referências Científicas:</strong>
          OCDE (2026) <em>PISA 2025: Future-Ready Students</em> · Chevallard (1991) <em>Transposition Didactique</em> · Vygotsky (1978) <em>Mind in Society (ZDP)</em> · Bruner (1976) <em>Scaffolding</em> · Bloom (1984) <em>2 Sigmas</em> · Sal Khan (2023) <em>Khanmigo</em> · Xu et al. (2025) <em>EduBench</em>.
        </div>
      </div>
    </div>

    <!-- RODAPÉ DO PÔSTER -->
    <div class="flex items-center justify-between text-[10px] text-slate-300 border-t border-slate-800 pt-1.5 mt-0.5">
      <div>
        <strong>Projeto 2ª VA · Educação a Distância (EaD)</strong> · Licenciatura em Computação (UFRPE · 2026.2) · Orientador: Prof. Ermeson
      </div>
      <div class="font-mono-code text-cyan-300 font-bold">
        INFOGRÁFICO SÍNTESE · AUTOR: CAUÃ DA CUNHA LIRA
      </div>
    </div>

  </main>

  <script>
    function copyInfographicPrompt() {{
      const text = document.getElementById('infoPromptText').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const btn = document.getElementById('btnCopyInfoPrompt');
        const original = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
        setTimeout(() => {{ btn.innerHTML = original; }}, 2000);
      }});
    }}

    function highlightVersion(mode) {{
      const btnAll = document.getElementById('btnFilterAll');
      const btnV1 = document.getElementById('btnFilterV1');
      const btnV2 = document.getElementById('btnFilterV2');
      [btnAll, btnV1, btnV2].forEach(b => b.classList.remove('mode-active-btn'));

      const v1Chips = document.querySelectorAll('.row-v1');
      const v2Chips = document.querySelectorAll('.row-v2');
      const card2 = document.getElementById('cardNivel2');
      const card3 = document.getElementById('cardNivel3');

      v1Chips.forEach(el => {{ el.style.opacity = '1'; el.style.transform = 'scale(1)'; }});
      v2Chips.forEach(el => {{ el.style.opacity = '1'; el.style.transform = 'scale(1)'; }});
      card2.style.opacity = '1';
      card3.style.opacity = '1';

      if (mode === 'all') {{
        btnAll.classList.add('mode-active-btn');
      }} else if (mode === 'v1') {{
        btnV1.classList.add('mode-active-btn');
        v2Chips.forEach(el => {{ el.style.opacity = '0.25'; }});
        v1Chips.forEach(el => {{ el.style.transform = 'scale(1.1)'; }});
        card3.style.opacity = '0.35';
      }} else if (mode === 'v2') {{
        btnV2.classList.add('mode-active-btn');
        v1Chips.forEach(el => {{ el.style.opacity = '0.25'; }});
        v2Chips.forEach(el => {{ el.style.transform = 'scale(1.1)'; }});
        card2.style.opacity = '0.35';
      }}
    }}
  </script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

sz_mb = os.path.getsize(OUT_HTML) / (1024 * 1024)
print(f"Sucesso! {OUT_HTML} gerado. Tamanho: {sz_mb:.2f} MB")
