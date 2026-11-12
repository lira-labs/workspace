# 🔌 Notas de Integração & Estados da Interface (Integration Notes)
> Diretrizes para consumo de dados e tratamento de estados de UI sem AI Slop.

---

## 1. Regras de Integração Frontend ↔ Backend

1. **Zero Campos Inventados:**
   O Frontend não pode inventar propriedades que não constem em `api-contract.yaml` e `data-model.md`.
2. **Imutabilidade de Contrato:**
   O Backend não pode renomear chaves ou alterar tipos sem atualização prévia deste documento.
3. **Resiliência Offline / Falha de Rede:**
   O frontend mantém cache local em memória e `localStorage` para navegação contínua mesmo em pontos com sinal 3G/4G degradado na Rodovia PE-60.

---

## 2. Os 5 Estados Obrigatórios da Interface

Cada tela ou componente interativo DEVE tratar conscientemente:
1. **Carregando (`Loading / Skeleton`):**
   - Transição suave sem pulo de layout (*Layout Shift = 0*).
   - Indicador de leitura de telemetria sem spinners infinitos genéricos.
2. **Sucesso com Dados (`Success`):**
   - Renderização dos dados reais com hierarquia visual clara (destaque para métricas principais).
3. **Estado Vazio (`Empty State`):**
   - Mensagem clara com ação orientadora (ex: *"Nenhum ônibus em trânsito no trecho rural no momento. Consulte o horário tabelado ou selecione outra linha."*).
4. **Erro Tratado (`Error State`):**
   - Mensagem explicativa em linguagem humana e botão explícito *"Tentar Novamente"*.
5. **Dados Parciais / Alerta (`Partial Data / Stale`):**
   - Indicador de sinal fraco de satélite ou divergência com acionamento do selo de interdição `[?]`.
