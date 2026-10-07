# 🎬 Roteiro Mestre para Geração da Apresentação (Para o Claude)

Prezado Claude,

Este arquivo contém o direcionamento completo e minucioso para você gerar os **Slides da Apresentação Final** do nosso projeto da disciplina "Tópicos Avançados em IA". Você deve processar todos os arquivos JSON e Markdown das pastas `outputs/utopia/` e `outputs/distopia/` contidos neste repositório/ZIP, bem como o código fonte, para gerar uma apresentação acadêmica de excelência.

## 🎯 Objetivo da Apresentação
Demonstrar a arquitetura técnica do nosso Sistema Multi-Agente (que simulou contrafactuais da História do Brasil) e apresentar os resultados das duas simulações: **Utopia** (onde tomamos as melhores decisões possíveis) vs **Distopia** (onde o país tomou o pior caminho possível).

## 🛠️ O que os Slides devem conter obrigatoriamente:

### 1. Capa e Introdução
- **Título**: AI4Good: Simulando Contrafactuais Históricos com LLMs.
- **Contexto**: Explicar a proposta da disciplina de Tópicos Avançados em IA.
- **Motivação**: Como a IA pode ser usada para modelar cenários complexos de economia, política e impacto social ("E se o Brasil tivesse tomado outro caminho?").

### 2. A Arquitetura Técnica do Sistema
- **Estrutura Multi-Agente**: Explicar como configuramos os 3 agentes interagindo em um loop fechado:
  - `Arquiteto` (LLM Remota/Gemini): O propositor das políticas.
  - `Cético` (LLM Local/Ollama): O crítico implacável apontando falhas e consequências.
  - `Auditor` (LLM Local/Ollama): O juiz que sintetiza e pontua a Viabilidade e Equidade Social (mesmo sofrendo com alucinações).
- **O Verificador de Fatos (Human-in-the-Loop)**: Explicar o papel crucial do 4º agente (Antigravity/Claude) que injeta o *fact-checking* via arquivo de *scratch* em cada rodada para manter a sanidade histórica e impedir a degradação do contexto nos modelos locais menores.
- Mapeamento Técnico: Mostrar que a orquestração foi feita em Python (`main.py`, `orchestrator.py`) usando prompts dinâmicos baseados no `timeline_utopia.yaml` e no histórico iterativo (`history[-1]`).

### 3. A Dinâmica da Simulação
- O jogo percorreu 20 épocas chave (1808 a 2026).
- Comparativo entre:
  - **Brasil Real** (Linha do tempo histórica).
  - **Utopia** (As escolhas áureas guiadas pelo usuário e refinadas pelo Arquiteto).
  - **Distopia** (O pior dos mundos, as piores escolhas exploratórias).

### 4. Geração de Gráficos e Visualização de Dados (CRÍTICO)
> **Instrução para o Claude:** Você deve usar Python/Matplotlib ou Plotly (se for em formato de código a executar), ou gerar artefatos em Mermaid ou SVG representando os dados contrafactuais. Se gerar código, escreva os scripts de plotagem.
- **Gráfico 1**: *A Evolução do IDH (1808-2026)*. Mostre 3 linhas: Brasil Real, Utopia (disparando para patamares nórdicos) e Distopia (caindo para abismos).
- **Gráfico 2**: *PIB vs Dívida Externa nos Anos 80*. Mostre como a Utopia evitou a hiperinflação da década perdida (recusando petrodólares) versus a crise da história Real.
- **Gráfico 3**: *Desmatamento na Amazônia (2019-2022)*. Comparar os 13.000 km² do Brasil real com a preservação de Tolerância Zero da Utopia.
- **Gráfico 4**: *Autonomia Tecnológica em 2026*. Comparar a Utopia (líder de IA Verde com Lítio e Nióbio) versus a Distopia.

### 5. As Alucinações da IA (O Estudo de Caso de Comportamento Emergente)
- Dedique 1 ou 2 slides para o fenômeno técnico observado: **Colapso de Contexto nos Modelos Locais (Ollama)**.
- Mostre como o `Auditor` entrou em um *loop infinito* a partir da Rodada 10, julgando a saúde pública e a educação com base em "Bases Militares da 2ª Guerra Mundial e a resistência da Grã-Bretanha".
- Mostre o delírio do `Cético` ao afirmar que "a Vale do Rio Doce fez parceria com a Volks para fabricar peças de carros em 1999".
- Explique o valor disso para o trabalho: como os modelos open-source menores falham em simulações extensas (*Long-Context Window*) e por que a arquitetura com o Verificador de Fatos (Antigravity) consertando a "memória" rodada a rodada salvou a simulação.

### 6. Os Grandes Pontos de Virada (Turning Points)
- Escolha os momentos onde o Brasil de "Utopia" superou a armadilha do Brasil Real:
  - **Abolição e Terras (1850-1888)**: Reforma agrária antecipada via Engenheiros Negros (André Rebouças) vs o latifúndio real.
  - **As Ferrovias (Anos 50)**: Escolha pelos trilhos vs o Rodoviarismo de JK.
  - **Soberania vs Doença Holandesa (Anos 2000)**: Trocar minério cru por trens-bala e IA com a China, com Fundo Soberano bancando Renda Básica.

### 7. Conclusão da Disciplina
- Resumo de como a simulação LLM serve para Planejamento Estratégico Estatal.
- O futuro do Brasil: Como as escolhas do presente (PBIA, COP30) moldam se caminhamos para a Utopia ou para a Distopia.
- Referências Bibliográficas (livros e dados citados nas 20 rodadas de `knowledge/`).

---

**Nota Final ao Claude:**
Seja visual, dinâmico e use uma linguagem engajadora e acadêmica ao mesmo tempo. Você está apresentando este slide a uma banca de mestrado/doutorado em "Tópicos Avançados em Inteligência Artificial". Gere o código LaTeX (Beamer) completo ou Marp Markdown para os slides, de ponta a ponta!
