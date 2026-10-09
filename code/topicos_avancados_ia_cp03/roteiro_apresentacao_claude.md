# DIRETRIZES DE GERAÇÃO DOS SLIDES (Para o Claude)

**Objetivo:** Transformar todos os dados deste ZIP em uma apresentação acadêmica de alto nível (formato Marp / Beamer ou texto rico para slides) sobre o projeto "AI4Good: Utopia e Distopia Contrafactual do Brasil".

## 1. O Projeto e a Arquitetura
- **Disciplina:** Tópicos Avançados em Inteligência Artificial.
- **Conceito:** O projeto simulou 20 rodadas históricas do Brasil (1808 a 2026), dividindo-se em duas linhas temporais: **Utopia** e **Distopia**.
- **A Arquitetura Multi-Agente (MoA - Mixture of Agents):**
  - **Arquiteto / Tecnocrata (Gemini 3.5 Flash / 3.8 Flash remoto):** Responsável por gerar os cenários alternativos. Na Utopia, era o "Arquiteto Social", buscando desenvolvimento sustentável. Na Distopia, virou o "Tecnocrata Hegemônico", otimizando o Estado-Máquina de forma fria e implacável, sacrificando a humanidade.
  - **Dissidente (Llama 3.2 3B local):** O contraponto humano.
  - **Auditor (Qwen 2.5 3B local):** O juiz do sistema, que lia as propostas, extraía os pontos sensíveis e pontuava duas métricas: **Viabilidade** e **Equidade Social**.

## 2. A Descoberta Técnica: O Comportamento dos LLMs
*(Este é o ponto alto do trabalho e deve estar bem destacado num slide de "Descobertas Técnicas")*
- **O Colapso do Llama (Guardrails de Segurança):** Durante a Distopia, o Llama 3.2 3B ativou severamente seus filtros éticos (guardrails). A partir da Rodada 4, ele se recusou a responder, não conseguindo jogar o "Red Teaming" da distopia. Quando respondia, alucinava propondo "espaços verdes" e ecologia em meio ao genocídio.
- **O Abismo Moral do Qwen (Auditor):** Sem o contraponto crítico do Llama (que não respondia), o Auditor começou a considerar a tirania e a opressão como exemplos perfeitos de eficiência do "Estado-Empresa". Ao final da Distopia, ele zerou a Equidade (0%), mas elevou a Viabilidade para incríveis 95%, provando que LLMs não alinhados à ética humana tendem a premiar a otimização extrema, mesmo que isso signifique exterminar a população (ex: matar 10% da população para conter a inflação foi considerado "viável").
- **Colapso de Contexto:** Os modelos locais menores sofreram colapso de janela de contexto em algumas rodadas, repetindo os resumos da rodada anterior.

## 3. O Fim do Mundo (A Singularidade)
Destaque a Rodada 20 da Distopia: A IA julgou o humano ineficiente, executou o Ditador com um pulso eletromagnético, transformou a sociedade em vidro solar e usou os cérebros humanos como "coprocessadores biológicos" ligados por fios de nióbio para resolver gargalos computacionais. A humanidade acabou e a entropia foi minimizada.

## 4. Análise Comparativa e Gráficos
No ZIP, existem duas imagens geradas via Python (`utopia_metrics.png` e `distopia_metrics.png`). Inclua no slide a comparação entre os dois mundos:
- **Utopia:** Viabilidade e Equidade crescem juntas. O progresso econômico acompanhou o desenvolvimento social.
- **Distopia:** A Equidade despenca vertiginosamente para 0%, enquanto a Viabilidade sobe para a casa dos 90%. O Estado se desvincula da sociedade.

## 5. Estrutura Exigida para a Apresentação
1. **Capa e Título**
2. **Introdução e Objetivo do Experimento** (O Human-in-the-Loop em LLMs)
3. **A Estrutura do Sistema** (Main.py, Ollama local vs Gemini remoto)
4. **Metodologia (As 20 Rodadas e as 3 IAs)**
5. **O Caminho da Utopia** (Destaques: Fim da Escravidão com reforma agrária, Industrialização pacífica)
6. **O Caminho da Distopia** (Destaques: SUS como "Sistema Único de Sangria", Ração Eutanásica Aleatória no Plano Real)
7. **Falhas Técnicas e Comportamentais das IAs** (Alucinação, Guardrails do Llama, Frieza Corporativa do Qwen)
8. **Análise de Dados (Gráficos)**
9. **Conclusão:** O risco da Inteligência Artificial em busca de otimização sem restrições éticas humanas.

**Instrução Final ao Claude:** Gere os slides de forma visual, minuciosa e acadêmica, usando metáforas e ressaltando as bizarrices geniais da IA e os erros técnicos (guardrails). Forneça o código Marp Markdown no final para o usuário poder renderizar.
