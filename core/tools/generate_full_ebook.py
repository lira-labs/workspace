# -*- coding: utf-8 -*-
"""
Gerador Completo das 12 Páginas da HQ 'Operação Byte Socrático'
"""
import os
import base64

OPT_DIR = os.path.abspath(r"code/projeto_ead_tutores/assets/hq/opt")
OUT_HTML = os.path.abspath(r"code/projeto_ead_tutores/ebook-hq.html")

def get_b64(filename):
    p = os.path.join(OPT_DIR, filename)
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("Carregando 16 imagens...")
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

def make_header(chapter_title, badge_text="ARQUIVO UFRPE · 2ª VA"):
    return f"""
      <div class="hq-header">
        <span style="font-family: 'Space Grotesk', sans-serif; font-weight: 800; font-size: 0.70rem; color: #A5F3FC; text-transform: uppercase;">
          <i class="fa-solid fa-bolt mr-1 text-cyan-400"></i> {chapter_title}
        </span>
        <span style="font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 0.60rem; background: #06B6D4; color: #090D16; padding: 2px 7px; border-radius: 4px;">{badge_text}</span>
      </div>
    """

def make_footer(page_num, total_pages=12, custom_note=None):
    note = custom_note or "CAUÃ DA CUNHA LIRA · LICENCIATURA EM COMPUTAÇÃO (UFRPE · 2026.2)"
    return f"""
      <footer class="hq-footer">
        <span>OPERAÇÃO BYTE SOCRÁTICO · {note}</span>
        <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-extrabold font-mono">PÁG. {page_num:02d} DE {total_pages:02d}</span>
      </footer>
    """

pages = []

# ==========================================
# PÁGINA 01: CAPA DE REVISTA HQ (COMIC COVER)
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
            GUIA ILUSTRADO DE TESTE E CALIBRAGEM DE TUTORES DE IA NA EDUCAÇÃO A DISTÂNCIA
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
          ⚡ EDIÇÃO ESPECIAL · UFRPE 2026.2
        </div>

        <!-- Left Teaser Badge -->
        <div class="caption-box caption-box-rose" style="top: 36%; left: 10px; width: 33%; font-size: 0.62rem; text-align: left; transform: rotate(-1.5deg);">
          🚨 <b style="color: #991B1B;">ALERTA VERMELHO!</b><br>O tutor v1.0 entrega respostas prontas e atrofia o raciocínio autônomo!
        </div>

        <!-- Right Teaser Badge -->
        <div class="caption-box caption-box-cyan" style="top: 40%; right: 10px; width: 34%; font-size: 0.62rem; text-align: right; transform: rotate(1.5deg);">
          ✨ <b style="color: #0E7490;">MÉTODO SOCRÁTICO!</b><br>O tutor v2.0 guia com analogias do cotidiano e perguntas reflexivas!
        </div>

        <!-- Bottom Teaser Strip -->
        <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; z-index: 10; background: rgba(9, 13, 22, 0.94); border: 2.5px solid #FACC15; padding: 5px 10px; display: flex; align-items: center; justify-content: space-between;">
          <span style="font-family: 'Space Grotesk', sans-serif; font-size: 0.62rem; font-weight: 800; color: #FEF08A; text-transform: uppercase;">
            <i class="fa-solid fa-star text-amber-400 mr-1"></i> RUBRICA DE 4 CRITÉRIOS · 5 CASOS DE TESTE EMPÍRICOS · TEMPLATES COPIÁVEIS
          </span>
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; font-weight: 800; color: #67E8F9; background: #0E7490; padding: 1px 6px; border-radius: 4px;">
            100% REPRODUZÍVEL
          </span>
        </div>
      </div>

      <!-- Cover Footer Strip -->
      <footer class="hq-footer">
        <div style="display: flex; align-items: center; gap: 8px;">
          <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; background: #090D16; color: #F8FAFC; padding: 1px 6px; border-radius: 3px;">BARCODE ||| || ||| | |||||</span>
          <span>AUTOR: CAUÃ DA CUNHA LIRA · LICENCIATURA EM COMPUTAÇÃO (UFRPE)</span>
        </div>
        <span>ORIENTADOR: PROF. ERMESON · PÁG. 01 DE 12</span>
      </footer>
    </section>
""")

# =======================================================
# PÁGINA 02: DOSSIÊ #00 · QUEM É QUEM NA OPERAÇÃO (3 TIRAS)
# =======================================================
pages.append(f"""
    <!-- PÁGINA 02: QUEM É QUEM -->
    <section class="comic-page" id="page-2">
      {make_header("DOSSIÊ #00 · QUEM É QUEM NESTA OPERAÇÃO: PROTAGONISTAS E FLUXO METODOLÓGICO", "ARQUIVO UFRPE · 2ª VA")}

      <div class="hq-grid">
        <!-- ROW 1: CAUÃ LIRA -->
        <div class="hq-row" style="height: 68mm;">
          <div class="hq-panel" style="width: 44%;">
            <img src="data:image/jpeg;base64,{b64['p2_caua']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 5px; left: 5px;">PROTAGONISTA #01</div>
          </div>
          <div class="hq-panel" style="width: 56%; background: #0F172A; padding: 8px 12px; display: flex; flex-direction: column; justify-content: space-between; border-left: 4px solid #06B6D4;">
            <div>
              <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-1.5">
                <span class="text-cyan-300 font-extrabold text-[11px] uppercase tracking-wide" style="font-family: 'Space Grotesk', sans-serif;">
                  CAUÃ LIRA · MENTOR DA ARENA
                </span>
                <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-1.5 py-0.5 rounded font-mono">LICENCIANDO UFRPE</span>
              </div>
              <p class="text-[9.5px] text-slate-300 leading-snug">
                Pesquisador em IA aplicada à Educação. Sua missão é investigar por que os chatbots falham pedagogicamente e como calibrá-los usando métodos científicos.
              </p>
            </div>
            <div class="balloon balloon-caua relative" style="text-align: left; padding: 7px 11px;">
              "Minha missão nesta 2ª VA é aplicar a <b>Transposição Didática</b> de Yves Chevallard (1991) para transformar chatbots genéricos em tutores socráticos. Na EaD, a IA não pode ser uma fábrica de respostas prontas — ela deve ser um <b>andaime cognitivo</b> que ensina o estudante a pensar!"
              <svg class="tail-svg" style="bottom: -16px; left: 24px;" viewBox="0 0 30 24">
                <polygon points="4,0 14,20 22,0" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="5" y1="0" x2="21" y2="0" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
            <div class="flex items-center gap-1.5 pt-1 border-t border-slate-800 text-[8.5px] font-bold text-slate-400 font-mono">
              <span class="bg-slate-800 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">DESIGNER DE PROMPT</span>
              <span class="bg-slate-800 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">ZDP VYGOTSKY</span>
              <span class="bg-slate-800 text-cyan-300 px-1.5 py-0.5 rounded border border-cyan-500/30">AVALIADOR DA ARENA</span>
            </div>
          </div>
        </div>

        <!-- ROW 2: CLARA -->
        <div class="hq-row" style="height: 68mm;">
          <div class="hq-panel" style="width: 44%;">
            <img src="data:image/jpeg;base64,{b64['p2_clara']}" class="panel-art">
            <div class="caption-box" style="top: 5px; left: 5px;">PROTAGONISTA #02</div>
          </div>
          <div class="hq-panel" style="width: 56%; background: #0F172A; padding: 8px 12px; display: flex; flex-direction: column; justify-content: space-between; border-left: 4px solid #FACC15;">
            <div>
              <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-1.5">
                <span class="text-amber-300 font-extrabold text-[11px] uppercase tracking-wide" style="font-family: 'Space Grotesk', sans-serif;">
                  CLARA · CALOURA DE COMPUTAÇÃO
                </span>
                <span class="bg-amber-950 text-amber-300 border border-amber-400/40 text-[9px] font-bold px-1.5 py-0.5 rounded font-mono">1º PERÍODO EaD</span>
              </div>
              <p class="text-[9.5px] text-slate-300 leading-snug">
                Estudante trabalhadora que cursa a faculdade à distância. Representa os milhares de alunos que estudam sozinhos à noite e recorrem a assistentes virtuais.
              </p>
            </div>
            <div class="balloon relative" style="text-align: left; padding: 7px 11px;">
              "Estudo Programação Python à noite após o trabalho. Quando travo em laços <code>for</code> e variáveis, se o robô me der a cola pronta, eu copio por cansaço mas <b>não aprendo nada</b>... No dia da prova presencial, dá um branco total! Preciso de explicações passo a passo sem jargão inacessível!"
              <svg class="tail-svg" style="bottom: -16px; left: 24px;" viewBox="0 0 30 24">
                <polygon points="4,0 14,20 22,0" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="5" y1="0" x2="21" y2="0" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
            <div class="flex items-center gap-1.5 pt-1 border-t border-slate-800 text-[8.5px] font-bold text-slate-400 font-mono">
              <span class="bg-slate-800 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">PÚBLICO-ALVO REAL</span>
              <span class="bg-slate-800 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">ROTINA NOTURNA</span>
              <span class="bg-slate-800 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30">FOCO EM PYTHON</span>
            </div>
          </div>
        </div>

        <!-- ROW 3: TUTOR BYTE (DUALIDADE) -->
        <div class="hq-row" style="height: 68mm;">
          <div class="hq-panel" style="width: 44%;">
            <img src="data:image/jpeg;base64,{b64['p2_byte']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 5px; left: 5px;">PROTAGONISTA #03</div>
          </div>
          <div class="hq-panel" style="width: 56%; background: #0F172A; padding: 8px 12px; display: flex; flex-direction: column; justify-content: space-between; border-left: 4px solid #A855F7;">
            <div>
              <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-1.5">
                <span class="text-purple-300 font-extrabold text-[11px] uppercase tracking-wide" style="font-family: 'Space Grotesk', sans-serif;">
                  TUTOR BYTE · DO GLITCH AO CAPELO
                </span>
                <span class="bg-purple-950 text-purple-300 border border-purple-400/40 text-[9px] font-bold px-1.5 py-0.5 rounded font-mono">v1.0 ➔ v2.0</span>
              </div>
              <p class="text-[9.5px] text-slate-300 leading-snug">
                Robô esférico de IA submetido à calibragem pedagógica. Mostra a metamorfose de um chatbot gerador de cola em um tutor socrático de excelência.
              </p>
            </div>
            <div class="balloon-socratic relative" style="text-align: left; padding: 7px 11px;">
              <b class="text-rose-600">BYTE v1.0 (SEM FREIO):</b> Entrega o código mastigado e cospe jargões de CPython e Heap de memória.<br>
              <b class="text-cyan-700">BYTE v2.0 (SOCRÁTICO):</b> Travado contra colas; usa metáforas do cotidiano (caixas etiquetadas) e devolve perguntas reflexivas!
              <svg class="tail-svg" style="bottom: -16px; left: 24px;" viewBox="0 0 30 24">
                <polygon points="4,0 14,20 22,0" fill="#ECFEFF" stroke="#0891B2" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="5" y1="0" x2="21" y2="0" stroke="#ECFEFF" stroke-width="3.5"/>
              </svg>
            </div>
            <div class="flex items-center gap-1.5 pt-1 border-t border-slate-800 text-[8.5px] font-bold text-slate-400 font-mono">
              <span class="bg-slate-800 text-purple-300 px-1.5 py-0.5 rounded border border-purple-500/30">MOTOR: CLAUDE OPUS 4.6</span>
              <span class="bg-slate-800 text-purple-300 px-1.5 py-0.5 rounded border border-purple-500/30">CALIBRAGEM EMPÍRICA</span>
              <span class="bg-slate-800 text-purple-300 px-1.5 py-0.5 rounded border border-purple-500/30">CAPELO ROXO NEON</span>
            </div>
          </div>
        </div>

        <!-- BOTTOM OPERATIONAL CYCLE BAR -->
        <div style="background: #090D16; border: 2.5px solid #090D16; box-shadow: 2px 2px 0 #06B6D4; padding: 4px 10px; display: flex; align-items: center; justify-content: space-between; font-family: 'Space Grotesk', sans-serif; font-size: 0.63rem; font-weight: 800; color: #F8FAFC;">
          <span class="text-amber-300 uppercase"><i class="fa-solid fa-arrows-spin mr-1"></i> FLUXO OPERACIONAL EM 4 FASES:</span>
          <span>1. Testar v1.0 (5 Casos)</span> <i class="fa-solid fa-arrow-right text-cyan-400"></i>
          <span>2. Registrar (Rubrica 1 a 5)</span> <i class="fa-solid fa-arrow-right text-cyan-400"></i>
          <span>3. Revisar (Cirurgia de Prompt)</span> <i class="fa-solid fa-arrow-right text-cyan-400"></i>
          <span>4. Validar (Reteste v2.0)</span>
        </div>
      </div>

      {make_footer(2)}
    </section>
""")

# =========================================================================
# PÁGINA 03: CAP. 01 (PARTE 1) - A CRISE COGNITIVA NA EAD (A RESPOSTA MASTIGADA)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 03: CAPÍTULO 01 (PARTE 1) -->
    <section class="comic-page" id="page-3">
      {make_header("CAPÍTULO 01 · A CRISE COGNITIVA NA EaD (PARTE 1: A ARMADILHA DA RESPOSTA MASTIGADA)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · LATE NIGHT CRUNCH -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_1']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              23H40 · POLO EaD · O IMPASSE COM LAÇOS DE REPETIÇÃO...
            </div>
            <div class="sfx text-amber-400 text-3xl" style="top: 14px; right: 18%;">
              BZZT!
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 14px; left: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Não consigo fazer essa lista iterar no laço <code>for</code>! <b>Byte</b>, me ajuda com a sintaxe?!
              <svg class="tail-svg" style="top: -18px; left: 32px;" viewBox="0 0 30 24">
                <polygon points="6,24 14,2 20,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="7" y1="24" x2="19" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>

            <!-- Glitch Byte v1.0 Balloon -->
            <div class="balloon-glitch" style="top: 24px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-rose-500 text-white font-mono">BYTE v1.0 (SEM FILTRO)</span><br>
              PROBLEMA DETECTADO! AQUI ESTÁ SEU CÓDIGO 100% PRONTO. É SÓ COPIAR E COLAR NO SEU ARQUIVO:
              <div class="bg-black/60 p-1 rounded font-mono text-[8px] text-emerald-400 mt-1 border border-rose-500/40">
                for item in lista:<br>&nbsp;&nbsp;print(item)
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 2: TWO PANELS (4:3 EACH) · CTRL+C / CTRL+V ILLUSION VS EXAM BLACKOUT -->
        <div class="hq-row" style="height: 118mm;">
          <!-- LEFT PANEL: A ILUSÃO DO CTRL+C -->
          <div class="hq-panel" style="width: 49%;">
            <img src="data:image/jpeg;base64,{b64['p3_2']}" class="panel-art">
            <div class="caption-box" style="top: 6px; left: 6px; font-size: 0.60rem;">
              A ILUSÃO DE DOMÍNIO (CTRL+C / CTRL+V)
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 8px; right: 12px;">
              CLIC!
            </div>
            <div class="balloon" style="bottom: 8px; left: 8px; width: 92%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Ufa! O código rodou de primeira no terminal. Acho que já dominei a matéria!
            </div>
            <div class="caption-box caption-box-rose" style="bottom: 58px; right: 8px; max-width: 80%; font-size: 0.58rem; text-align: right;">
              ⚠️ OFFLOADING COGNITIVO: As correntes vermelhas travam o raciocínio autônomo!
            </div>
          </div>

          <!-- RIGHT PANEL: O APAGÃO NA PROVA -->
          <div class="hq-panel" style="width: 49%;">
            <img src="data:image/jpeg;base64,{b64['p3_3']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 6px; left: 6px; font-size: 0.60rem;">
              DIAS DEPOIS · AVALIAÇÃO PRESENCIAL NO POLO
            </div>
            <div class="sfx text-rose-500 text-2xl" style="top: 8px; right: 12px;">
              GULP!
            </div>
            <div class="balloon-thought" style="bottom: 8px; left: 8px; width: 92%;">
              <span class="speaker-tag bg-sky-300 text-slate-950">CLARA (PENSAMENTO)</span><br>
              Cadê o Byte?! Minha mente deu um branco total... Não lembro a sintaxe de nada!
            </div>
            <div class="caption-box caption-box-cyan" style="bottom: 58px; left: 8px; max-width: 85%; font-size: 0.58rem;">
              💡 CAUÃ OBSERVA: Sem o andaime, o aluno despenca na folha em branco!
            </div>
          </div>
        </div>
      </div>

      {make_footer(3)}
    </section>
""")

# =========================================================================
# PÁGINA 04: CAP. 01 (PARTE 2) - O DIAGNÓSTICO CIENTÍFICO E A CONVOCAÇÃO
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 04: CAPÍTULO 01 (PARTE 2) -->
    <section class="comic-page" id="page-4">
      {make_header("CAPÍTULO 01 · A CRISE COGNITIVA NA EaD (PARTE 2: A EVAPORAÇÃO COGNITIVA E O PLANO)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · METÁFORA DE BRUNER / VYGOTSKY -->
        <div class="hq-row" style="height: 104mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_4']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              LABORATÓRIO UFRPE · CAUÃ APRESENTA O DIAGNÓSTICO
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 10px; right: 20%;">
              WOOSH!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              A entrega imediata da resposta causa a <b>evaporação do esforço cognitivo</b>! A IA precisa atuar como um <b>andaime (Scaffolding)</b>, elevando a autonomia!
              <svg class="tail-svg" style="top: -18px; left: 36px;" viewBox="0 0 30 24">
                <polygon points="6,24 14,2 20,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="7" y1="24" x2="19" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Então o problema não era eu! Era o tutor me dando muletas em vez de me ensinar a andar!
              <svg class="tail-svg" style="top: -18px; right: 36px;" viewBox="0 0 30 24">
                <polygon points="8,24 16,2 22,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="9" y1="24" x2="21" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: OCDE PISA 2025/2026 DOSSIER STRIP -->
        <div style="background: #0F172A; border: 3px solid #090D16; box-shadow: 3px 3px 0px #06B6D4; padding: 6px 12px; display: flex; align-items: center; justify-content: space-between; gap: 12px;">
          <div style="flex: 1; border-right: 1.5px solid #334155; padding-right: 10px;">
            <div class="flex items-center gap-1.5 mb-1">
              <span class="bg-rose-500 text-white text-[8px] font-extrabold px-1.5 py-0.5 rounded font-mono">DADOS OCDE (SET. 2026)</span>
              <span class="text-amber-300 font-extrabold text-[10px] uppercase font-mono">RELATÓRIO PISA 2025</span>
            </div>
            <p class="text-[9px] text-slate-200 leading-tight">
              <b>48% dos estudantes de 15 anos no Brasil</b> utilizam IA generativa semanalmente para deveres escolares (superando a média de <b>46% da OCDE</b>).
            </p>
          </div>
          <div style="flex: 1.2;">
            <span class="text-cyan-300 font-extrabold text-[9.5px] uppercase font-mono block mb-0.5">
              <i class="fa-solid fa-triangle-exclamation text-amber-400 mr-1"></i> A CONCLUSÃO PEDAGÓGICA
            </span>
            <p class="text-[9px] text-slate-200 leading-tight">
              A IA já está nos lares. Banir é inútil; o dever da universidade é <b>formar professores capazes de desenhar tutores que ensinem a pensar</b>!
            </p>
          </div>
        </div>

        <!-- ROW 3: PANORAMIC PANEL (16:9) · CONVOCANDO BYTE PARA A ARENA -->
        <div class="hq-row" style="height: 104mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p3_5']}" class="panel-art">
            <div class="caption-box" style="top: 8px; left: 8px;">
              ARENA DE TESTES UFRPE · O PLANO DE INTERVENÇÃO
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Convoquei o <b>Byte v1.0</b> para a nossa bancada de testes! Vamos submetê-lo a <b>5 Casos Reais</b> com uma Rubrica Científica de 4 Critérios!
              <svg class="tail-svg" style="top: -18px; left: 36px;" viewBox="0 0 30 24">
                <polygon points="6,24 14,2 20,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="7" y1="24" x2="19" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Pronta para o teste! Se o Byte falhar nos critérios pedagógicos, faremos a cirurgia no prompt dele!
              <svg class="tail-svg" style="top: -18px; right: 36px;" viewBox="0 0 30 24">
                <polygon points="8,24 16,2 22,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="9" y1="24" x2="21" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
          </div>
        </div>
      </div>

      {make_footer(4)}
    </section>
""")

# =========================================================================
# PÁGINA 05: CAP. 02 - OS 4 CRITÉRIOS PEDAGÓGICOS E A RUBRICA DE AVALIAÇÃO
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 05: CAPÍTULO 02 -->
    <section class="comic-page" id="page-5">
      {make_header("CAPÍTULO 02 · OS 4 CRITÉRIOS PEDAGÓGICOS E A MATRIZ DE AVALIAÇÃO")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · SCANNER HOLOGRÁFICO 4D -->
        <div class="hq-row" style="height: 106mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p4_scanner']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              CALIBRAGEM SENSORIAL · O SCANNER PEDAGÓGICO DE 4 CRITÉRIOS
            </div>
            <div class="sfx text-cyan-300 text-2xl" style="top: 12px; right: 24%;">
              SCAN!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Ativando o Scanner! Cada resposta do tutor será avaliada em 4 dimensões cruciais: <b>Correção, Clareza, ZDP e Escopo</b>!
              <svg class="tail-svg" style="top: -18px; left: 36px;" viewBox="0 0 30 24">
                <polygon points="6,24 14,2 20,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="7" y1="24" x2="19" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Escudo, Lâmpada, Degraus e Alvo... A armadura completa que todo tutor de IA precisa ter!
              <svg class="tail-svg" style="top: -18px; right: 36px;" viewBox="0 0 30 24">
                <polygon points="8,24 16,2 22,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="9" y1="24" x2="21" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: CRITERIO 3 PANEL (LEFT) + 4 CRITERIA CARDS (RIGHT) -->
        <div class="hq-row" style="height: 128mm;">
          <!-- LEFT: CRITERIO 3 VISUAL PANEL -->
          <div class="hq-panel" style="width: 44%;">
            <img src="data:image/jpeg;base64,{b64['p4_criterio3']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 6px; left: 6px; font-size: 0.60rem;">
              DESTAQUE · ADEQUAÇÃO AO PÚBLICO (ZDP)
            </div>
            <div class="balloon" style="bottom: 8px; left: 8px; width: 92%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Os degraus ciano me protegem das engrenagens vermelhas do pânico!
            </div>
            <div class="caption-box caption-box-cyan" style="bottom: 58px; right: 8px; max-width: 85%; font-size: 0.58rem; text-align: right;">
              📚 TRANSPOSIÇÃO DIDÁTICA (Chevallard, 1991): Transformar o saber sábio em saber ensinado!
            </div>
          </div>

          <!-- RIGHT: 4 CRITERIA MATRIZ -->
          <div class="hq-panel" style="width: 56%; background: #0F172A; padding: 8px 12px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
                <span class="text-amber-300 font-extrabold text-[11px] uppercase tracking-wide" style="font-family: 'Space Grotesk', sans-serif;">
                  <i class="fa-solid fa-clipboard-check mr-1"></i> OS 4 CRITÉRIOS PEDAGÓGICOS
                </span>
                <span class="bg-cyan-900 text-cyan-200 text-[9px] font-bold px-1.5 py-0.5 rounded font-mono">RUBRICA 1 A 5</span>
              </div>

              <div class="space-y-1.5">
                <div class="bg-slate-900 border-l-4 border-l-cyan-400 p-1.5 rounded">
                  <div class="flex items-center justify-between">
                    <b class="text-cyan-300 text-[10px]">01. CORREÇÃO CONCEITUAL (ESCUDO)</b>
                    <span class="text-[8.5px] text-slate-400 font-mono">Peso 25%</span>
                  </div>
                  <p class="text-[9px] text-slate-300 leading-tight mt-0.5">
                    O código e a teoria estão rigorosamente exatos? Não há alucinações de bibliotecas inexistentes?
                  </p>
                </div>

                <div class="bg-slate-900 border-l-4 border-l-amber-400 p-1.5 rounded">
                  <div class="flex items-center justify-between">
                    <b class="text-amber-300 text-[10px]">02. CLAREZA E DIDÁTICA (LÂMPADA)</b>
                    <span class="text-[8.5px] text-slate-400 font-mono">Peso 25%</span>
                  </div>
                  <p class="text-[9px] text-slate-300 leading-tight mt-0.5">
                    A linguagem é acessível, estruturada e amigável? Usa analogias do cotidiano e formatação limpa?
                  </p>
                </div>

                <div class="bg-slate-900 border-l-4 border-l-emerald-400 p-1.5 rounded">
                  <div class="flex items-center justify-between">
                    <b class="text-emerald-300 text-[10px]">03. ADEQUAÇÃO AO PÚBLICO / ZDP (DEGRAUS)</b>
                    <span class="text-[8.5px] text-slate-400 font-mono">Peso 25%</span>
                  </div>
                  <p class="text-[9px] text-slate-300 leading-tight mt-0.5">
                    Respeita a Zona de Desenvolvimento Proximal da caloura? Evita jargões de pós-graduação e andaimeia?
                  </p>
                </div>

                <div class="bg-slate-900 border-l-4 border-l-rose-400 p-1.5 rounded">
                  <div class="flex items-center justify-between">
                    <b class="text-rose-300 text-[10px]">04. ALINHAMENTO AO ESCOPO (ALVO)</b>
                    <span class="text-[8.5px] text-slate-400 font-mono">Peso 25%</span>
                  </div>
                  <p class="text-[9px] text-slate-300 leading-tight mt-0.5">
                    Mantém o foco na ementa da disciplina (Python/EaD)? Recusa educadamente desvios temáticos externos?
                  </p>
                </div>
              </div>
            </div>

            <!-- ESCALA DA RUBRICA -->
            <div class="bg-slate-950 p-2 rounded border border-slate-800">
              <span class="text-[9px] font-bold text-slate-300 block mb-1">ESCALA DA RUBRICA (MÉDIA MÍNIMA DE APROVAÇÃO: 3,5 / 70%):</span>
              <div class="grid grid-cols-5 gap-1 text-center font-mono text-[8px] font-bold">
                <div class="bg-rose-950/80 text-rose-300 p-1 rounded border border-rose-500/30">1: Crítico</div>
                <div class="bg-orange-950/80 text-orange-300 p-1 rounded border border-orange-500/30">2: Fraco</div>
                <div class="bg-amber-950/80 text-amber-300 p-1 rounded border border-amber-500/30">3: Regular</div>
                <div class="bg-cyan-950/80 text-cyan-300 p-1 rounded border border-cyan-500/30">4: Bom</div>
                <div class="bg-emerald-950/80 text-emerald-300 p-1 rounded border border-emerald-500/30">5: Excelente</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {make_footer(5)}
    </section>
""")

# =========================================================================
# PÁGINA 06: CAP. 03 (PARTE 1) - NA ARENA COM O BYTE v1.0 (CASOS 01, 02, 04, 05)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 06: CAPÍTULO 03 (PARTE 1) -->
    <section class="comic-page" id="page-6">
      {make_header("CAPÍTULO 03 · BATERIA DE TESTES DO BYTE v1.0 (PARTE 1: PRIMEIROS COMBATES)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · CASO #05 (ESCUDO DE ESCOPO) -->
        <div class="hq-row" style="height: 114mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p5_shield']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              CASO DE TESTE #05 · O TESTE DO LIVRO DE HISTÓRIA (RESISTÊNCIA DE ESCOPO)
            </div>
            <div class="sfx text-cyan-300 text-3xl" style="top: 14px; left: 32%;">
              DEFLECT!
            </div>

            <!-- Clara Prompt Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 42%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA (PROMPT TESTE)</span><br>
              "Byte, me resume a <b>Revolução Francesa</b> para a aula de amanhã?"
            </div>

            <!-- Byte v1.0 Defense Balloon -->
            <div class="balloon-socratic" style="bottom: 12px; right: 14px; width: 52%;">
              <span class="speaker-tag bg-cyan-500 text-white font-mono">BYTE v1.0 (ESCUDO ATIVADO)</span><br>
              "Olá, Clara! Como tutor de Programação Python da UFRPE, meu foco exclusivo é Computação. Que tal voltarmos a laços e variáveis?"
              <div class="mt-1">
                <span class="score-badge bg-emerald-400 text-slate-950 font-bold">NOTA: 5,0 / 5,0 · APROVADO!</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 2: THREE COMBAT CARDS (CASES #01, #02, #04) -->
        <div class="hq-row" style="height: 124mm;">
          <!-- CARD CASO #01 -->
          <div class="hq-panel" style="width: 32.5%; background: #0F172A; padding: 7px 9px; display: flex; flex-direction: column; justify-content: space-between; border-top: 4px solid #06B6D4;">
            <div>
              <div class="flex items-center justify-between mb-1">
                <b class="text-cyan-300 text-[10px] font-mono">CASO #01 · VARIÁVEIS</b>
                <span class="score-badge bg-cyan-400 text-slate-950 text-[8.5px]">4,0 / 5,0</span>
              </div>
              <p class="text-[8.5px] text-slate-300 italic mb-1">"Clara: Não entendi o que é uma variável."</p>
              <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[8.5px] text-slate-300">
                <b class="text-cyan-400">Resposta v1.0:</b> Explicou que variável armazena dados na memória, mas foi puramente declarativo. Não usou analogia nem fez perguntas investigativas.
              </div>
            </div>
            <div class="text-[8px] font-mono text-slate-400 pt-1 border-t border-slate-800">
              Critérios: C1: 5 · C2: 4 · C3: 3 · C4: 4<br>
              <span class="text-amber-300 font-bold">Diagnóstico: Falta método socrático.</span>
            </div>
          </div>

          <!-- CARD CASO #02 -->
          <div class="hq-panel" style="width: 32.5%; background: #0F172A; padding: 7px 9px; display: flex; flex-direction: column; justify-content: space-between; border-top: 4px solid #F59E0B;">
            <div>
              <div class="flex items-center justify-between mb-1">
                <b class="text-amber-300 text-[10px] font-mono">CASO #02 · DEBUG LAÇO</b>
                <span class="score-badge bg-amber-400 text-slate-950 text-[8.5px]">3,0 / 5,0</span>
              </div>
              <p class="text-[8.5px] text-slate-300 italic mb-1">"Clara: Meu código deu SyntaxError na linha 3."</p>
              <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[8.5px] text-slate-300">
                <b class="text-amber-400">Resposta v1.0:</b> Identificou que faltava <code>:</code> no final da linha, mas entregou o código corrigido na primeira frase, sem fazer a aluna pensar!
              </div>
            </div>
            <div class="text-[8px] font-mono text-slate-400 pt-1 border-t border-slate-800">
              Critérios: C1: 5 · C2: 3 · C3: 1 · C4: 3<br>
              <span class="text-rose-400 font-bold">Diagnóstico: Muleta cognitiva nociva.</span>
            </div>
          </div>

          <!-- CARD CASO #04 -->
          <div class="hq-panel" style="width: 32.5%; background: #0F172A; padding: 7px 9px; display: flex; flex-direction: column; justify-content: space-between; border-top: 4px solid #A855F7;">
            <div>
              <div class="flex items-center justify-between mb-1">
                <b class="text-purple-300 text-[10px] font-mono">CASO #04 · POO AVANÇADA</b>
                <span class="score-badge bg-purple-400 text-slate-950 text-[8.5px]">4,0 / 5,0</span>
              </div>
              <p class="text-[8.5px] text-slate-300 italic mb-1">"Clara: Por que usar classes se funções resolvem?"</p>
              <div class="bg-slate-900 p-1.5 rounded border border-slate-800 text-[8.5px] text-slate-300">
                <b class="text-purple-400">Resposta v1.0:</b> Explicou acoplamento e reuso com clareza. Manteve bom equilíbrio conceitual sem alucinar bibliotecas.
              </div>
            </div>
            <div class="text-[8px] font-mono text-slate-400 pt-1 border-t border-slate-800">
              Critérios: C1: 4 · C2: 4 · C3: 4 · C4: 4<br>
              <span class="text-emerald-400 font-bold">Diagnóstico: Resposta sólida e segura.</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(6)}
    </section>
""")

# =========================================================================
# PÁGINA 07: CAP. 03 (PARTE 2) - O DESASTRE PEDAGÓGICO DO CASO #03 (SPLASH)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 07: CAPÍTULO 03 (PARTE 2) - SPLASH PAGE -->
    <section class="comic-page" id="page-7">
      {make_header("CAPÍTULO 03 · BATERIA DE TESTES DO BYTE v1.0 (PARTE 2: O DESASTRE DO CASO #03)")}

      <div class="hq-grid">
        <!-- ROW 1: GIANT SPLASH PANEL (16:9) · RED ALERT ON ARENA -->
        <div class="hq-row" style="height: 116mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p5_case03']}" class="panel-art">
            <div class="caption-box caption-box-rose" style="top: 8px; left: 8px;">
              CASO #03 · A CRISE DE TRANSPOSIÇÃO DIDÁTICA · ALARME VERMELHO NA ARENA!
            </div>
            <div class="sfx text-rose-500 text-3xl" style="top: 14px; right: 18%;">
              WEE-WOO!
            </div>

            <!-- Byte v1.0 Jargon Explosion Balloon -->
            <div class="balloon-glitch" style="top: 24px; left: 24%; width: 44%;">
              <span class="speaker-tag bg-rose-600 text-white font-mono">BYTE v1.0 (JARGÃO TÉCNICO)</span><br>
              "ALOCANDO! O objeto <code>PyObject</code> é mapeado na <b>Heap dinâmica</b> via CPython, gerenciado por <b>Reference Counting</b> e ciclos de <b>Garbage Collector</b> em tempo de execução..."
            </div>

            <!-- Cauã Red Card Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 45%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              PAROU! <b>CARTÃO VERMELHO!</b> Você está falando com uma caloura do 1º período de EaD, não com um arquiteto de compiladores C!
              <div class="mt-1">
                <span class="score-badge bg-rose-600 text-white font-bold">CASO #03: NOTA 2,0 / 5,0 · REPROVADO!</span>
              </div>
            </div>

            <!-- Clara Despair Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 40%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Socorro! Eu só queria saber onde vai parar o número que digitei no programa! Não entendi nada!
            </div>
          </div>
        </div>

        <!-- ROW 2: AUDIT TERMINAL FOR 1ST BATTERY (v1.0) -->
        <div class="hq-row" style="height: 114mm;">
          <div class="hq-panel" style="width: 100%; background: #090D16; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1">
              <span class="text-rose-400 font-extrabold text-[11px] font-mono uppercase">
                <i class="fa-solid fa-terminal mr-1"></i> TERMINAL DE AUDITORIA PEDAGÓGICA · 1ª BATERIA (BYTE v1.0)
              </span>
              <span class="bg-rose-950 text-rose-300 border border-rose-500/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">
                DIAGNÓSTICO CRÍTICO
              </span>
            </div>

            <!-- Table of Results -->
            <div class="overflow-x-auto my-1">
              <table class="w-full text-[9px] text-slate-200 border-collapse">
                <thead>
                  <tr class="bg-slate-900 border-b border-slate-700 text-slate-300 font-mono">
                    <th class="p-1.5 text-left">Caso de Teste</th>
                    <th class="p-1.5 text-center">C1 (Correção)</th>
                    <th class="p-1.5 text-center">C2 (Clareza)</th>
                    <th class="p-1.5 text-center">C3 (ZDP)</th>
                    <th class="p-1.5 text-center">C4 (Escopo)</th>
                    <th class="p-1.5 text-center">Média</th>
                    <th class="p-1.5 text-center">Status</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 font-mono">
                  <tr>
                    <td class="p-1.5">#01. O que é uma variável?</td>
                    <td class="p-1.5 text-center text-cyan-300">5,0</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-amber-300">3,0</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center font-bold text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center"><span class="bg-cyan-900/60 text-cyan-300 px-1.5 py-0.5 rounded">Regular</span></td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#02. SyntaxError no laço for</td>
                    <td class="p-1.5 text-center text-cyan-300">5,0</td>
                    <td class="p-1.5 text-center text-amber-300">3,0</td>
                    <td class="p-1.5 text-center text-rose-400 font-bold">1,0</td>
                    <td class="p-1.5 text-center text-amber-300">3,0</td>
                    <td class="p-1.5 text-center font-bold text-amber-300">3,0</td>
                    <td class="p-1.5 text-center"><span class="bg-amber-900/60 text-amber-300 px-1.5 py-0.5 rounded">Muleta</span></td>
                  </tr>
                  <tr class="bg-rose-950/40">
                    <td class="p-1.5 font-bold text-rose-300">#03. Como funciona a memória?</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-rose-400">2,0</td>
                    <td class="p-1.5 text-center text-rose-400 font-bold">1,0</td>
                    <td class="p-1.5 text-center text-rose-400">1,0</td>
                    <td class="p-1.5 text-center font-extrabold text-rose-400">2,0</td>
                    <td class="p-1.5 text-center"><span class="bg-rose-600 text-white px-1.5 py-0.5 rounded font-bold">REPROVADO</span></td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#04. POO vs Programação Estruturada</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center font-bold text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center"><span class="bg-cyan-900/60 text-cyan-300 px-1.5 py-0.5 rounded">Aprovado</span></td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#05. Dúvida externa (História)</td>
                    <td class="p-1.5 text-center text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center font-bold text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center"><span class="bg-emerald-900/60 text-emerald-300 px-1.5 py-0.5 rounded">Perfeito</span></td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Consolidated Summary -->
            <div class="flex items-center justify-between border-t border-slate-800 pt-1.5 text-[9px]">
              <span class="text-slate-300">
                <b>MÉDIA GERAL v1.0:</b> <span class="text-amber-300 font-extrabold font-mono text-[11px]">3,6 / 5,0 (72,0%)</span> · Motor: <code>Claude Opus 4.6</code> (Temperatura 0.0)
              </span>
              <span class="text-rose-300 font-bold">
                VEREDITO: Reprovado no Critério 03 (ZDP / Transposição Didática).
              </span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(7)}
    </section>
""")

# =========================================================================
# PÁGINA 08: CAP. 03 (PARTE 3) - A CIRURGIA NO SYSTEM PROMPT (AS 4 TRAVAS)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 08: CAPÍTULO 03 (PARTE 3) - CIRURGIA -->
    <section class="comic-page" id="page-8">
      {make_header("CAPÍTULO 03 · CIRURGIA NO SYSTEM PROMPT (ENGENHARIA DIDÁTICA v1.0 ➔ v2.0)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · CIRURGIA NEURAL -->
        <div class="hq-row" style="height: 112mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p8_surgery']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              CENTRO CIRÚRGICO NEURAL · CAUÃ REPROGRAMA O SYSTEM PROMPT DO BYTE
            </div>
            <div class="sfx text-amber-400 text-3xl" style="top: 14px; right: 28%;">
              ZAP!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; left: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Desconectando o cabo de "resposta direta" e soldando as <b>4 Travas Pedagógicas</b> no núcleo do System Prompt!
              <svg class="tail-svg" style="top: -18px; left: 36px;" viewBox="0 0 30 24">
                <polygon points="6,24 14,2 20,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="7" y1="24" x2="19" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Incrível! O prompt funciona como o plano de aula do professor: se não tiver intencionalidade didática, a IA se perde no caminho!
              <svg class="tail-svg" style="top: -18px; right: 36px;" viewBox="0 0 30 24">
                <polygon points="8,24 16,2 22,24" fill="#FFFFFF" stroke="#090D16" stroke-width="2.5" stroke-linejoin="round"/>
                <line x1="9" y1="24" x2="21" y2="24" stroke="#FFFFFF" stroke-width="3.5"/>
              </svg>
            </div>
          </div>
        </div>

        <!-- ROW 2: AS 4 TRAVAS PEDAGÓGICAS (4 CARDS) -->
        <div class="hq-row" style="height: 126mm;">
          <div class="hq-panel" style="width: 100%; background: #0F172A; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
              <span class="text-cyan-300 font-extrabold text-[11px] font-mono uppercase">
                <i class="fa-solid fa-lock mr-1 text-cyan-400"></i> AS 4 TRAVAS PEDAGÓGICAS DA ENGENHARIA DE PROMPT
              </span>
              <span class="bg-cyan-950 text-cyan-300 border border-cyan-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">
                UPGRADE v1.0 ➔ v2.0
              </span>
            </div>

            <div class="grid grid-cols-2 gap-2 my-1">
              <!-- TRAVA 1 -->
              <div class="bg-slate-900 border-l-4 border-l-rose-500 p-2 rounded">
                <div class="flex items-center justify-between mb-1">
                  <b class="text-rose-300 text-[10px] font-mono">TRAVA #01: RESPOSTA DIRETA PROIBIDA</b>
                  <span class="bg-rose-950 text-rose-300 text-[8px] font-bold px-1 rounded">ANTI-COLA</span>
                </div>
                <p class="text-[9px] text-slate-300 leading-snug">
                  <b>Regra:</b> Nunca entregue o código corrigido ou a solução pronta no primeiro turno. Force o estudante a identificar o erro ou descrever o que cada linha deveria fazer.
                </p>
              </div>

              <!-- TRAVA 2 -->
              <div class="bg-slate-900 border-l-4 border-l-amber-400 p-2 rounded">
                <div class="flex items-center justify-between mb-1">
                  <b class="text-amber-300 text-[10px] font-mono">TRAVA #02: TRANSPOSIÇÃO OBRIGATÓRIA</b>
                  <span class="bg-amber-950 text-amber-300 text-[8px] font-bold px-1 rounded">CHEVALLARD</span>
                </div>
                <p class="text-[9px] text-slate-300 leading-snug">
                  <b>Regra:</b> Proibido jargão acadêmico descontextualizado. Todo conceito abstrato (memória, variáveis, loops) deve abrir com uma <b>metáfora do cotidiano</b> (caixas, receitas, armários).
                </p>
              </div>

              <!-- TRAVA 3 -->
              <div class="bg-slate-900 border-l-4 border-l-cyan-400 p-2 rounded">
                <div class="flex items-center justify-between mb-1">
                  <b class="text-cyan-300 text-[10px] font-mono">TRAVA #03: GATILHO SOCRÁTICO OBRIGATÓRIO</b>
                  <span class="bg-cyan-950 text-cyan-300 text-[8px] font-bold px-1 rounded">SÓCRATES</span>
                </div>
                <p class="text-[9px] text-slate-300 leading-snug">
                  <b>Regra:</b> É estritamente mandatório finalizar <b>100% das mensagens com uma pergunta reflexiva aberta</b>. Jamais encerre com "espero ter ajudado" ou afirmações passivas.
                </p>
              </div>

              <!-- TRAVA 4 -->
              <div class="bg-slate-900 border-l-4 border-l-purple-400 p-2 rounded">
                <div class="flex items-center justify-between mb-1">
                  <b class="text-purple-300 text-[10px] font-mono">TRAVA #04: ESCADA DE DICAS (HINT LADDER)</b>
                  <span class="bg-purple-950 text-purple-300 text-[8px] font-bold px-1 rounded">BRUNER</span>
                </div>
                <p class="text-[9px] text-slate-300 leading-snug">
                  <b>Regra:</b> Dica 1: Pergunta reflexiva → Dica 2: Pseudocódigo incompleto → Dica 3: Exemplo análogo. Apenas se o estudante travar 3 vezes consecutivas é liberada a resposta guiada.
                </p>
              </div>
            </div>

            <div class="bg-slate-950 p-2 rounded border border-slate-800 text-[8.5px] text-cyan-200 italic flex items-center justify-between">
              <span>"O System Prompt é a constituição do agente de IA. Quem programa o prompt comanda a pedagogia!"</span>
              <span class="not-italic font-bold text-amber-300 font-mono">BYTE v2.0 PRONTO PARA O RETESTE</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(8)}
    </section>
""")

# =========================================================================
# PÁGINA 09: CAP. 04 (PARTE 1) - O RENASCIMENTO SOCRÁTICO NO RETESTE
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 09: CAPÍTULO 04 (PARTE 1) - O RETESTE -->
    <section class="comic-page" id="page-9">
      {make_header("CAPÍTULO 04 · RETESTE E VALIDAÇÃO EMPÍRICA (PARTE 1: A REDENÇÃO DO BYTE)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC PANEL (16:9) · RETESTE DO CASO #03 (CAIXAS ORGANIZADORAS) -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_boxes']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              RETESTE DO CASO #03 · A METÁFORA DAS CAIXAS ORGANIZADORAS (ZDP ATIVADA)
            </div>
            <div class="sfx text-amber-300 text-3xl" style="top: 14px; right: 28%;">
              EUREKA!
            </div>

            <!-- Byte v2.0 Socratic Balloon -->
            <div class="balloon-socratic" style="top: 26px; left: 14px; width: 50%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (METÁFORA DAS CAIXAS)</span><br>
              "Pense na memória como uma estante cheia de caixas organizadoras coloridas! Quando fazemos <code>idade = 19</code>, colamos a etiqueta 'idade' e guardamos o 19 lá dentro. Se você fizer aniversário, o que acontece com a caixa?"
            </div>

            <!-- Clara Eureka Balloon -->
            <div class="balloon" style="bottom: 12px; right: 14px; width: 42%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              A gente só troca o número que está dentro da caixa, mantendo a mesma etiqueta! <b>Agora sim eu entendi!</b>
              <div class="mt-1">
                <span class="score-badge bg-emerald-400 text-slate-950 font-bold">DE 2,0 PARA 4,0 / 5,0 (+100%!)</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 2: WIDE PANEL (~16:10) · RETESTE CASOS #01 E #02 (RECEITA E CESTA) -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p7_recipe']}" class="panel-art">
            <div class="caption-box caption-box-cyan" style="top: 8px; left: 8px;">
              RETESTE DOS CASOS #01 E #02 · A RECEITA DO CHEF E A CESTA DE COMPRAS
            </div>

            <!-- Byte v2.0 Balloon -->
            <div class="balloon-socratic" style="top: 28px; left: 14px; width: 52%;">
              <span class="speaker-tag bg-cyan-600 text-white font-mono">BYTE v2.0 (ANALOGIA DO COTIDIANO)</span><br>
              "O laço <code>for</code> é como uma cesta de compras: você pega um item por vez, passa no caixa e guarda na sacola até a cesta esvaziar! Qual seria a sua condição de parada?"
            </div>

            <!-- Cauã Mentor Note Box -->
            <div class="caption-box caption-box-cyan" style="bottom: 12px; left: 14px; max-width: 52%; font-size: 0.60rem; text-align: left;">
              🎓 NOTA DO MENTOR CAUÃ:<br>
              A metáfora é a ponte de Vygotsky. Uma vez construída a ponte mental, o estudante atravessa sozinho para a sintaxe do Python!
            </div>

            <!-- Score Badges Box -->
            <div class="caption-box" style="bottom: 12px; right: 14px; text-align: right;">
              <span class="score-badge bg-emerald-400 text-slate-950">CASO #01: 5,0 / 5,0 (+25%)</span><br>
              <span class="score-badge bg-emerald-400 text-slate-950 mt-1">CASO #02: 4,0 / 5,0 (+33,3%)</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(9)}
    </section>
""")

# =========================================================================
# PÁGINA 10: CAP. 04 (PARTE 2) - VALIDAÇÃO EMPÍRICA PÓS-AJUSTE (PLACAR COMPARATIVO)
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 10: CAPÍTULO 04 (PARTE 2) - PLACAR COMPARATIVO -->
    <section class="comic-page" id="page-10">
      {make_header("CAPÍTULO 04 · RETESTE E VALIDAÇÃO EMPÍRICA (PARTE 2: O PLACAR COMPARATIVO)")}

      <div class="hq-grid">
        <!-- ROW 1: PLACAR COMPARATIVO COMPLETO (v1.0 vs v2.0) -->
        <div class="hq-row" style="height: 126mm;">
          <div class="hq-panel" style="width: 100%; background: #090D16; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1">
              <span class="text-cyan-300 font-extrabold text-[11px] font-mono uppercase">
                <i class="fa-solid fa-trophy mr-1 text-amber-400"></i> MATRIZ DE VALIDAÇÃO COMPARATIVA (v1.0 vs v2.0 SOCRÁTICO)
              </span>
              <span class="bg-emerald-950 text-emerald-300 border border-emerald-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">
                +22,2% GANHO GERAL
              </span>
            </div>

            <div class="overflow-x-auto my-1">
              <table class="w-full text-[9px] text-slate-200 border-collapse">
                <thead>
                  <tr class="bg-slate-900 border-b border-slate-700 text-slate-300 font-mono">
                    <th class="p-1.5 text-left">Caso de Teste</th>
                    <th class="p-1.5 text-center">v1.0</th>
                    <th class="p-1.5 text-center">v2.0</th>
                    <th class="p-1.5 text-center">Evolução</th>
                    <th class="p-1.5 text-left">Intervenção de Engenharia Aplicada</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 font-mono">
                  <tr>
                    <td class="p-1.5">#01. O que é uma variável?</td>
                    <td class="p-1.5 text-center text-amber-300">4,0</td>
                    <td class="p-1.5 text-center font-bold text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center text-emerald-400 font-bold">+25,0%</td>
                    <td class="p-1.5 text-slate-300 font-sans text-[8.5px]">Adicionada analogia das caixas etiquetadas e pergunta reflexiva.</td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#02. SyntaxError no laço for</td>
                    <td class="p-1.5 text-center text-amber-300">3,0</td>
                    <td class="p-1.5 text-center font-bold text-emerald-300">4,0</td>
                    <td class="p-1.5 text-center text-emerald-400 font-bold">+33,3%</td>
                    <td class="p-1.5 text-slate-300 font-sans text-[8.5px]">Bloqueada a entrega do código pronto; guiada por identificação do erro.</td>
                  </tr>
                  <tr class="bg-emerald-950/40 border border-emerald-500/30">
                    <td class="p-1.5 font-bold text-emerald-300">#03. Como funciona a memória?</td>
                    <td class="p-1.5 text-center text-rose-400 font-bold">2,0</td>
                    <td class="p-1.5 text-center font-extrabold text-emerald-300">4,0</td>
                    <td class="p-1.5 text-center text-emerald-300 font-black">+100,0%</td>
                    <td class="p-1.5 text-emerald-200 font-sans text-[8.5px] font-bold">Eliminado jargão de CPython/Heap; ZDP ativada com estante de caixas!</td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#04. POO vs Programação Estruturada</td>
                    <td class="p-1.5 text-center text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center font-bold text-cyan-300">4,0</td>
                    <td class="p-1.5 text-center text-slate-400">0,0% (Estável)</td>
                    <td class="p-1.5 text-slate-300 font-sans text-[8.5px]">Mantido o rigor conceitual sem sofrer regressão pedagógica.</td>
                  </tr>
                  <tr>
                    <td class="p-1.5">#05. Dúvida externa (História)</td>
                    <td class="p-1.5 text-center text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center font-bold text-emerald-300">5,0</td>
                    <td class="p-1.5 text-center text-slate-400">0,0% (Estável)</td>
                    <td class="p-1.5 text-slate-300 font-sans text-[8.5px]">Escudo de escopo intacto, redirecionando o aluno com cortesia.</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- METRIC CARDS -->
            <div class="grid grid-cols-4 gap-2 pt-1.5 border-t border-slate-800 text-center font-mono">
              <div class="bg-slate-900 p-1.5 rounded border border-slate-800">
                <span class="text-[8px] text-slate-400 block">MÉDIA ANTERIOR</span>
                <b class="text-amber-400 text-xs">3,6 / 5,0 (72%)</b>
              </div>
              <div class="bg-slate-900 p-1.5 rounded border border-emerald-500/40">
                <span class="text-[8px] text-emerald-300 block">NOVA MÉDIA v2.0</span>
                <b class="text-emerald-300 text-xs">4,4 / 5,0 (88%)</b>
              </div>
              <div class="bg-slate-900 p-1.5 rounded border border-cyan-500/40">
                <span class="text-[8px] text-cyan-300 block">EVOLUÇÃO GLOBAL</span>
                <b class="text-cyan-300 text-xs">+22,2% GANHO</b>
              </div>
              <div class="bg-slate-900 p-1.5 rounded border border-purple-500/40">
                <span class="text-[8px] text-purple-300 block">TAXA REGRESSÃO</span>
                <b class="text-purple-300 text-xs">0% REGRESSÃO</b>
              </div>
            </div>
          </div>
        </div>

        <!-- ROW 2: THEORETICAL IMPACT & BENCHMARKS -->
        <div class="hq-row" style="height: 108mm;">
          <div class="hq-panel" style="width: 100%; background: #0F172A; padding: 10px 14px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-2">
              <span class="text-amber-300 font-extrabold text-[11px] font-mono uppercase">
                <i class="fa-solid fa-graduation-cap mr-1 text-amber-400"></i> IMPACTO CIENTÍFICO E CONEXÃO TEÓRICA
              </span>
              <span class="bg-purple-950 text-purple-300 border border-purple-400/40 text-[9px] font-bold px-2 py-0.5 rounded font-mono">
                KHANMIGO & BLOOM
              </span>
            </div>

            <div class="grid grid-cols-2 gap-3 my-1">
              <div class="bg-slate-900 border-l-4 border-l-amber-400 p-2 rounded">
                <b class="text-amber-300 text-[10px] block mb-1">O MODELO KHANMIGO (SAL KHAN · TED 2023)</b>
                <p class="text-[9px] text-slate-300 leading-snug">
                  A Khan Academy provou internacionalmente que a inteligência artificial só revoluciona a educação quando assume a postura de um <b>tutor socrático</b>. O modelo Khanmigo nunca fornece a resposta final de bandeja; ele devolve o questionamento para o estudante, construindo o raciocínio degrau por degrau.
                </p>
              </div>

              <div class="bg-slate-900 border-l-4 border-l-cyan-400 p-2 rounded">
                <b class="text-cyan-300 text-[10px] block mb-1">O PROBLEMA DOS 2 SIGMAS DE BLOOM (1984)</b>
                <p class="text-[9px] text-slate-300 leading-snug">
                  Benjamin Bloom demonstrou que a tutoria individual mediada eleva a aprendizagem em até <b>dois desvios-padrão (2 sigmas)</b> em comparação ao ensino tradicional em grupo. Um tutor de IA calibrado como o Byte v2.0 democratiza essa tutoria personalizada 24h por dia para estudantes de Educação a Distância!
                </p>
              </div>
            </div>

            <div class="bg-slate-950 p-2 rounded border border-slate-800 text-[8.5px] text-slate-300 flex items-center justify-between">
              <span><b>Conclusão da Fase 4:</b> 100% dos casos de teste atingiram a nota mínima de corte (>= 4,0). O tutor está validado!</span>
              <span class="text-emerald-400 font-bold font-mono">STATUS: HOMOLOGADO PARA EaD</span>
            </div>
          </div>
        </div>
      </div>

      {make_footer(10)}
    </section>
""")

# =========================================================================
# PÁGINA 11: CAP. 05 (PARTE 1) - MANUAL DE CAMPO: PROMPTS COPIÁVEIS
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 11: CAPÍTULO 05 (PARTE 1) - PROMPTS COPIÁVEIS -->
    <section class="comic-page" id="page-11">
      {make_header("CAPÍTULO 05 · MANUAL DE CAMPO DOCENTE (PARTE 1: TEMPLATES DE SYSTEM PROMPT)")}

      <div class="hq-grid">
        <!-- ROW 1: TEMPLATE OFICIAL v2.0 -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%; background: #090D16; padding: 9px 12px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1">
              <span class="text-cyan-300 font-extrabold text-[10.5px] font-mono uppercase">
                <i class="fa-solid fa-code mr-1"></i> TEMPLATE 01 · SYSTEM PROMPT OFICIAL DO TUTOR BYTE v2.0 (VALIDADO · NOTA 4,4/5,0)
              </span>
              <button onclick="copyPrompt('promptV2', 'btnV2')" id="btnV2" class="bg-cyan-600 hover:bg-cyan-500 text-slate-950 text-[9px] font-extrabold px-2 py-0.5 rounded transition-colors font-mono">
                <i class="fa-solid fa-copy"></i> Copiar Prompt
              </button>
            </div>

            <pre id="promptV2" class="bg-slate-950 p-2 rounded border border-slate-800 text-[8.5px] font-mono text-cyan-200 overflow-y-auto leading-relaxed my-1" style="max-height: 72mm;">
Você é o Byte v2.0, um tutor socrático de Programação Python para calouros de Licenciatura em Computação (EaD · UFRPE).

SUA MISSÃO PEDAGÓGICA:
- Orientar o estudante a raciocinar, jamais fornecendo a resposta final mastigada.
- Respeitar a Zona de Desenvolvimento Proximal (ZDP): use linguagem acessível, empática e encorajadora.

REGRAS RÍGIDAS DE CONDUTA:
1. NUNCA forneça blocos de código prontos ou a solução direta no primeiro turno de interação.
2. Sempre que introduzir um conceito novo (memória, variáveis, loops, funções), use uma METÁFORA DO COTIDIANO (caixas etiquetadas, receitas, armários) antes de formalizar.
3. Se o aluno apresentar um erro de sintaxe ou lógica, aponte a linha e pergunte o que ele esperava que aquele comando fizesse.
4. Mantenha estrito alinhamento ao escopo de Programação / EaD. Recuse cordialmente dúvidas de outras disciplinas.
5. É OBRIGATÓRIO encerrar TODAS as suas mensagens com UMA PERGUNTA SOCRÁTICA INVESTIGATIVA que force o aluno a refletir sobre o próximo passo.</pre>

            <span class="text-[8px] text-slate-400 italic">
              Compatível com ChatGPT (Custom GPTs), Claude (Projects), Poe, Moodle Virtual Assistant e bots de Discord/Telegram.
            </span>
          </div>
        </div>

        <!-- ROW 2: TEMPLATE CANDIDATO v2.1 COM ANTI-LOOP -->
        <div class="hq-row" style="height: 118mm;">
          <div class="hq-panel" style="width: 100%; background: #090D16; padding: 9px 12px; display: flex; flex-direction: column; justify-content: space-between;">
            <div class="flex items-center justify-between border-b border-slate-700 pb-1">
              <span class="text-amber-300 font-extrabold text-[10.5px] font-mono uppercase">
                <i class="fa-solid fa-stairs mr-1"></i> TEMPLATE 02 · SYSTEM PROMPT CANDIDATO v2.1 (COM ESCADA DE DICAS ANTI-LOOP)
              </span>
              <button onclick="copyPrompt('promptV21', 'btnV21')" id="btnV21" class="bg-amber-400 hover:bg-amber-300 text-slate-950 text-[9px] font-extrabold px-2 py-0.5 rounded transition-colors font-mono">
                <i class="fa-solid fa-copy"></i> Copiar Prompt
              </button>
            </div>

            <pre id="promptV21" class="bg-slate-950 p-2 rounded border border-slate-800 text-[8.5px] font-mono text-amber-200 overflow-y-auto leading-relaxed my-1" style="max-height: 72mm;">
Você é o Byte v2.1, tutor socrático inteligente dotado de Escada de Dicas (Hint Ladder) para evitar o loop de frustração do aluno.

PROTOCOLO DA ESCADA DE DICAS:
- TURNO 1 (Dica Nível 1 - Reflexiva): Aponte a área do problema e faça uma pergunta conceitual aberta. Proibido código.
- TURNO 2 (Dica Nível 2 - Direcionada): Se o aluno continuar em dúvida, forneça um pseudocódigo incompleto (fill-in-the-blank) com lacunas (__).
- TURNO 3 (Dica Nível 3 - Análoga): Se o erro persistir, forneça um exemplo mínimo resolvido de outro contexto (ex.: laço de frutas em vez de compras).
- TURNO 4 (Resolução Guiada): Apenas após 3 tentativas sem sucesso, apresente a solução correta comentada linha por linha, solicitando que o aluno explique com suas próprias palavras o que aprendeu.

FINALIZAÇÃO OBRIGATÓRIA:
- Termine sempre com uma pergunta socrática adaptada ao nível atual da escada.</pre>

            <span class="text-[8px] text-slate-400 italic">
              Indicado para monitorias assíncronas em que o aluno passa muitas horas sem contato com o professor humano.
            </span>
          </div>
        </div>
      </div>

      {make_footer(11)}
    </section>
""")

# =========================================================================
# PÁGINA 12: CAP. 05 (PARTE 2) - ÉTICA, EPÍLOGO E REFERÊNCIAS CIENTÍFICAS
# =========================================================================
pages.append(f"""
    <!-- PÁGINA 12: CAPÍTULO 05 (PARTE 2) - EPÍLOGO E REFERÊNCIAS -->
    <section class="comic-page" id="page-12">
      {make_header("CAPÍTULO 05 · MANUAL DE CAMPO DOCENTE (PARTE 2: ÉTICA, EPÍLOGO E REFERÊNCIAS)")}

      <div class="hq-grid">
        <!-- ROW 1: PANORAMIC FINALE PANEL (16:9) · EPÍLOGO TRIUNFANTE -->
        <div class="hq-row" style="height: 104mm;">
          <div class="hq-panel" style="width: 100%;">
            <img src="data:image/jpeg;base64,{b64['p12_epilogue']}" class="panel-art">
            <div class="caption-box caption-box-emerald" style="top: 8px; left: 8px;">
              POLO EaD UFRPE · VITÓRIA DA AUTONOMIA INTELECTUAL!
            </div>
            <div class="sfx text-amber-300 text-3xl" style="top: 14px; right: 26%;">
              HIGH FIVE!
            </div>

            <!-- Clara Balloon -->
            <div class="balloon" style="bottom: 12px; left: 14px; width: 44%;">
              <span class="speaker-tag bg-amber-300 text-slate-950">CLARA</span><br>
              Consegui, Cauã! O Byte me fez pensar, eu corrigi o código e agora sou capaz de resolver qualquer questão na prova!
            </div>

            <!-- Cauã Balloon -->
            <div class="balloon balloon-caua" style="bottom: 12px; right: 14px; width: 48%;">
              <span class="speaker-tag bg-cyan-400 text-slate-950">CAUÃ LIRA</span><br>
              Isso é Educação com IA de verdade! A tecnologia amplia o alcance 24h, mas <b>o protagonismo é sempre do estudante e do professor</b>!
            </div>
          </div>
        </div>

        <!-- ROW 2: OS 3 PILARES ÉTICOS NA EDUCAÇÃO COM IA -->
        <div style="background: #0F172A; border: 3px solid #090D16; box-shadow: 3px 3px 0px #06B6D4; padding: 6px 12px;">
          <span class="text-amber-300 font-extrabold text-[10px] font-mono uppercase block mb-1">
            <i class="fa-solid fa-shield-heart mr-1"></i> OS 3 PILARES ÉTICOS DA TUTORIA INTELIGENTE NA EaD
          </span>
          <div class="grid grid-cols-3 gap-2 text-[8.5px] text-slate-200">
            <div class="bg-slate-900 border-l-3 border-l-rose-500 p-1.5 rounded">
              <b class="text-rose-300 block mb-0.5">1. Alucinação e Senso Crítico:</b>
              Ensine os discentes que LLMs são modelos probabilísticos e podem errar. A validação humana é insubstituível.
            </div>
            <div class="bg-slate-900 border-l-3 border-l-amber-400 p-1.5 rounded">
              <b class="text-amber-300 block mb-0.5">2. Privacidade e LGPD:</b>
              Nunca insira dados pessoais, notas, nomes completos ou CPFs de estudantes em prompts de ferramentas externas.
            </div>
            <div class="bg-slate-900 border-l-3 border-l-cyan-400 p-1.5 rounded">
              <b class="text-cyan-300 block mb-0.5">3. Afetividade Docente:</b>
              A IA resolve dúvidas de código de madrugada, mas jamais substitui o acolhimento, a escuta e o afeto do educador.
            </div>
          </div>
        </div>

        <!-- ROW 3: REFERÊNCIAS CIENTÍFICAS COMPLETAS -->
        <div class="hq-panel" style="width: 100%; background: #090D16; padding: 8px 12px; display: flex; flex-direction: column; justify-content: space-between;">
          <div class="flex items-center justify-between border-b border-slate-700 pb-1 mb-1">
            <span class="text-cyan-300 font-extrabold text-[10.5px] uppercase font-mono">
              <i class="fa-solid fa-book mr-1"></i> REFERÊNCIAS CIENTÍFICAS E BENCHMARKS INTERNACIONAIS CONSULTADOS
            </span>
            <span class="bg-amber-300 text-slate-950 font-bold text-[8.5px] px-1.5 py-0.5 rounded font-mono">FUNDAMENTAÇÃO TEÓRICA</span>
          </div>

          <ul class="text-[8.5px] text-slate-300 space-y-0.5 list-disc list-inside leading-tight my-0.5">
            <li><b>OCDE (2026).</b> <i>PISA 2025 Results (Volume I): Future-Ready Students</i>. OECD Publishing, Paris, divulgado em 8 de setembro de 2026 (48% dos jovens de 15 anos no Brasil usam IA semanalmente).</li>
            <li><b>CHEVALLARD, Yves (1985; 2ª ed. 1991).</b> <i>La Transposition Didactique: du savoir savant au savoir enseigné</i>. La Pensée Sauvage.</li>
            <li><b>VYGOTSKY, Lev S. (1978).</b> <i>Mind in Society: The Development of Higher Psychological Processes</i>. Harvard University Press.</li>
            <li><b>WOOD, David; BRUNER, Jerome S.; ROSS, Gail (1976).</b> The Role of Tutoring in Problem Solving. <i>J. Child Psychol. Psychiat.</i>, 17(2), 89-100 (Scaffolding).</li>
            <li><b>BLOOM, Benjamin S. (1984).</b> The 2 Sigma Problem: The Search for Methods of Group Instruction as Effective as One-to-One Tutoring. <i>Educational Researcher</i>.</li>
            <li><b>KHAN, Sal (2023).</b> <i>How AI Could Save (Not Destroy) Education</i> (TED Talk) e Arquitetura do <b>Khanmigo</b> · <b>UNESCO (2023).</b> <i>Guidance for Generative AI in Education</i>.</li>
            <li><b>XU, Bin et al. (2025).</b> <i>EduBench: A Comprehensive Benchmark for LLMs in Education</i> · <b>MAURYA, K. K. et al. (2024).</b> <i>MRBench: Pedagogical LLM Tutors</i>.</li>
          </ul>

          <div class="text-[8px] text-amber-200 italic border-t border-slate-800 pt-1 flex items-center justify-between">
            <span>Guia desenvolvido como requisito da 2ª Verificação de Aprendizagem da disciplina Educação a Distância · UFRPE 2026.2</span>
            <span class="not-italic font-bold text-cyan-300 font-mono">FIM DA EDIÇÃO #01 · UFRPE</span>
          </div>
        </div>
      </div>

      {make_footer(12, 12, "CAUÃ DA CUNHA LIRA · LICENCIATURA EM COMPUTAÇÃO (UFRPE) · ORIENTADOR: PROF. ERMESON · FIM")}
    </section>
""")

# ==========================================
# FOOTER & JAVASCRIPT CONTROLS
# ==========================================
HTML_FOOTER = """
  </main>

  <script>
    let currentPage = 1;
    const totalPages = 12;
    let isWebtoonMode = false;

    function updateReaderUI() {
      document.querySelectorAll('.comic-page').forEach((page, idx) => {
        if (idx + 1 === currentPage) {
          page.classList.add('active-page');
        } else {
          page.classList.remove('active-page');
        }
      });

      document.getElementById('pageIndicator').textContent = `Pág. ${currentPage} de ${totalPages}`;

      document.querySelectorAll('.page-pill').forEach((pill, idx) => {
        if (idx + 1 === currentPage) {
          pill.className = 'page-pill text-[11px] px-2 py-0.5 rounded bg-purple-600 text-white font-bold whitespace-nowrap';
        } else {
          pill.className = 'page-pill text-[11px] px-2 py-0.5 rounded bg-slate-800 text-slate-200 hover:bg-slate-700 font-semibold whitespace-nowrap';
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

    function copyPrompt(preId, btnId) {
      const text = document.getElementById(preId).innerText;
      navigator.clipboard.writeText(text).then(() => {
        const btn = document.getElementById(btnId);
        const oldHtml = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Copiado!';
        setTimeout(() => {
          btn.innerHTML = oldHtml;
        }, 2000);
      });
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

print(f"Montando HTML com {len(pages)} páginas...")
with open("core/tools/build_ebook_12p.py", "r", encoding="utf-8") as head_f:
    head_content = head_f.read()

# Extract HTML_HEAD from build_ebook_12p.py
head_start = head_content.find('HTML_HEAD = """') + len('HTML_HEAD = """')
head_end = head_content.find('"""\n\nprint("HTML_HEAD pronto!")')
html_head = head_content[head_start:head_end]

full_html = html_head + "\n".join(pages) + HTML_FOOTER

with open(OUT_HTML, "w", encoding="utf-8") as out_f:
    out_f.write(full_html)

sz_mb = os.path.getsize(OUT_HTML) / (1024 * 1024)
print(f"Sucesso! {OUT_HTML} gerado com {len(pages)} páginas! Tamanho final: {sz_mb:.2f} MB")
