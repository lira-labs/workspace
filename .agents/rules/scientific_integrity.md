---
name: scientific-integrity
trigger: model_decision
description: Regras obrigatórias de integridade científica, verificação de fontes primárias e controle anti-alucinação via CLAIMS_AND_EVIDENCE.md ao pesquisar ou redigir artigos científicos.
---

# Integridade Científica & Memória de Evidências

1. **Zero Fabricação:** Nunca invente referências, DOIs, autores, amostras, métricas, resultados experimentais ou capacidades de software.
2. **Fontes Primárias Obrigatórias:** Toda citação inserida em `references.bib` ou no manuscrito deve ter título, autores, ano, veículo e DOI/URL verificados em fonte primária; nunca cite um trabalho apenas pelo título sem confirmar que o conteúdo sustenta a afirmação.
3. **Diferenciação de Status:** Separe explicitamente artigos revisados por pares (*peer-reviewed*), *preprints* (arXiv), relatórios técnicos, projetos *open-source* e produtos comerciais.
4. **Fonte Única da Verdade (`CLAIMS_AND_EVIDENCE.md`):**
   - Antes de redigir ou revisar qualquer seção de um projeto em `papers/research_system/projects/<projeto>/`, leia `PROJECT_BRIEF.md` e `CLAIMS_AND_EVIDENCE.md`.
   - **Nunca converta funcionalidade implementada em eficácia experimental comprovada** (ex.: existir heurística de desvio de olhar no código não prova detecção validada de smartphone ou redução de fadiga sem estudo empírico).
   - Quando faltar evidência, registre explicitamente a lacuna ou marque `% TODO` / `[PENDENTE DE MEDIÇÃO]`.
