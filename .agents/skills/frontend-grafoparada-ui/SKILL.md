---
name: frontend-grafoparada-ui
description: Use when implementing HTML, CSS, SVG icons, data provenance badges, or Leaflet UI flows inside code/grafoparada_web/. Keeps the UI aligned with GrafoParada tokens and avoids AI slop.
---

# GrafoParada Frontend Builder

Guia técnico para implementação limpa em `code/grafoparada_web/index.html` e `code/grafoparada_web/real_transit_engine.js`.

## Regras de Implementação
1. **Design Tokens & Tipografia**:
   - Consuma as variáveis de `:root` e `design-references/ui-tokens.json` (`Plus Jakarta Sans` para leitura, `monospace` tabular para minutos, linhas e KPIs).
   - Evite CSS inline redundante quando já existir classe semântica.
2. **Ícones & Semântica Visual**:
   - Proibido usar emojis em botões, abas, pills, títulos de cards ou controles de mapa. Utilize `<svg class="gp-svg" viewBox="0 0 24 24">` com `stroke="currentColor"` (`1.75px`).
   - Sempre classifique dados com os selos semânticos:
     - `.gp-badge-real`: dado real (`GTFS` / `Cittamobi`)
     - `.gp-badge-pred`: previsão do modelo (`ST-GCN`)
     - `.gp-badge-sim`: simulação / cenário operacional
     - `.gp-badge-alert`: incidente / lotação crítica
3. **Separação das 3 Visões**:
   - Controle o escopo via `setAppMode('passenger' | 'ctm' | 'lab')`. Elementos acadêmicos e PPTX não podem aparecer na tela do passageiro.
4. **Protagonismo do Mapa & Progressive Disclosure**:
   - No modo Radar/Mapa (`#app-screen-radar`), mantenha `.mobile-bottom-sheet` compacta (`max-height: 205px` em repouso) e legenda discreta (`#map-floating-legend`).
   - Ferramentas secundárias na Home ficam recolhidas em `<details>` e modais específicos.
5. **Segurança & Contrato**:
   - Todo texto vindo de busca, rota, parada ou API deve passar por `escapeHtml` ou `textContent` (nunca HTML cru sem sanitização).
   - Preserve IDs e atributos `toolname` exigidos por `pre_flight_check.py` e `test_e2e_e_motor.py`.
