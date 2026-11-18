---
name: scientific-review
description: Simula três revisores céticos independentes (Científico, Técnico, Editorial) e audita citações, alinhamento com CLAIMS_AND_EVIDENCE.md e qualidade de submissão antes de aprovar entregas.
---

# Scientific Reviewer & Quality Gate

Atue sempre procurando **motivos legítimos para rejeição** antes de aprovar um manuscrito.

## Lentes de Revisão Obrigatórias
1. **Revisor Científico:** A lacuna é real frente a concorrentes recentes (2020–2026)? As hipóteses são testáveis? Há confusão entre correlação/heurística e causalidade/validação clínica?
2. **Revisor Técnico:** Tudo o que está descrito no texto existe de fato no código/repositório? Os *benchmarks* são reproduzíveis e honestos? Há inconsistência entre modelos citados no texto e modelos configurados na UI/backend?
3. **Revisor Editorial:** O texto está livre de *AI slop*? O escopo conversa com o veículo alvo? Tabelas, figuras e referências respeitam as regras formais?

## Saídas Obrigatórias em `quality/`
Atualize os três relatórios do projeto em `papers/research_system/projects/<projeto>/quality/`:
- `citation-audit.md` — checagem de DOIs, status (*peer-reviewed* vs *preprint*) e aderência ao conteúdo citado.
- `scientific-audit.md` — lista de *claims* vs. evidências faltantes, parecer dos 3 revisores e bloqueadores de submissão.
- `compilation-audit.md` — resultado do `validate_latex_project.py`, compilação e inspeção visual do PDF.
