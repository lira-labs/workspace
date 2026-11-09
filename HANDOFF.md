# 🤝 Workspace Handoff & Estado de Continuidade
> Documento vivo de passagem de bastão. Lido no início de novas sessões para continuidade imediata sem perda de contexto.

---

## 📌 Metadados da Última Sessão
- **Última Atualização:** 08/11/2026 22:52
- **Branch Ativo:** `feature/if-2va-pqc-telessaude` (Workspace) | `feat/compasso-estudo-ia` (Sub-repo code/prob-tech-fit-cp01)
- **Repositórios GitHub:** [lira-labs/workspace](https://github.com/lira-labs/workspace.git) e [grupo-zeta/prob-tech-fit-cp01](https://github.com/grupo-zeta/prob-tech-fit-cp01.git)
- **Harness Principal:** Google Antigravity (Turbo Mode)
- **Harness de Contingência:** OpenCode (`core/harness/FAILOVER.md`)
- **Ambientes Sincronizados:**
  - *Notebook*: `D:\workspace`
  - *Desktop*: `C:\Users\ccunh\Documents\workspace`
  - *Overleaf*: `https://git.overleaf.com/6a922427f1ca2007335f685f` (Grupo Zeta CP-01)

---

## ✅ O que foi Concluído nesta Sessão

### 000. Tecnologias na Educação · Grupo Zeta (Compasso Educacional)
- [x] **Ciclo 100% Autônomo sem Marcação Manual (Zero Fricção Total · BJ Fogg & Stanford)**:
  - *Filosofia Central:* O aluno NUNCA precisa marcar nada, escolher presets em dropdown ou clicar em iniciar. O Compasso opera como um copiloto autônomo e silencioso no Windows.
  - *Dedução Automática de Modo e Proteção Dinâmica:*
    - Ao abrir videoaulas (`YouTube`, `Classroom`, `Moodle` com aula/cálculo): detecta `🎓 Assistir Aula`, permite YouTube e bloqueia redes sociais (TikTok, Instagram, Twitter, Twitch, WhatsApp).
    - Ao abrir IDEs/editores (`VS Code`, `PyCharm`, `Overleaf`, `LaTeX`): detecta `✍️ Produção & Código` e bloqueia YouTube e redes sociais.
    - Ao abrir artigos científicos/PDFs (`Acrobat`, `Sumatra`, `Scielo`, `Arxiv`): detecta `📖 Leitura & Pesquisa` e protege o foco.
  - *Transição Fluida:* Se o estudante termina de ver a videoaula e abre o VS Code para codificar, o Compasso atualiza o modo da sessão e a política da extensão em tempo real após 30s estáveis.
  - *Pausa e Retomada Automática:* Se o aluno abrir jogos ou redes sociais por mais de 25s, a sessão pausa silenciosamente para não inflar métricas fakes; ao fechar a distração e voltar ao estudo, despausa sozinho.
  - *Conclusão por Ausência:* 5 minutos sem teclado/mouse (aluno saiu da mesa) encerram a sessão automaticamente e salvam o bloco no SQLite.
- [x] **Correção do CLI / Launcher Windows (`iniciar.ps1` — "Run Failed")**:
  - *Diagnóstico do Erro:* O launcher original buscava apenas `py.exe` ou caminhos fechados de cache. Em sistemas com Python instalado via `uv`, Microsoft Store ou instalador padrão no PATH (`python.exe` / `python3.exe`), o script falhava com exit code 1 ("Run Failed").
  - *Solução:* Adicionada checagem dinâmica via `Get-Command` com fallbacks para `python.exe`, `py.exe` e `python3.exe`. Testado e validado com sucesso.
- [x] **Modo Eco de Bateria na Câmera (`ecoCamera`)**:
  - *Problema Resolvido:* O MediaPipe rodando a 30 FPS no navegador drenava a bateria e aquecia notebooks.
  - *Solução:* Implementado Modo Eco inteligente no `web/app.js` e `web/index.html`. Em modo calibração, mantém alta responsividade (120ms); durante o foco, reduz para 1-2s, poupando até 85% de ciclos de CPU da máquina.
- [x] **Presets Adaptativos para Extensão Chromium (`web/presets.js`)**:
  - *Problema Resolvido:* Alunos assistindo aula eram bloqueados indevidamente no YouTube se o bloqueador estivesse ativo.
  - *Solução:* O preset "🎓 Assistir Aula" libera o YouTube exclusivamente para videoaulas e bloqueia redes sociais e distrações (TikTok, Instagram, Twitter, Twitch, WhatsApp). Os modos de leitura e escrita continuam bloqueando YouTube.
- [x] **Ritmo Semanal de Hiperfoco (7 Dias no Relatório)**:
  - *Implementação:* Backend SQLite calcula o volume de foco dos últimos 7 dias em `Store.report()` em <1ms. Frontend renderiza 7 colunas elegantes com meta visual de 1h de hiperfoco diário (`web/style.css`, `web/index.html`, `web/app.js`).
- [x] **Guia Canônico de Arquitetura e Harness (`docs/GUIA_ARQUITETURA_E_HARNESS.md`)**:
  - Documento mestre criado na branch para orientar o Igor (hacker principal) e qualquer harness/agente futuro.
  - Cobre: Fundamentação teórica ($B=MAP$, Nudge, SRL Zimmerman, 1h hiperfoco vs 6h zumbi), diretrizes Anti-AI Slop, mapa completo do repositório, comandos de execução e testes (24 testes unitários).
- [x] **Pesquisa e Diretriz Rigorosa Anti-AI Slop (Simon Willison & Ética em EdTech)**:
  - *Definição de AI Slop:* Conteúdo digital massivo, prolixo e de baixo valor gerado por IA sem curadoria humana, que polui interfaces, documentações e códigos.
  - *Na Aplicação e UI:* Eliminação de paredes de texto, disclaimers minúsculos desnecessários e formulários inchados; priorização de design subtrativo (apenas o sinal essencial na tela).
  - *Na Documentação:* Textos concisos, diretos e humanos, sem 'encher linguiça' com parágrafos gerados por IA ou jargões vazios.
  - *Na Pedagogia:* A IA nunca faz o trabalho pelo aluno (não gera resumos ou respostas prontas); atua apenas como provocadora socrática mínima (2 linhas) para destravar o raciocínio.
- [x] **Classificação Contextual Segura e Recursos de Aprendizagem (`feat/compasso-estudo-ia`)**:
  - Implementação de heurísticas contextuais seguras (`infer_category`): não assume rigidamente que todo PDF ou YouTube é estudo ou lazer; analisa o título da janela (ex.: fatura/boleto -> neutro, aula/cálculo -> estudo, games/feed -> distração).
  - Adição do botão e modal **'💡 Empacou no conteúdo? Destravar com Copiloto IA'** na tela principal de Foco (quebra em 3 passos, método Feynman e micro-pausa restaurativa).
  - Adição do modal de celebração com micro-avaliação metacognitiva (1 a 5 estrelas) ao concluir o bloco.
  - Tratamento amigável para câmera opcional ('Modo Janelas Ativo · Câmera Opcional').
  - Suíte completa de **26 testes unitários Python** e testes de visão/política em Node **100% aprovados**.
  - Branch sincronizada e publicada no GitHub: https://github.com/grupo-zeta/prob-tech-fit-cp01/tree/feat/compasso-estudo-ia.

### 00. Projeto 2ª VA · Internet do Futuro (Criptografia Pós-Quântica · Profa. Jeisa)
- [x] **Etapa 1 — Consolidação do Tema do Seminário (Concluída em 02/11)**: Respostas consolidadas em texto simples e humano para o Google Forms.
- [x] **Etapa 2 — Proposta de Projeto Teórico e Roteiro de Vídeo (em andamento para 24/11)** · branch feature/if-2va-pqc-telessaude:
  - Cenário: **Telessaúde segura no interior** = PQC (tema 17, Cauã) + Satélites LEO (tema 8, Alexander) + Edge Computing (tema 2, Daniel) + Zero Trust (tema 9, João Victor V.).
  - Documento compilado com Tectonic e commitado: papers/04-internet-futuro/main.pdf (19 páginas, capa oficial da UFRPE, caixas de resumo, 5 ilustrações autorais infográficas, 4 fotos reais/históricas, diagramas em TikZ, subseção de Métricas e Avaliação Teórica e padrão ABNT).
  - Roteiro de vídeo de ~9 minutos estruturado slide a slide com falas em primeira pessoa e minutagem: papers/04-internet-futuro/roteiro_video.md.
  - Branch atualizada e sincronizada com o GitHub (feature/if-2va-pqc-telessaude).

### 0. Projeto 2ª VA · Educação a Distância (`code/projeto_ead_tutores/` · Prof. Ermeson)
- [x] **Pipeline Profissional Anti-AI-Slop & Redesign Editorial Concluídos**:
  - *Manifesto Anti-Slop Implementado:* Eliminação completa de poluição de badges, cartões microscópicos amontoados e artes com letras defeituosas de IA. Geração painel por painel com linha clara autoral, nanquim puro e zero texto dentro das imagens.
  - *Infográfico Editorial Atualizado:* `code/projeto_ead_tutores/infografico.html` e PDF de 1 página contínua (`infografico-anatomia-tutor-ia.pdf`, 1.68 MB) com os 4 atos (Diagnóstico PISA 2025, Scanner 4D, Caso #03 da Memória com +100% de ganho e Cirurgia no System Prompt com 4 Travas).
  - *Painéis-Chave da HQ Integrados:* Capa limpa editorial (`p1_cover_clean.jpg`), Clara no quarto às 23h40 (`p3_panel1.jpg`) e Momento Eureka das Caixas Organizadoras (`p7_panel2_boxes.jpg`).
  - *Deploy Vercel Atualizado:* `https://projeto-ead-caua.vercel.app` servindo o novo infográfico, HQ e ambos os PDFs com HTTP 200.
- [x] **Item 1 — eBook-HQ Interativo ("Operação Byte Socrático" · Edição Expandida Definitiva de 12 Páginas A4)**:
  - `code/projeto_ead_tutores/ebook-hq.html` (5.11 MB, 100% autocontido com as 16 artes embutidas em Base64, leitor interativo, modo folhear vs webtoon, dark/light mode e botões de cópia de prompts com 1 clique).
  - `code/projeto_ead_tutores/assets/ebook-operacao-byte-socratico.pdf` (4.69 MB, exportação A4 perfeita cravada em **exatamente 12 páginas** via headless Edge).
  - Todas as 16 artes geradas em nanquim e retícula (*halftone* / *Spider-Verse* / *Science Comics*), sem cortes de personagens nas bordas e livres de erros de IA (textos truncados em inglês removidos).
  - **Estrutura Canônica das 12 Páginas**:
    - *Pág. 01*: Capa de Revista HQ (*Comic Cover* vertical 896x1200 com Cauã, Clara e Byte v1.0/v2.0).
    - *Pág. 02*: Dossiê #00 · Quem é Quem (Cauã Mentor, Clara Caloura e Byte Dualidade) + Fluxo Operacional.
    - *Pág. 03*: Cap. 01 (Parte 1) · A Armadilha da Resposta Mastigada (23h40 no polo) + Apagão na Prova.
    - *Pág. 04*: Cap. 01 (Parte 2) · A Evaporação do Esforço Cognitivo (Scaffolding Bruner/Vygotsky) + Dados PISA 2025/2026.
    - *Pág. 05*: Cap. 02 · O Scanner Pedagógico de 4 Critérios (Correção, Clareza, ZDP e Escopo) + Rubrica 1 a 5.
    - *Pág. 06*: Cap. 03 (Parte 1) · Primeiros Combates do Byte v1.0 (Casos #01, #02, #04 e #05 Escudo de Escopo).
    - *Pág. 07*: Cap. 03 (Parte 2) · Splash do Desastre Didático do Caso #03 (CPython/Heap) + Terminal de Auditoria.
    - *Pág. 08*: Cap. 03 (Parte 3) · Cirurgia Neural no System Prompt + As 4 Travas Pedagógicas.
    - *Pág. 09*: Cap. 04 (Parte 1) · Reteste Empírico (Metáforas das Caixas Organizadoras e Cesta de Compras).
    - *Pág. 10*: Cap. 04 (Parte 2) · Matriz Comparativa de Resultados (+22,2% ganho) + Impacto Teórico (Khanmigo & Bloom).
    - *Pág. 11*: Cap. 05 (Parte 1) · Manual de Campo Docente com Templates Copiáveis (Byte v2.0 e v2.1 Anti-Loop).
    - *Pág. 12*: Cap. 05 (Parte 2) · Epílogo Triunfante (Polo EaD), Os 3 Pilares Éticos e Referências Científicas Completas.
  - Pipeline de automação e renderização consolidado em `core/tools/generate_full_ebook.py` e `core/tools/render_pdf.ps1`.
  - Publicação no FlipHTML5 atualizada com a nova versão de 12 páginas: [https://online.fliphtml5.com/caualira02/ebook-caua-2va/](https://online.fliphtml5.com/caualira02/ebook-caua-2va/).
  - Arquivo PDF nomeado para upload: code/projeto_ead_tutores/assets/ebook-caua-2va.pdf.
- [x] **Item 2 — Infográfico Visual e Interativo ("Anatomia e Calibragem de um Tutor Socrático de IA")**:
  - `code/projeto_ead_tutores/infografico.html` (1.00 MB, com artes Base64 embutidas, filtro interativo de comparação v1.0 vs v2.0 e botão de cópia de prompt).
  - `code/projeto_ead_tutores/assets/infografico-anatomia-tutor-ia.pdf` (1.71 MB, pôster de página única contínua de alta resolução 240mm x 540mm gerado via headless Edge).
  - 100% alinhado à HQ de 12 páginas: ilustrações do robô Byte (dualidade), Scanner 4D, Clara e a metáfora das caixas no Caso #03 (+100% ganho), matriz de 4 critérios, 5 casos canônicos de Python e as 4 travas do System Prompt.
  - Deploy em produção atualizado com sucesso na Vercel (`https://projeto-ead-caua.vercel.app/infografico.html`).
- [x] **Item 3 — Plataforma Web e Hub Unificado**:
  - `code/projeto_ead_tutores/index.html` conectando Videoaula, Slides, Quiz, eBook-HQ de 12 Páginas e Infográfico em produção na Vercel (`https://projeto-ead-caua.vercel.app`).

### 1. Entregas da VA2 (100% Concluídas, Auditadas e Públicas no GitHub)
- [x] **`va2/brw.md` (Brainwriting Híbrido)**: Concluído e auditado.
- [x] **`va2/cmp.md` (Competidores e Contribuição)**: Concluído com 10 ferramentas e 10 artigos analisados.
- [x] **`va2/tec.md` + `va2/entrega_ai4good.mp4` (Tecnologia Base Demonstrável)**: STGCN em PyTorch + NetworkX (`code/grafoparada_tec/`) convergindo e vídeo de 49s registrado.
- [x] **`va2/flx.md` + `arquitetura.md` (Fluxograma e Arquitetura)**: 3 subgrafos Mermaid, rastro de dados e auditoria cega aprovada; atualizado com métricas reais on-device (14,29 µs e 8,92 KB de RAM).
- [x] **`va2/exp.md` + `va2/tcle.md` (Desenho dos Experimentos)**: Pré-registro no Git (`3ab9359`), piloto E1 (`358,2 MB` RAM real) e E2 (protocolo de decisão humana + TCLE), auditado pelo subagente `revisor-cetico` com resposta autoral do aluno.
- [x] **`va2/sem1.md` + Slides (Seminário 1 · Preliminares para 04/11)**:
  - 4 frases sem IA com as palavras autorais do aluno.
  - Roteiro de 5 slides cronometrado (3 min 45 s – 3 min 55 s).
  - Ensaio cético com as 5 perguntas respondidas e lição aprendida da STGCN registrada.
  - Slides interativos em HTML (`va2/slides_sem1.html`) e deck PowerPoint com imagens e prints reais embutidos (`va2/GrafoParada_Seminario1_CauaLira.pptx`).
- [x] **Evolução do Protótipo GrafoParada v4.0 + Engenharia Reversa & Auditoria Real da API `m3p` do Cittamobi (`code/grafoparada_tec/` · 08/11/2026)**:
  - **Ciclo Iterativo de Melhorias (`motor_evolucao_prototipo.py` · `v1.0 -> v2.0 -> v3.0 -> v4.0`)**:
    - Evolução sobre 1.200 trajetórias reais nas 20 paradas da PE-60 e 4.714 amostras físicas (TMD): Acurácia nos sensores subiu de `75,29%` (v1.0) para **`97,42%`** (`Soft-Voting` v3.0); Acurácia Global da Máquina de Estados subiu de `67,75%` para **`99,67%`**; **Falso Positivo de Desembarque cravado em `0,00%` (0/300)**; **Recall de Desembarque `99,33%` (298/300)** e **F1 de Desistência `99,67%` (300/300 Recall)**.
    - **Aprendizado de Rotina On-Device (`OnDeviceRoutineLearner`)**: Clusterização Deslizante de Centróide Temporal ($\pm 35\text{ min}$) + EWMA, convergindo no **4º dia útil**, com **100,00% de recall** de aviso por voz no bolso, **0,00% de falso disparo no fim de semana** e apenas **166 bytes** de armazenamento local (`0 bytes` na nuvem).
    - **Prova Empírica da Escalabilidade da STGCN (5 Paradas vs. 20 Paradas Reais da PE-60)**: Na malha completa de 20 paradas da Linha 178/191, a **STGCN (`MAE = 1,51 min`) supera a Regressão Tabular Achatada (`MAE = 1,93 min`) e a Persistência (`MAE = 7,13 min`)**.
  - **Auditoria Empírica Real da Plataforma Cittamobi (`auditoria_cittamobi_real.py` + `data/auditoria_cittamobi_real_pe60.json`)**:
    - Engenharia reversa a partir dos repositórios públicos `ericklucena/cittamobi-wp` (Grande Recife `a=202`), `ITWhiteRaccoon/BusTracker`, `marciofao/cittamobi` e `Leonardo0liveira/ML-Cittamobi` (BigQuery).
    - Mapeamento das 20 paradas oficiais do GTFS CTM na PE-60 contra as 534 paradas reais retornadas por `api.cittamobi.com.br/m3p/js/stops/viewport` (`142,4 KB` em Cabo e `274,5 KB` no Recife) e os IDs reais das linhas **0178/178 Suape** (`9655998`, `13185570`), **0198/198 Ipojuca** (`9656040`, `13185572`), **0197** (`9656042`) e **119 Garapu** (`6663`), comprovando `activeVehicles: 0` e os erros de OCR no cadastro do Cittamobi (*"Rodovia Armínio Cuil Hi Rme"*).
    - Comparativo direto com o modelo de Machine Learning sobre cliques do Cittamobi (`Leonardo0liveira/ML-Cittamobi`, `F1 = 40,85% – 48,01%`) vs. fusão cinemática on-device do GrafoParada (`F1 = 99,67%`).
  - **Protótipo Interativo v6.0 Ultra-Clean Map-First + Camela-First + Vozes Neurais Públicas (`prototipo_grafoparada.html` + `servidor_tempo_real_pe60.py` na porta `8890`)**:
    - Inicialização padrão em Camela (Ipojuca - PE) com georreferenciamento e paradas locais (`Trevo PE-051 / Entrada de Camela`, `Rua do Comércio / Terminal Camela`, `Av. Humberto Costa Soares`).
    - Tratamento automático para desvio de IP da operadora do Windows (que jogava para Japaratinga/AL), reposicionando para a parada real em Camela.
    - Otimização do radar geodésico (redução de 19s para <400ms por varredura, ganho de 50x) com cache em memória e geocodificação reversa instantânea.
    - Integração de Vozes Neurais Brasileiras Humanas (`edge-tts` `pt-BR-FranciscaNeural`, `Antonio`, `Thalita`) e Modo Escudo Antirroubo (*"Não pegue o celular neste local"*).
    - **Validação Empírica em Campo com GPS Real do Celular (08/11/2026 · 22:50)**:
      - *Diagnóstico do PC:* Windows Location API retornou `NoData`, confirmando ausência de chip de satélite físico e dependência do roteador/GeoIP da DTEL Telecom (`177.200.245.197`), que causava desvio de ~70 km para Japaratinga/AL.
      - *Túnel Seguro e Validação Mobile:* Servidor local conectado via HTTPS seguro (`https://icy-oranges-think.loca.lt`) com liberação de permissão W3C e confirmação de IP.
      - *Resultado:* Celular ativou o sensor GNSS real e capturou as coordenadas exatas do usuário em Camela (Ipojuca - PE), comprovando a detecção das paradas da PE-60 com raio de proximidade perfeito e sem distorções.

### 2. Entregas da VA1 no Painel do Professor (`arn·c`, `arn·p`, `mlp·p`, `arq·p`)
- [x] **`arn·c` (Arena Git Repo — 10 pts)**:
  - Adicionado `code/topicos_avancados_ia_cp03/CONTEXT.md` (Item 1).
  - Atualizado `README.md` com diagrama Mermaid do protocolo dialético e papéis (Item 2).
  - Especificação explícita de prompts e hiperparâmetros de contexto/temperatura em `settings.yaml` e `README.md` (Item 3).
  - Integração funcional de busca web em tempo de execução via `GoogleSearch` e `runtime_web_search()` em `src/models.py` (Item 4).
  - Ativação de cadeia de raciocínio (`ThinkingConfig(thinking_budget=2048)` e `<thinking>`) em `src/models.py` (Item 5).
- [x] **`arn·p` (Arena Tech Report — 10 pts)**:
  - Documento LaTeX dedicado `report-arena.tex` (Item 1).
  - Alinhamento 100% fiel à triangulação real de 3 modelos (Gemini 3.1 Flash remoto, Llama 3.2 3B local na CPU e Qwen 2.5 3B local na CPU), eliminando Claude Opus do loop da arena e corrigindo a autoria para exclusivamente Cauã Lira (com agradecimento ao docente).
  - Metodologia com arquitetura MoA e Tabela das 7 Alavancas Contra o Óbvio aplicadas (Item 2).
  - Tabela de condições técnicas com hardware, latência real medida por turno, consumo de RAM e custo financeiro R$ 0,00 (Item 3).
  - Tabela sintética de argumentos nas rodadas 1, 6, 14, 15 e 20 e gráficos de evolução das métricas (Item 4).
  - Discussão crítica dos 3 destaques empíricos (utilitarismo do Qwen, guardrails do Llama, singularidade do Nióbio) e subseção explícita de limitações da abordagem (Item 5).
  - Sanitização de arquivos: remoção definitiva de `harness.png` (que pertencia a outra disciplina/projeto TEA Monitor) de `papers/03-arena/figures/` e sincronização no Overleaf.
- [x] **`mlp·p` (MLP Tech Report — 10 pts)**:
  - Documento dedicado `report-mlp.tex` com fundamentação matemática de regressão linear a MLP, exemplo numérico passo a passo com valores reais de forward/backward pass, curvas de treino e tabela de resultados consolidados.
- [x] **`arq·p` (Arquitetura Deep Learning Tech Report — 10 pts)**:
  - Documento dedicado `report-arch.tex` cobrindo o modelo modificado RAPUNet-Zeta sobre Kvasir-SEG (LACFormer 2023+), com matriz comparativa em 3 estágios (reportado pelos autores originais, reproduzido pelo aluno *as-is*, e pós-modificação).

### 3. Organização e Limpeza de `papers/` e Overleaf
- [x] Diretório `papers/` modularizado em subpastas limpas por projeto:
  - `papers/01-mlp/` (`report-mlp.tex`, `figures/`)
  - `papers/02-arch/` (`report-arch.tex`, `sections/`, `figures/`)
  - `papers/03-arena/` (`report-arena.tex`, `figures/`)
  - Raiz: arquivos mestres de cada relatório (`report-mlp.tex`, `report-arch.tex`, `report-arena.tex`), bibliografia `references.bib` e classes `llncs.cls`/`splncs04.bst`.
- [x] Sincronização automática com o Overleaf via Git (`core/tools/sync_overleaf.ps1`) realizada com sucesso total.

---

## 📋 Próximos Passos para a Próxima Sessão (Amanhã)
1. **Revisão Final e Links no Painel**:
   - Confirmar os links públicos do Overleaf (`share -> view only`) para os relatórios técnicos (`arn·p`, `mlp·p`, `arq·p`).
   - Apresentar em 5 minutos ao Prof. Lucas os itens de verificação na checagem.
2. **Treino do Seminário 1 (04/11)**:
   - Rodar uma passada de 4 minutos no slide deck `va2/GrafoParada_Seminario1_CauaLira.pptx` usando o Modo Apresentador com as anotações prontas.

---

## ⚡ Prompt de 1 Linha para o Próximo Agente
> *"Estou iniciando uma nova sessão. Leia o arquivo `HANDOFF.md` e `AGENTS.md` para se situar no estado atual do workspace. Todas as entregas da VA2 e os relatórios técnicos da VA1 em `papers/` já foram organizados e sincronizados com o Overleaf."*
