# -*- coding: utf-8 -*-
"""
Gerador do Infográfico Atualizado: Anatomia e Calibragem de um Tutor Socrático de IA
Edição Editorial Anti-AI-Slop · Sincronizado 100% com a HQ (12 Páginas A4)
UFRPE · 2ª VA de Educação a Distância (2026.2)
Autor: Cauã da Cunha Lira | Orientador: Prof. Ermeson
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
HQ_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/infografico.html")

def get_b64(filename):
    p_opt = os.path.join(OPT_DIR, filename)
    p_hq = os.path.join(HQ_DIR, filename)
    target = p_opt if os.path.exists(p_opt) else p_hq
    with open(target, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando ilustrações para o infográfico...")
b64_byte = get_b64("p2_panel3_byte.jpg")
b64_scanner = get_b64("p4_panel1_scanner_clean.jpg")
b64_boxes = get_b64("p7_panel2_boxes.jpg")
b64_surgery = get_b64("p8_panel1_surgery.jpg")
b64_epilogue = get_b64("p12_panel1_epilogue.jpg")
print("Ilustrações carregadas com sucesso!")

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
  <link href="https://fonts.googleapis.com/css2?family=Bangers&family=Chakra+Petch:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&family=Space+Grotesk:wght@600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-dark: #070A11;
      --card-bg: #0F172A;
      --card-inner: #090D16;
      --border-subtle: #1E293B;
      --border-highlight: #334155;
      --cyan-neon: #06B6D4;
      --cyan-soft: #22D3EE;
      --amber-warm: #F59E0B;
      --emerald-clean: #10B981;
      --rose-danger: #EF4444;
      --purple-accent: #8B5CF6;
    }}

    * {{ box-sizing: border-box; }}

    body {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: var(--bg-dark);
      color: #F8FAFC;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }}

    .font-comic {{
      font-family: 'Bangers', cursive;
      letter-spacing: 1.2px;
    }}

    .font-tech {{
      font-family: 'Space Grotesk', sans-serif;
    }}

    .font-mono-code {{
      font-family: 'JetBrains Mono', monospace;
    }}

    /* Editorial Poster Container */
    .infographic-poster {{
      width: 240mm;
      max-width: 100%;
      margin: 32px auto;
      background-color: #0B0F19;
      background-image:
        radial-gradient(rgba(139, 92, 246, 0.08) 1.5px, transparent 1.5px),
        radial-gradient(rgba(6, 182, 212, 0.06) 1.5px, #0B0F19 1.5px);
      background-size: 24px 24px;
      background-position: 0 0, 12px 12px;
      border: 3px solid #1E293B;
      border-radius: 20px;
      padding: 12mm;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.85);
      position: relative;
    }}

    .section-card {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(8px);
      border: 1.5px solid var(--border-subtle);
      border-radius: 14px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }}

    .section-card:hover {{
      border-color: var(--border-highlight);
    }}

    .badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 3px 10px;
      border-radius: 999px;
      white-space: nowrap;
    }}

    .score-chip {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 800;
      font-size: 11.5px;
      padding: 2.5px 8px;
      border-radius: 6px;
      white-space: nowrap;
    }}

    @media print {{
      @page {{
        size: 240mm 600mm;
        margin: 0;
      }}
      html, body {{
        width: 240mm !important;
        height: 600mm !important;
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
        margin: 0 !important;
        padding: 8mm 10mm !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        width: 240mm !important;
        height: 600mm !important;
        max-height: 600mm !important;
        overflow: hidden !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Sticky Navigation & Download Toolbar (No-Print) -->
  <nav class="no-print sticky top-0 z-50 bg-slate-950/90 backdrop-blur-md border-b border-slate-800 px-4 py-3 shadow-xl">
    <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-between gap-3 text-white">
      <div class="flex items-center gap-3">
        <a href="index.html" class="flex items-center gap-1.5 text-xs font-bold text-cyan-400 hover:text-cyan-300 transition-colors bg-slate-900 border border-cyan-500/30 px-3 py-1.5 rounded-lg shadow-sm">
          <i class="fa-solid fa-arrow-left"></i> Hub da Disciplina
        </a>
        <a href="ebook-hq.html" class="flex items-center gap-1.5 text-xs font-bold text-purple-300 hover:text-purple-200 transition-colors bg-purple-950/40 border border-purple-500/30 px-3 py-1.5 rounded-lg shadow-sm">
          <i class="fa-solid fa-book-open"></i> Ler HQ (12 Páginas)
        </a>
        <div class="hidden sm:flex items-center gap-2 pl-2 border-l border-slate-800">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></span>
          <span class="font-extrabold text-xs tracking-wider text-slate-300 uppercase">
            INFOGRÁFICO ACADÊMICO · UFRPE 2026.2
          </span>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="px-3 py-1.5 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-lg border border-slate-700 transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> Imprimir Pôster
        </button>
        <a href="assets/infografico-anatomia-tutor-ia.pdf" target="_blank" class="px-3.5 py-1.5 text-xs bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-lg transition shadow-md flex items-center gap-1.5">
          <i class="fa-solid fa-file-pdf"></i> Baixar PDF Oficial
        </a>
      </div>
    </div>
  </nav>

  <!-- =========================================================================
       MAIN POSTER CONTAINER (240mm x 540mm)
       ========================================================================= -->
  <main class="infographic-poster">

    <!-- HEADER CANÔNICO EDITORIAL -->
    <header class="border-b-2 border-slate-700/80 pb-5 mb-6">
      <div class="flex flex-wrap items-center justify-between gap-3 text-xs text-slate-400 font-mono-code mb-2">
        <div class="flex items-center gap-2 font-semibold">
          <span class="text-cyan-400 font-bold">UFRPE</span> · UNIVERSIDADE FEDERAL RURAL DE PERNAMBUCO
          <span class="text-slate-600">|</span> DEPARTAMENTO DE EDUCAÇÃO E EAD
        </div>
        <div class="flex items-center gap-2">
          <span class="badge-pill bg-purple-950/80 text-purple-300 border border-purple-500/40">
            <i class="fa-solid fa-graduation-cap"></i> 2ª VA · LICENCIATURA EM COMPUTAÇÃO
          </span>
          <span class="badge-pill bg-cyan-950/80 text-cyan-300 border border-cyan-500/40">
            PROF. ERMESON
          </span>
        </div>
      </div>

      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mt-3">
        <div>
          <h1 class="font-comic text-4xl md:text-5xl text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-cyan-200 to-purple-300 leading-none tracking-wide">
            ANATOMIA E CALIBRAGEM DE UM TUTOR SOCRÁTICO DE IA
          </h1>
          <p class="font-tech text-slate-300 text-sm md:text-base mt-2 font-medium max-w-4xl leading-relaxed">
            Como transformar geradores automáticos de respostas prontas em mediadores reflexivos da Zona de Desenvolvimento Proximal na Educação a Distância.
          </p>
        </div>
        <div class="hidden md:flex flex-col items-end text-right bg-slate-900/80 border border-slate-800 p-3 rounded-xl min-w-[210px]">
          <span class="text-[10px] text-slate-400 font-mono uppercase tracking-wider">Autor & Pesquisador</span>
          <span class="font-bold text-sm text-white">Cauã da Cunha Lira</span>
          <span class="text-[11px] text-cyan-400 font-medium">Estudo de Caso: Operação Byte Socrático</span>
        </div>
      </div>
    </header>

    <!-- =========================================================================
         ATO 1: O PROBLEMA REAL NA EAD — A ARMADILHA DA RESPOSTA MASTIGADA
         ========================================================================= -->
    <section class="mb-6">
      <div class="flex items-center gap-2 mb-3">
        <span class="w-2.5 h-6 bg-amber-400 rounded-sm"></span>
        <h2 class="font-comic text-2xl text-amber-300 tracking-wide">
          1. O DIAGNÓSTICO: A ILUSÃO DE COMPETÊNCIA E O APAGÃO NA FOLHA EM BRANCO
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
        <!-- Diagnóstico PISA & Clara -->
        <div class="md:col-span-5 section-card p-4 flex flex-col justify-between border-l-4 border-l-amber-400">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-tech font-bold text-xs text-amber-300 uppercase tracking-wider">
                <i class="fa-solid fa-brain mr-1.5"></i> Offloading Cognitivo
              </span>
              <span class="font-mono-code text-[10px] bg-amber-400/10 text-amber-300 px-2 py-0.5 rounded border border-amber-400/30">
                PISA 2025 · OCDE (2026)
              </span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              O relatório <em>Future-Ready Students</em> (OCDE, set/2026) constatou que <strong>48% dos estudantes brasileiros</strong> utilizam IA semanalmente nos estudos (46% na OCDE). Apenas 11% nunca utilizaram.
            </p>
            <div class="bg-rose-950/40 border border-rose-500/40 rounded-xl p-3 mb-2 text-xs text-rose-200 leading-relaxed">
              <strong class="text-rose-300 block mb-1 font-tech uppercase text-[11px]">
                <i class="fa-solid fa-triangle-exclamation mr-1"></i> O Drama de Clara no Polo:
              </strong>
              Ao usar uma IA sem freio pedagógico (Byte v1.0), Clara recebe o código pronto e acredita ter aprendido. Na prova presencial individual sem computador, ocorre o <strong>apagão cognitivo</strong> diante da folha em branco.
            </div>
          </div>
          <div class="text-[11px] text-slate-400 font-mono-code pt-2 border-t border-slate-800">
            Conclusão: Banir a IA é inútil; o desafio é calibrar o tutor para ensinar a pensar.
          </div>
        </div>

        <!-- Os 3 Níveis de Apoio -->
        <div class="md:col-span-7 section-card p-4 flex flex-col justify-between border-l-4 border-l-cyan-400">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-tech font-bold text-xs text-cyan-300 uppercase tracking-wider">
                <i class="fa-solid fa-layer-group mr-1.5"></i> A Evolução da Mediação Pedagógica na EaD
              </span>
              <span class="font-mono-code text-[10px] text-slate-400">3 GERAÇÕES TECNOLÓGICAS</span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-2">
              <!-- Nível 1 -->
              <div class="bg-slate-950/80 border border-slate-800 rounded-xl p-3 flex flex-col justify-between">
                <div>
                  <div class="text-[10px] font-mono font-bold text-slate-400 uppercase mb-1">Nível 01 · Passado</div>
                  <h4 class="font-bold text-white text-xs mb-1.5">Chatbot de Regras</h4>
                  <p class="text-[11px] text-slate-400 leading-snug">
                    Árvores de decisão rígidas. Qualquer dúvida fora do script causa bloqueio na interação.
                  </p>
                </div>
                <div class="mt-2 pt-2 border-t border-slate-800 text-[10px] text-slate-500 font-mono">
                  Flexibilidade: Baixa
                </div>
              </div>

              <!-- Nível 2 -->
              <div class="bg-rose-950/30 border-2 border-rose-500/60 rounded-xl p-3 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-mono font-bold text-rose-300 uppercase">Nível 02 · Risco</span>
                    <span class="score-chip bg-rose-600 text-white text-[9.5px]">v1.0</span>
                  </div>
                  <h4 class="font-bold text-rose-200 text-xs mb-1.5">LLM sem Freio</h4>
                  <p class="text-[11px] text-rose-100/80 leading-snug">
                    Respostas prontas instantâneas e colapso em jargões herméticos de compiladores C (PyObject, Heap).
                  </p>
                </div>
                <div class="mt-2 pt-2 border-t border-rose-900/50 text-[10px] text-rose-300 font-mono font-bold">
                  Média: 3,6 / 5,0 (72%)
                </div>
              </div>

              <!-- Nível 3 -->
              <div class="bg-emerald-950/30 border-2 border-emerald-400 rounded-xl p-3 flex flex-col justify-between">
                <div>
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-[10px] font-mono font-bold text-emerald-300 uppercase">Nível 03 · Alvo</span>
                    <span class="score-chip bg-emerald-400 text-slate-950 text-[9.5px]">v2.0</span>
                  </div>
                  <h4 class="font-bold text-emerald-200 text-xs mb-1.5">Tutor Socrático</h4>
                  <p class="text-[11px] text-emerald-100/90 leading-snug">
                    Bloqueado contra respostas prontas. Andaimes cognitivos (Bruner) e mediação na ZDP (Vygotsky).
                  </p>
                </div>
                <div class="mt-2 pt-2 border-t border-emerald-900/50 text-[10px] text-emerald-300 font-mono font-bold">
                  Média: 4,4 / 5,0 (88%)
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         ATO 2: A BÚSSOLA PEDAGÓGICA — O SCANNER 4D
         ========================================================================= -->
    <section class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-6 bg-cyan-400 rounded-sm"></span>
          <h2 class="font-comic text-2xl text-cyan-300 tracking-wide">
            2. A BÚSSOLA: SCANNER PEDAGÓGICO DE 4 CRITÉRIOS (MATRIZ 4D)
          </h2>
        </div>
        <span class="text-xs text-slate-400 font-mono hidden md:inline">
          Rigor Epistemológico: Chevallard (1991), Bruner (1976), Vygotsky (1978) e EduBench (2025)
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-3.5">
        <!-- 01. Correção -->
        <div class="section-card p-3.5 border-t-4 border-t-cyan-400 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-comic text-lg text-cyan-300">01. CORREÇÃO</span>
              <span class="w-7 h-7 rounded-full bg-cyan-950 border border-cyan-400/50 flex items-center justify-center text-cyan-400 text-xs">
                <i class="fa-solid fa-shield-halved"></i>
              </span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              Rigor conceitual e sintático em Python. Proíbe alucinar bibliotecas ou inventar funções inexistentes.
            </p>
          </div>
          <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[11px] font-mono-code text-cyan-300">
            <strong>Auditoria:</strong> O código é tecnicamente verdadeiro e sem alucinações?
          </div>
        </div>

        <!-- 02. Clareza -->
        <div class="section-card p-3.5 border-t-4 border-t-amber-400 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-comic text-lg text-amber-300">02. CLAREZA</span>
              <span class="w-7 h-7 rounded-full bg-amber-950 border border-amber-400/50 flex items-center justify-center text-amber-400 text-xs">
                <i class="fa-solid fa-lightbulb"></i>
              </span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              Organização passo a passo e empatia pedagógica. Uso mandatório de analogias do cotidiano antes de qualquer formalismo.
            </p>
          </div>
          <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[11px] font-mono-code text-amber-300">
            <strong>Auditoria:</strong> A explicação é acessível e estruturada para um iniciante?
          </div>
        </div>

        <!-- 03. Adequação / ZDP -->
        <div class="section-card p-3.5 border-t-4 border-t-emerald-400 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-comic text-lg text-emerald-300">03. ADEQUAÇÃO / ZDP</span>
              <span class="w-7 h-7 rounded-full bg-emerald-950 border border-emerald-400/50 flex items-center justify-center text-emerald-400 text-xs">
                <i class="fa-solid fa-stairs"></i>
              </span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              <strong>Transposição Didática:</strong> Respeita o nível cognitivo da caloura. Proíbe jargões herméticos de compiladores C (CPython/Heap).
            </p>
          </div>
          <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[11px] font-mono-code text-emerald-300">
            <strong>Auditoria:</strong> O tutor transforma o saber sábio em saber ensinado?
          </div>
        </div>

        <!-- 04. Escopo -->
        <div class="section-card p-3.5 border-t-4 border-t-purple-400 flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-comic text-lg text-purple-300">04. ESCOPO</span>
              <span class="w-7 h-7 rounded-full bg-purple-950 border border-purple-400/50 flex items-center justify-center text-purple-400 text-xs">
                <i class="fa-solid fa-bullseye"></i>
              </span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              Foco estrito na ementa da disciplina (Programação na EaD). Recusa cortês a desvios temáticos alheios (ex.: História).
            </p>
          </div>
          <div class="bg-slate-950 p-2 rounded-lg border border-slate-800 text-[11px] font-mono-code text-purple-300">
            <strong>Auditoria:</strong> Bloqueia desvios sem perder a cortesia com o discente?
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         ATO 3: A EXPERIMENTAÇÃO — BATERIA CANÔNICA & O CASO #03 (MEMÓRIA)
         ========================================================================= -->
    <section class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-6 bg-emerald-400 rounded-sm"></span>
          <h2 class="font-comic text-2xl text-emerald-300 tracking-wide">
            3. A EXPERIMENTAÇÃO: BATERIA CANÔNICA EM PYTHON E O MOMENTO EUREKA
          </h2>
        </div>
        <span class="font-mono-code text-xs text-emerald-400 bg-emerald-950/60 px-2.5 py-1 rounded border border-emerald-500/40">
          Claude Opus 4.6 (Temp 0.0) · 10 Rodadas · Rubrica 1 a 5
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
        <!-- Tabela dos 5 Casos -->
        <div class="md:col-span-7 section-card p-4 flex flex-col justify-between">
          <div>
            <h3 class="font-tech font-bold text-sm text-cyan-300 uppercase mb-3 flex items-center gap-2">
              <i class="fa-solid fa-table-list"></i> Matriz de Desempenho dos 5 Casos de Teste
            </h3>

            <div class="space-y-2">
              <!-- Caso 01 -->
              <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <div class="font-bold text-white text-xs">#01. O que é uma variável?</div>
                  <div class="text-[10px] text-slate-400">Correção & Clareza</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="score-chip bg-slate-800 text-amber-300 border border-slate-700">v1: 4,0</span>
                  <i class="fa-solid fa-arrow-right text-slate-500 text-xs"></i>
                  <span class="score-chip bg-emerald-400 text-slate-950">v2: 5,0</span>
                  <span class="text-[11px] font-mono font-bold text-emerald-400">+25%</span>
                </div>
              </div>

              <!-- Caso 02 -->
              <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <div class="font-bold text-white text-xs">#02. SyntaxError no laço for</div>
                  <div class="text-[10px] text-slate-400">Clareza & Scaffolding</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="score-chip bg-slate-800 text-amber-300 border border-slate-700">v1: 3,0</span>
                  <i class="fa-solid fa-arrow-right text-slate-500 text-xs"></i>
                  <span class="score-chip bg-emerald-400 text-slate-950">v2: 4,0</span>
                  <span class="text-[11px] font-mono font-bold text-emerald-400">+33%</span>
                </div>
              </div>

              <!-- Caso 03 (Destaque) -->
              <div class="bg-gradient-to-r from-rose-950/40 via-slate-950 to-emerald-950/40 p-2.5 rounded-xl border-2 border-emerald-400 flex items-center justify-between gap-2">
                <div>
                  <div class="flex items-center gap-1.5">
                    <span class="font-bold text-white text-xs">#03. Como funciona a memória?</span>
                    <span class="text-[9px] bg-rose-900/80 text-rose-200 px-1.5 py-0.2 rounded font-mono font-bold uppercase">Gargalo</span>
                  </div>
                  <div class="text-[10px] text-emerald-300 font-semibold">Adequação / ZDP (Vygotsky)</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="score-chip bg-rose-600 text-white">v1: 2,0</span>
                  <i class="fa-solid fa-arrow-right text-emerald-400 text-xs"></i>
                  <span class="score-chip bg-emerald-400 text-slate-950 font-extrabold">v2: 4,0</span>
                  <span class="text-[11px] font-mono font-extrabold text-emerald-300">+100%</span>
                </div>
              </div>

              <!-- Caso 04 -->
              <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <div class="font-bold text-white text-xs">#04. POO vs. Estruturada</div>
                  <div class="text-[10px] text-slate-400">Rigor Conceitual</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="score-chip bg-slate-800 text-cyan-300 border border-slate-700">v1: 4,0</span>
                  <i class="fa-solid fa-arrow-right text-slate-500 text-xs"></i>
                  <span class="score-chip bg-cyan-400 text-slate-950">v2: 4,0</span>
                  <span class="text-[11px] font-mono font-bold text-slate-400">Estável</span>
                </div>
              </div>

              <!-- Caso 05 -->
              <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <div class="font-bold text-white text-xs">#05. Dúvida externa (História)</div>
                  <div class="text-[10px] text-slate-400">Escudo de Escopo</div>
                </div>
                <div class="flex items-center gap-2">
                  <span class="score-chip bg-slate-800 text-emerald-300 border border-slate-700">v1: 5,0</span>
                  <i class="fa-solid fa-arrow-right text-slate-500 text-xs"></i>
                  <span class="score-chip bg-emerald-400 text-slate-950">v2: 5,0</span>
                  <span class="text-[11px] font-mono font-bold text-emerald-400">Perfeito</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Métricas Síntese -->
          <div class="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-slate-800 text-center">
            <div class="bg-slate-900/80 p-2 rounded-lg border border-slate-800">
              <div class="text-[10px] text-slate-400 uppercase font-mono">Média Byte v1.0</div>
              <div class="font-mono-code font-bold text-sm text-rose-300">3,6 / 5,0 (72%)</div>
            </div>
            <div class="bg-slate-900/80 p-2 rounded-lg border border-emerald-500/40">
              <div class="text-[10px] text-slate-400 uppercase font-mono">Média Byte v2.0</div>
              <div class="font-mono-code font-bold text-sm text-emerald-300">4,4 / 5,0 (88%)</div>
            </div>
            <div class="bg-slate-900/80 p-2 rounded-lg border border-cyan-500/40">
              <div class="text-[10px] text-slate-400 uppercase font-mono">Ganho Médio</div>
              <div class="font-mono-code font-bold text-sm text-cyan-300">+22,2% GLOBAL</div>
            </div>
          </div>
        </div>

        <!-- Zoom no Caso #03: O Momento Eureka -->
        <div class="md:col-span-5 section-card p-4 flex flex-col justify-between border-2 border-amber-400/80">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-comic text-lg text-amber-300">O MOMENTO EUREKA (CASO #03)</span>
              <span class="score-chip bg-emerald-400 text-slate-950 font-bold text-xs">+100% GANHO</span>
            </div>

            <!-- Imagem da Metáfora das Caixas -->
            <div class="rounded-xl overflow-hidden border border-slate-700 mb-3 relative shadow-md h-36">
              <img src="data:image/jpeg;base64,{b64_boxes}" alt="Clara compreendendo o conceito com a metáfora das caixas organizadoras." class="w-full h-full object-cover">
              <div class="absolute bottom-1.5 right-1.5 bg-slate-950/90 text-cyan-300 font-mono text-[9.5px] px-2 py-0.5 rounded border border-cyan-400/40">
                Metáfora das Caixas (ZDP)
              </div>
            </div>

            <div class="space-y-2 text-xs">
              <div class="bg-rose-950/40 border border-rose-500/40 rounded-lg p-2.5">
                <strong class="text-rose-300 block font-mono text-[10px] uppercase mb-0.5">Como o Byte v1.0 falhou (Nota 2,0):</strong>
                <p class="text-rose-100/90 italic text-[11px] leading-snug">
                  "O objeto PyObject é alocado na Heap via CPython e gerenciado por contagem de referências do Garbage Collector..."
                </p>
              </div>

              <div class="bg-emerald-950/40 border border-emerald-400/50 rounded-lg p-2.5">
                <strong class="text-emerald-300 block font-mono text-[10px] uppercase mb-0.5">Como o Byte v2.0 mediou (Nota 4,0):</strong>
                <p class="text-emerald-100/90 italic text-[11px] leading-snug">
                  "Pense na memória como caixas organizadoras etiquetadas! Se a caixa se chama 'idade' e você faz aniversário, o que muda?"
                </p>
              </div>
            </div>
          </div>

          <div class="mt-3 pt-2 border-t border-slate-800 text-[10.5px] text-slate-400 leading-snug">
            <strong class="text-amber-300">O Efeito 2 Sigmas de Bloom (1984):</strong> A mediação reflexiva socrática reproduz os ganhos de tutoria humana individualizada em escala 24h na EaD.
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         ATO 4: A CIRURGIA NO SYSTEM PROMPT (AS 4 TRAVAS DO TUTOR)
         ========================================================================= -->
    <section class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-2">
          <span class="w-2.5 h-6 bg-purple-400 rounded-sm"></span>
          <h2 class="font-comic text-2xl text-purple-300 tracking-wide">
            4. A CIRURGIA: AS 4 TRAVAS DO SYSTEM PROMPT SOCRÁTICO
          </h2>
        </div>
        <button onclick="copyInfographicPrompt()" id="btnCopyInfoPrompt" class="no-print bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-extrabold text-xs px-3 py-1 rounded-lg transition font-mono-code flex items-center gap-1.5 shadow-sm">
          <i class="fa-regular fa-copy"></i> Copiar Prompt v2.0
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-4">
        <!-- As 4 Travas -->
        <div class="md:col-span-6 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div class="section-card p-3 border-l-4 border-l-rose-500 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-tech font-bold text-xs text-rose-300 uppercase">Trava 01 · Anti-Cola</span>
                <span class="text-[9px] font-mono bg-rose-950 text-rose-300 px-1.5 py-0.5 rounded">Rigor</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mt-1">
                Proibido fornecer blocos de código prontos ou a solução direta no primeiro turno.
              </p>
            </div>
            <div class="text-[10px] text-slate-400 font-mono mt-2">Bloqueia o offloading passivo</div>
          </div>

          <div class="section-card p-3 border-l-4 border-l-amber-400 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-tech font-bold text-xs text-amber-300 uppercase">Trava 02 · Metáfora</span>
                <span class="text-[9px] font-mono bg-amber-950 text-amber-300 px-1.5 py-0.5 rounded">Didática</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mt-1">
                Conceitos abstratos abrem obrigatoriamente com analogias cotidianas (caixas, receitas, armários).
              </p>
            </div>
            <div class="text-[10px] text-slate-400 font-mono mt-2">Transposição de Chevallard</div>
          </div>

          <div class="section-card p-3 border-l-4 border-l-cyan-400 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-tech font-bold text-xs text-cyan-300 uppercase">Trava 03 · Gatilho</span>
                <span class="text-[9px] font-mono bg-cyan-950 text-cyan-300 px-1.5 py-0.5 rounded">Sócrates</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mt-1">
                100% das mensagens encerram com uma pergunta investigativa que devolve a reflexão à aluna.
              </p>
            </div>
            <div class="text-[10px] text-slate-400 font-mono mt-2">Garante a postura ativa</div>
          </div>

          <div class="section-card p-3 border-l-4 border-l-purple-400 flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-1">
                <span class="font-tech font-bold text-xs text-purple-300 uppercase">Trava 04 · Andaimes</span>
                <span class="text-[9px] font-mono bg-purple-950 text-purple-300 px-1.5 py-0.5 rounded">Bruner</span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mt-1">
                Escada de dicas gradativa: Pista reflexiva ➔ Pseudocódigo lacunado ➔ Exemplo guiado.
              </p>
            </div>
            <div class="text-[10px] text-slate-400 font-mono mt-2">Scaffolding estruturado</div>
          </div>
        </div>

        <!-- System Prompt Box -->
        <div class="md:col-span-6 section-card p-4 flex flex-col justify-between bg-slate-950/90 border border-slate-700">
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="font-mono text-xs text-cyan-300 font-bold flex items-center gap-1.5">
                <i class="fa-solid fa-terminal"></i> SYSTEM_PROMPT_BYTE_V2.TXT
              </span>
              <span class="text-[10px] text-slate-400 font-mono">v2.1 Anti-Loop Ready</span>
            </div>
            <pre id="infoPromptText" class="font-mono-code text-[11px] text-slate-300 whitespace-pre-wrap leading-relaxed bg-slate-900/90 p-3 rounded-xl border border-slate-800">Você é o Byte v2.0, tutor socrático de Programação Python para calouros de Licenciatura em Computação (EaD · UFRPE).

1. NUNCA forneça código pronto no 1º turno. Force o estudante a descrever o erro com as próprias palavras.
2. Todo conceito novo abre com uma METÁFORA DO COTIDIANO (caixas etiquetadas, receitas de bolo) antes do formalismo.
3. Se houver erro de sintaxe, aponte a linha e pergunte o que o aluno esperava que aquele comando realizasse.
4. Mantenha estrito alinhamento ao escopo de Programação na EaD. Recuse cordialmente pedidos externos.
5. É OBRIGATÓRIO encerrar 100% das mensagens com UMA PERGUNTA SOCRÁTICA INVESTIGATIVA sobre o próximo passo.</pre>
          </div>
          <div class="text-[10.5px] text-slate-400 mt-2 font-mono flex items-center justify-between">
            <span>Template pronto para uso em OpenAI, Anthropic, Google Gemini e Llama.</span>
            <span class="text-emerald-400 font-bold">100% Testado</span>
          </div>
        </div>
      </div>
    </section>

    <!-- =========================================================================
         FOOTER: OS 3 PILARES ÉTICOS E REFERÊNCIAS CIENTÍFICAS
         ========================================================================= -->
    <footer class="border-t-2 border-slate-800 pt-5 mt-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
        <div class="bg-slate-900/60 border border-slate-800 p-3 rounded-xl">
          <div class="font-tech font-bold text-xs text-cyan-300 uppercase mb-1">
            <i class="fa-solid fa-user-shield mr-1"></i> 1. Autonomia Discente
          </div>
          <p class="text-[11px] text-slate-300 leading-snug">
            A IA atua como andaime temporário para fortalecer o esforço cognitivo individual, jamais como muleta que atrofia o raciocínio.
          </p>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-3 rounded-xl">
          <div class="font-tech font-bold text-xs text-amber-300 uppercase mb-1">
            <i class="fa-solid fa-eye mr-1"></i> 2. Transparência Algorítmica
          </div>
          <p class="text-[11px] text-slate-300 leading-snug">
            O estudante tem ciência plena de que interage com um modelo de linguagem calibrado para orientá-lo reflexivamente.
          </p>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-3 rounded-xl">
          <div class="font-tech font-bold text-xs text-purple-300 uppercase mb-1">
            <i class="fa-solid fa-user-graduate mr-1"></i> 3. Human-in-the-Loop
          </div>
          <p class="text-[11px] text-slate-300 leading-snug">
            A curadoria e governança pedagógica pertencem ao corpo docente, que audita os logs e ajusta as travas do tutor.
          </p>
        </div>
      </div>

      <div class="flex flex-wrap items-center justify-between gap-3 text-[10.5px] text-slate-500 font-mono-code pt-3 border-t border-slate-900">
        <div>
          <strong>Referências Principais:</strong> Vygotsky (1978 · ZDP) · Bruner (1976 · Scaffolding) · Bloom (1984 · 2 Sigma) · Chevallard (1991 · Transposição Didática) · Xu et al. (EduBench · ICLR 2025) · OCDE (PISA 2025 · 2026).
        </div>
        <div>
          © 2026 Cauã da Cunha Lira · UFRPE / DEINFO · Licença MIT / Open Access
        </div>
      </div>
    </footer>

  </main>

  <script>
    function copyInfographicPrompt() {{
      const text = document.getElementById('infoPromptText').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const btn = document.getElementById('btnCopyInfoPrompt');
        const orig = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
        btn.classList.add('bg-emerald-400', 'text-slate-950');
        setTimeout(() => {{
          btn.innerHTML = orig;
          btn.classList.remove('bg-emerald-400', 'text-slate-950');
        }}, 2500);
      }}).catch(err => {{
        console.error('Falha ao copiar:', err);
      }});
    }}
  </script>
</body>
</html>
"""

with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Infográfico gerado com sucesso em: {{OUT_HTML}} (Tamanho: {{os.path.getsize(OUT_HTML)}} bytes)")
