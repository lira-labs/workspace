# Academic Research & Scientific Writing System

Sistema modular de pesquisa científica, escrita argumentativa e engenharia LaTeX/Overleaf integrado ao workspace do Antigravity.

## Arquitetura de Camadas
- **Regras Persistentes (`.agents/rules/`):** `scientific_integrity.md` e `academic_writing_and_hcai.md`.
- **Skills Especializadas (`.agents/skills/`):** `academic-research`, `scientific-writing`, `research-methodology`, `overleaf-latex` (com `scripts/validate_latex_project.py`), `scientific-review` e `venue-adaptation`.
- **Subagentes Compartilhados (`.agents/agents/`):**
  - `academic-researcher` (literatura, DOIs, `literature-matrix.csv`)
  - `methodology-reviewer` (RQs, protocolo experimental, auditorias em `quality/`)
  - `scientific-writer` (redação argumentativa em `.tex` vinculada a `CLAIMS_AND_EVIDENCE.md`)
  - `latex-overleaf-engineer` (estrutura LaTeX, BibTeX 7-bit, compilação e sincronização Git/Overleaf)
- **Base de Conhecimento & Templates (`knowledge/`, `templates/`):** diretrizes conceituais de Human-Centered AI in Education, protocolos e checklists.
- **Memória Científica por Projeto (`projects/<nome>/`):** `PROJECT_BRIEF.md`, `CLAIMS_AND_EVIDENCE.md`, `research_questions.md`, `literature-matrix.csv` e `quality/`.

## Fluxo Obrigatório de Produção (Níveis 1 a 5)
1. Atualizar `PROJECT_BRIEF.md` e `CLAIMS_AND_EVIDENCE.md`.
2. Consolidar `literature-matrix.csv` com fontes primárias verificadas.
3. Definir `research_questions.md` e o protocolo experimental antes de redigir a Introdução.
4. Redigir/revisar o manuscrito-base (PT-BR ou EN) no repositório local conectado ao Overleaf.
5. Rodar `validate_latex_project.py` + revisão cética em `quality/` antes de submeter ou adaptar ao template final (SIGCSE / EAAI / IJCAI).
