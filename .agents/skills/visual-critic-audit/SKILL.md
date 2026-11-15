---
name: visual-critic-audit
description: Use after any frontend change in code/grafoparada_web/ to capture real Chrome screenshots in Mobile (390x844) and Desktop (1280x800), verify zero horizontal overflow or console errors, and run a skeptical anti-AI-slop review.
---

# Visual Critic & Browser Audit

Nunca aprove uma mudança de interface apenas lendo código ou por `exit code 0`. Inspecione o navegador real.

## Passos Obrigatórios
1. Suba um servidor HTTP local em `code/grafoparada_web` (porta livre, ex.: `8767`):
   `uv run python -m http.server 8767`
2. Execute o auditor CDP incluído nesta skill:
   `.\.venv\Scripts\python.exe .agents/skills/visual-critic-audit/scripts/audit_ui_cdp.py --url http://127.0.0.1:8767/index.html --out-dir <pasta_saida>`
3. Abra e inspecione visualmente os PNGs gerados (`read_file` nas imagens) aplicando o checklist abaixo.

## Checklist de Reprovação Automática
- **Overflow Horizontal**: `overflowX > 0` em qualquer tela (`390x844` ou `1280x800`) reprova imediatamente.
- **Erros em Execução**: `consoleErrors > 0` ou `jsExceptions > 0` reprova imediatamente.
- **Sobreposição / Recorte**: textos cortados, badges em cima de ícones de ônibus ou botões cobrindo legenda/bottom sheet.
- **Sinais de AI Slop**: cards aninhados sem função, emojis soltos no lugar de SVG, placeholders `-- min` ou `-- assentos`, mistura de textos de banca na UI do passageiro.
- **Contraste & Leitura**: texto ilegível sobre mapa ou fundo claro/escuro.

Se encontrar qualquer defeito, devolva diagnóstico exato (arquivo, seletor, viewport e descrição do bug visual) antes de liberar o merge.
