---
name: overleaf-latex
description: Gerencia projetos LaTeX locais e sincronização Git com Overleaf sem destruir templates oficiais, validando referências cruzadas, BibTeX 7-bit, tabelas e compilação.
---

# Overleaf & LaTeX Engineering

## Fluxo Obrigatório de Edição
1. **Inspecionar Projeto:** Identifique `main.tex`, classe (`.cls`), estilo bibliográfico (`.bst`), pacotes e pastas (`sections/`, `figures/`, `tables/`). Nunca substitua o template oficial silenciosamente.
2. **Planejar Alteração:** Liste exatamente quais arquivos serão editados e por quê.
3. **Editar Incrementalmente:** Preserve estrutura modular, use labels semânticos (`sec:`, `tab:`, `fig:`) e garanta acentuação 7-bit (`{\'a}`, `{\~a}`, `{\c{c}}`) em `references.bib` quando usar `splncs04.bst`.
4. **Validar via Script (Quality Gate):**
   Execute o validador antes de qualquer commit ou entrega:
   `python .agents/skills/overleaf-latex/scripts/validate_latex_project.py <caminho_projeto_latex>`
5. **Compilar e Inspecionar:** Se `pdflatex`/`bibtex` estiverem disponíveis localmente, compile (`pdflatex -> bibtex -> pdflatex -> pdflatex`) e verifique o PDF; caso contrário, registre no `compilation-audit.md` que a checagem estática passou e instrua o *Recompile* no Overleaf.
6. **Git & Segurança Overleaf:** Nunca grave tokens (`olp_...`) em arquivos nem os deixe persistidos em `.git/config` ao final da operação.
