---
name: frontend-ux-spec
description: Use before creating or redesigning any screen, modal, or flow in GrafoParada. Enforces the Explore -> Spec -> Plan workflow (Beyond Vibe Coding) and extracts real UX patterns before any code is edited.
---

# Frontend UX Spec & Anti-Vibe-Coding

Nunca escreva HTML, CSS ou JS diretamente a partir de um pedido vago. Siga esta sequência obrigatória:

## 1. Explore (Somente Leitura)
1. Leia `design-references/README.md`, `design-references/ui-tokens.json` e `contracts/api-contract.yaml`.
2. Inspecione os arquivos alvo em `code/grafoparada_web/` com busca localizada (`Select-String` / `read_file` com intervalo).
3. Se o plugin Mobbin estiver disponível na sessão, pesquise referências reais de telas equivalentes para comparar densidade, hierarquia e estados vazios (sem copiar literalmente).

## 2. Spec da Tela (Contrato Visual)
Antes de editar código, redija uma especificação curta (máx. 25 linhas) respondendo:
- **Ambiente (`data-app-mode`)**: `passenger` (B2C no ponto), `ctm` (B2B operacional) ou `lab` (banca/pesquisa). Nunca misture contextos.
- **Pergunta primária da tela**: o usuário entende em 2 segundos *onde está -> qual ação principal fazer -> o que vem depois*?
- **Componentes corretos**: tabela para listas densas, mapa para geografia, barra comparativa para métricas, formulário para entrada. Proibido empilhar cards dentro de cards.
- **Os 5 Estados Obrigatórios**:
  1. `Loading`: estado explícito de carregamento (nunca `-- min`).
  2. `Success`: dados reais ou previsão claramente rotulada.
  3. `Empty`: orientação prática e botão de ação manual.
  4. `Error`: falha amigável + tentativa de recuperação.
  5. `Partial`: GPS desligado ou ônibus sem telemetria ao vivo -> fallback para grade GTFS.

## 3. Plan & Critérios de Reprovação
Liste os arquivos exatos que serão tocados, seletores/IDs preservados pelos testes e critérios visuais que o `visual-design-critic` deverá validar em `390x844` e `1280x800`.
