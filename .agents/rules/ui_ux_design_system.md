---
description: Diretrizes obrigatórias de UI/UX e prevenção de AI Slop para o front-end do GrafoParada.
---

# GrafoParada UI/UX Director Rules

Antes de editar ou criar telas em `code/grafoparada_web/`:

1. **Consultar Referências:** Leia `design-references/README.md` e `design-references/ui-tokens.json`.
2. **Separação de Contexto (3 Ambientes):**
   - Nunca misturar botões acadêmicos/UFRPE/PPTX dentro da UI do passageiro (`#app-shell` e barra principal do passageiro). Tudo de pesquisa/banca vive exclusivamente no ambiente **Laboratório (`lab`)**.
   - A Central CTM vive no ambiente **Central CTM (`ctm`)** com foco em KPIs operacionais, alocação de frota por faixa horária e confiança da previsão.
3. **Proibição de AI Slop:**
   - **Zero emojis como ícones corporativos/UI** em abas, chips de barra, títulos de cards e botões de ação: use ícones SVG vetoriais (`1.75px` stroke).
   - **Zero cards dentro de cards** com bordas redundantes e sombras pesadas.
   - **Zero gradientes decorativos aleatórios** em botões comuns ou cabeçalhos secundários.
   - **Zero placeholders `--` ou `-- min` soltos:** todo dado ausente ou pendente deve apresentar estado explícito (carregando GPS, GPS negado com seleção manual, ou sem ônibus ao vivo com consulta de grade).
4. **Transparência Semântica Obrigatória:**
   - Toda métrica exibida ao usuário ou gestor deve deixar claro se é **Dado Real** (verde `#059669`), **Previsão ST-GCN** (roxo `#7C3AED`) ou **Simulação** (âmbar `#D97706`).
