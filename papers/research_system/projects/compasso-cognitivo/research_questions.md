# Research Questions & Experimental Protocol · Compasso Cognitivo

## Questões de Pesquisa (RQs)
- **RQ1 (Desempenho e Soberania na Borda):** Qual é o custo computacional (CPU, RAM, latência de frame/análise) e o perfil de tráfego externo da arquitetura *local-first* em estações Windows de uso cotidiano?
- **RQ2 (Adequação das Heurísticas Contextuais):** Em que medida a heurística geométrica de desvio inferior (com/sem óculos e leitura em papel) e a classificação automática Estudo vs. Hobby evitam falsos alertas em cenários controlados?
- **RQ3 (Usabilidade e Suporte à Autorregulação — HCAI):** Como usuários ($N=15$) avaliam a usabilidade (SUS), a oportunidade/baixa intrusividade do gadget WPF + intervenções JITAI, a consciência metacognitiva promovida e o conforto com a privacidade *on-device*?

## Plano de Coleta ($N=15$ + Benchmark) — A Executar após Build Final do Igor
1. **Pré-requisito de código:** corrigir default `llama3:8b` -> `gemma3:4b` na UI e gerar `Compasso.exe` atualizado.
2. **Benchmark (1 máquina controlada):** medir 5 min em cada modo (só SO; SO + MediaPipe; revisão Ollama `gemma3:4b`) registrando CPU média/pico, RAM (MB), FPS real e tráfego de rede.
3. **Piloto ($N=15$ participantes):** sessão estruturada (estudo real + simulação controlada de olhar baixo/celular, leitura em caderno, abertura de jogo/mídia e respiração 4-4-4) + exportação de sumário JSON/CSV anonimizado + formulário SUS (10 itens) + Likert SRL/JITAI (4 dimensões) + 2 perguntas abertas.
