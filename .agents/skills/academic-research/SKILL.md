---
name: academic-research
description: Conduz revisão bibliográfica verificada (ACM DL, IEEE Xplore, Springer, ScienceDirect, Scopus, Google Scholar), valida DOIs, classifica concorrentes e alimenta literature-matrix.csv antes da redação.
---

# Academic Research & Literature Intelligence

Use esta skill antes de redigir *Trabalhos Relacionados* ou adicionar qualquer nova referência bibliográfica.

## Procedimento
1. **Consultar Memória Existente:** Leia `papers/research_system/projects/<projeto>/literature-matrix.csv` para evitar buscas duplicadas.
2. **Buscar em Fontes Primárias:** Priorize trabalhos revisados por pares (2020–2026) sem excluir referências seminais anteriores. Busque em ACM DL, IEEE Xplore, Springer, ScienceDirect, PubMed e arXiv.
3. **Verificação Obrigatória de Conteúdo:**
   - Confirme título exato, lista completa de autores, veículo/ano, DOI ou URL oficial e tamanho de amostra ($N$).
   - **Regra de Ouro:** Nunca inclua uma referência apenas pelo título; confirme no resumo/texto que o estudo realmente sustenta a afirmação.
   - Classifique o status: `peer-reviewed`, `preprint`, `open-source`, `commercial` ou `wip`.
4. **Atualizar Matriz & BibTeX:**
   - Adicione uma linha completa em `literature-matrix.csv` (metodologia, amostra, achados, limitações, relação com o projeto).
   - Gere entrada BibTeX em formato 7-bit safe (acentos escapados com `{\'a}`, `{\~a}`, `{\c{c}}` etc.).
5. **Identificar Lacunas & Concorrentes-Alvo:** Destaque onde os concorrentes **superam** o sistema proposto antes de argumentar diferenciação.
