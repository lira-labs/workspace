# 🎬 Roteiro Mestre para Geração da Apresentação (Para o Claude) - VERSÃO 2 (Expandida)

Prezado Claude,

Este arquivo contém o direcionamento completo, minucioso e aprofundado para você gerar os **Slides da Apresentação Final** do nosso projeto da disciplina "Tópicos Avançados em IA". Você deve processar todos os arquivos JSON e Markdown das pastas `outputs/utopia/` e `outputs/distopia/` contidos neste repositório/ZIP, bem como o código fonte, para gerar uma apresentação acadêmica de excelência e rica em explicações.

## 🎯 Objetivo da Apresentação
Demonstrar a arquitetura técnica do nosso Sistema Multi-Agente (que simulou contrafactuais da História do Brasil) e apresentar, de forma aprofundada e analítica, os resultados das simulações: **Utopia** vs **Distopia**.

## 🛠️ O que os Slides devem conter obrigatoriamente (com riqueza de detalhes):

### 1. Capa e Introdução (Mais Contexto)
- **Título**: AI4Good: Simulando Contrafactuais Históricos com LLMs.
- **Contexto**: Explicar a proposta da disciplina de Tópicos Avançados em IA.
- **Motivação**: Como a IA pode ser usada para modelar cenários complexos de economia, política e impacto social ("E se o Brasil tivesse tomado outro caminho?"). Justifique a importância de usar LLMs para explorar caminhos que a história não tomou, evidenciando o valor preditivo e analítico.

### 2. A Arquitetura Técnica e as Métricas (Aprofundado)
- **Estrutura Multi-Agente**: Explicar detalhadamente os 3 agentes:
  - `Arquiteto` (LLM Remota/Gemini): O propositor das políticas.
  - `Cético` (LLM Local/Ollama): O crítico apontando falhas e consequências (incluindo as alucinações dele próprio).
  - `Auditor` (LLM Local/Ollama): O juiz do sistema. **CRÍTICO: Defina explicitamente o que são as métricas de Viabilidade (capacidade econômica, técnica e política da proposta sobreviver) e Equidade Social (justiça distributiva, impacto nas populações marginais, direitos humanos). Explique como o Auditor calculava isso e por que essas métricas balizam o sucesso/fracasso das políticas.**
- **O Verificador de Fatos (Human-in-the-Loop)**: Explicar o papel crucial do 4º agente (Antigravity/Claude) injetando correções no histórico para impedir degradação de contexto.

### 3. A Dinâmica da Simulação e Comparativos Profundos
- Comparar **Brasil Real**, **Utopia** e **Distopia**.
- **Para cada comparativo, traga JUSTIFICATIVAS CLARAS**: Por que a escolha X da Utopia gerou um resultado Y melhor que a vida real? E por que a escolha Z da Distopia resultou em colapso? (Ex: Como o Fundo Soberano protegeu o país na Utopia durante a crise global, ao contrário do Brasil real que sofreu desindustrialização).

### 4. Geração de Gráficos e Visualização de Dados (CRÍTICO)
> **Instrução para o Claude:** Use Python/Matplotlib/Plotly para gerar ou escrever código para os gráficos.
- **Gráfico 1**: *Evolução do IDH (1808-2026)*. Três linhas cruzando os séculos, com anotações textuais no gráfico nos pontos de inflexão.
- **Gráfico 2**: *PIB vs Dívida Externa*. A hiperinflação e endividamento (Real vs Distopia) vs o crescimento sustentável (Utopia).
- **Gráfico 3**: *Desmatamento na Amazônia e Autonomia Tecnológica*. 

### 5. As Alucinações da IA (O Estudo de Caso)
- Detalhe o colapso do contexto nos modelos locais (Ollama) na simulação da Utopia. Explique o loop do Auditor sobre "bases militares" que desabou a métrica de Viabilidade injustificadamente.
- A correção ativa do Cético que inventou que a "Vale fez peças para a Volkswagen em 1999".

### 6. Os Grandes Pontos de Virada (Turning Points - COM JUSTIFICATIVAS)
- **Soberania vs Doença Holandesa (Anos 2000)**: Explique o racional de trocar minério bruto por "Joint-Ventures" com a China e reter a riqueza num Fundo Soberano, garantindo Renda Básica contra a recessão global. Contraste isso fortemente com o que aconteceu na Distopia.

### 7. Conclusão da Disciplina
- Resumo de como a simulação LLM serve para Planejamento Estratégico Estatal.
- O futuro do Brasil: Como as escolhas do presente moldam se caminhamos para a Utopia ou para a Distopia.

---

**Nota Final ao Claude:**
A apresentação anterior estava muito resumida. A nova versão deve ser **rica em justificativas, explicações do porquê os caminhos deram certo ou errado, e a definição clara de todas as métricas**. Gere código LaTeX (Beamer) completo ou Marp Markdown, garantindo densidade acadêmica.
