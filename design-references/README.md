# GrafoParada · Design References & Anti-AI-Slop Architecture

> **Regra Central:** Antes de implementar qualquer tela ou componente no GrafoParada, consulte este diretório e `ui-tokens.json`. Nenhuma interface deve parecer genérica ou "feita por IA". Cada elemento deve ter uma função clara ligada à jornada do usuário.

---

## 1. Benchmark de Referências Profissionais

| Ambiente | Referências Reais | Padrões Extraídos (Sem Cópia Literal) |
| :--- | :--- | :--- |
| **Passageiro (Mobile First)** | Mobbin (Citymapper, Transit, Uber, Google Maps) | Mapa como protagonista (`>60%` do viewport), bottom sheet compacto em repouso, **uma ação primária óbvia**, progressive disclosure para fluxos secundários, tipografia com contraste claro. |
| **Central CTM (B2B Ops)** | Refero / Nicely Done (Samsara, Datadog, Linear, Uber Fleet) | Faixa superior de KPIs numéricos densos (`Monospace`), gráfico comparativo visual de Pico vs. Fora de Pico, lista de alertas priorizados com nível de confiança e ação de 1 clique. |
| **Laboratório / Pesquisa (UFRPE)** | Vercel / Radix / Notion Academic Docs | Isolado fora da navegação do passageiro; agrupa deck PPTX, slides web, roteiro, arquitetura GTFS + ST-GCN, auditoria WCAG e metodologia sem poluir a tela de uso real. |

---

## 2. Os 7 Pilares do Refactor UI/UX (Checklist Obrigatório)

1. **Separação Estrita em 3 Ambientes (`data-app-mode`):**
   - `passenger`: Tela focada 100% no passageiro no ponto de ônibus. Zero menção a banca UFRPE, PPTX ou roteiro.
   - `ctm`: Central de Operações Metropolitana (B2B) — alocação de frota, pico vs. ociosidade, alertas de corredor.
   - `lab`: Espaço da Banca / Pesquisa — slides PPTX/Web, roteiro de apresentação, origem dos dados e acessibilidade.
2. **Tela Principal com Progressive Disclosure (`#app-screen-home`):**
   - Responde imediatamente: *Onde estou → Qual linha preciso → Quando chega → O que faço agora*.
   - Ações secundárias (Guia de Perdido, Segurança, 44 Terminais SEI) ficam acessíveis sem competir com a ação primária.
3. **Design System Coeso & Ícones SVG:**
   - Proibido usar emojis decorativos como ícones de interface em tabs, chips, botões e títulos técnicos. Utilizar exclusivamente ícones SVG `stroke="currentColor"` (`1.75px`, `16px–20px`).
   - Tipografia única (`Plus Jakarta Sans` / `Inter`) + `JetBrains Mono` / `monospace` tabular para tempos (`min`), códigos de parada e métricas CTM.
4. **Mapa como Protagonista (`#mobile-map`):**
   - Ocupa o máximo de altura no modo Radar/Mapa ao Vivo; legenda discreta flutuante (`Embarque`, `Caminhada`, `Trajeto`); marcador de embarque distinto da rota completa; botão dedicado de centralizar GPS.
5. **Transparência de Dados (Semântica Real vs. Previsão vs. Simulação):**
   - `.badge-real` (`#059669`): Dado Real · GTFS / Cittamobi
   - `.badge-pred` (`#7C3AED`): Previsão · ST-GCN
   - `.badge-sim` (`#D97706`): Simulação Operacional
   - `.badge-alert` (`#DC2626`): Alerta / Incidente
6. **Central CTM Orientada a Decisão Operacional:**
   - Substituir textões por KPIs objetivos, barras comparativas Pico vs. Fora de Pico (`10h–14h: 3 embarques` vs `Pico: 44–52 pass.`), índice de confiança e botão de simulação/aplicação imediata.
7. **Estados Reais de Carregamento, GPS Negado e Sem Veículo (Zero `--` solto):**
   - Nunca exibir `-- min` ou `--` cru sem contexto. Tratar explicitamente: `Procurando GPS...`, `GPS indisponível -> Escolher parada manualmente`, `Sem veículo ao vivo -> Ver horários programados`.
