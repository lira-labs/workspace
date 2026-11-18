---
name: scientific-writing
description: Orienta escrita científica argumentativa sem AI slop em Português e Inglês para Human-Centered AI in Education (SIGCSE, EAAI/AAAI, IJCAI). Use ao redigir ou revisar seções de manuscritos.
---

# Scientific Writing & Argumentation

Consulte também [references/scientific-writing-benchmark.md](./references/scientific-writing-benchmark.md) para exemplos de estilo e anti-padrões.

## Ordem Obrigatória Antes de Escrever
1. Leia `PROJECT_BRIEF.md`, `CLAIMS_AND_EVIDENCE.md`, `research_questions.md` e `literature-matrix.csv`.
2. **Regra da Introdução por Último:** Nunca redija ou reescreva a Introdução antes de consolidar mapa de evidências, concorrentes, RQs e metodologia.

## Regras de Argumentação por Seção
- **Resumo / Abstract:** Contexto específico -> lacuna mensurável -> arquitetura/método -> escopo real da avaliação (nunca prometa resultados que ainda não existem).
- **Introdução (Funil):** Relevância do problema com citações primárias -> falha das abordagens atuais -> hipótese/contribuição verificável -> roteiro das seções (`\ref{sec:...}`).
- **Trabalhos Relacionados:** Organize por **4 eixos temáticos** (nunca uma lista sequencial de resumos). Feche com uma **tabela comparativa** objetiva (`\checkmark`, `$\sim$`, `--`) e uma tese integradora.
- **Método / Arquitetura:** Descreva exatamente o que o sistema implementa (sem inflar heurísticas como "modelos profundos" ou protótipos como "validados").
- **Disciplina de Parágrafo:** Todo parágrafo deve ter função argumentativa explícita (mecanismo, evidência, contraste ou limite). Remova frases genéricas de preenchimento.
