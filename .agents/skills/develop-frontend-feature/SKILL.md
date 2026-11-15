---
name: develop-frontend-feature
description: Orquestra o ciclo completo de interface do GrafoParada (Explore -> Spec/Design -> Execute -> Verify -> Visual Review) acionando automaticamente os subagentes especializados de .agents/agents/. Use ao criar ou refatorar qualquer tela em code/grafoparada_web/.
---

# Pipeline Multiagente de Frontend · GrafoParada

Orquestre este ciclo de 5 etapas sem pular a especificação visual nem a revisão independente:

1. **Explore & Spec (`ux-spec-planner`)**
   - Carregue `frontend-ux-spec`.
   - Leia `design-references/README.md`, `ui-tokens.json`, `contracts/api-contract.yaml` e consulte referências no **Mobbin** ou **Figma** antes de desenhar.
   - Entregue mini-spec com ambiente (`passenger` | `ctm` | `lab`), ação primária, 5 estados e critérios de reprovação.
2. **Execução Isolada (`frontend-layout-ui` + `frontend-map-engine`)**
   - Carregue `frontend-grafoparada-ui`.
   - `frontend-layout-ui` implementa HTML/CSS, `.gp-svg` e `.gp-badge-*` em `code/grafoparada_web/index.html`.
   - `frontend-map-engine` implementa Leaflet/GTFS/Laya/XSS-safe DOM em `code/grafoparada_web/real_transit_engine.js`.
3. **Verificação Técnica (`qa-gatekeeper`)**
   - Execute `pre_flight_check.py` (40/40) e `pytest` (26/26). Nunca declare conclusão sem evidência executada.
4. **Crítica Visual Independente (`visual-design-critic`)**
   - Carregue `visual-critic-audit` e execute `.agents/skills/visual-critic-audit/scripts/audit_ui_cdp.py` em `390x844` e `1280x800`.
   - Abra os PNGs gerados e valide contraste, overflow zero, ausência de AI slop e separação real vs. simulação. Itere se houver qualquer defeito.
5. **Handoff & Deploy Contínuo**
   - Atualize `HANDOFF.md`, faça commit em `feature/grafoparada-dev`, promova via `--no-ff` para `main` e confirme o deploy automático em `https://grafoparadaweb.vercel.app`.
