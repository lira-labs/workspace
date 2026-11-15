# Workflow: Desenvolvimento Frontend Anti-AI-Slop (Explore -> Spec -> Execute -> Verify)

Use este fluxo sempre que for criar ou refatorar qualquer tela ou componente do GrafoParada (`code/grafoparada_web/`).

## Etapa 1 · Explore & UI Spec (`ux-spec-planner`)
- Carregue a skill `.agents/skills/frontend-ux-spec/SKILL.md`.
- Leia o trecho exato dos arquivos afetados + `design-references/README.md` + `design-references/ui-tokens.json`.
- Consulte referências reais no **Mobbin** quando precisar comparar hierarquia ou fluxos equivalentes.
- **Saída obrigatória antes de codificar:** mini-spec com ambiente (`passenger` | `ctm` | `lab`), ação primária, 5 estados e lista de arquivos/IDs.

## Etapa 2 · Implementação Isolada (`frontend-layout-ui` + `frontend-map-engine`)
- Carregue `.agents/skills/frontend-grafoparada-ui/SKILL.md`.
- `frontend-layout-ui` implementa estrutura HTML/CSS, ícones `.gp-svg`, selos `.gp-badge-*` e estados vazios/erro.
- `frontend-map-engine` implementa lógica JS em `real_transit_engine.js` respeitando os IDs e sanitização XSS.

## Etapa 3 · Gatekeeper Técnico (`qa-gatekeeper`)
- Rode com `$env:PYTHONUTF8="1"`:
  - `uv run --project code/grafoparada_tec python code/grafoparada_tec/pre_flight_check.py` (40/40)
  - `uv run --project code/grafoparada_tec pytest code/grafoparada_tec/test_e2e_e_motor.py code/grafoparada_tec/test_unitarios_cientificos.py -v` (26/26)

## Etapa 4 · Crítica Visual Independente (`visual-design-critic`)
- Carregue `.agents/skills/visual-critic-audit/SKILL.md`.
- Rode o auditor CDP (`audit_ui_cdp.py`) em Mobile (`390x844`) e Desktop (`1280x800`).
- Leia as capturas PNG geradas e corrija qualquer defeito antes do merge na `main`.

## Etapa 5 · Handoff & Deploy Contínuo
- Atualize `HANDOFF.md`, faça commit em `feature/grafoparada-dev`, promova via `--no-ff` para `main` e confirme o auto-deploy em `https://grafoparadaweb.vercel.app`.
