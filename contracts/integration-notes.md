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
   - Exibição de lotação e tempo previsto calibrado com as incertezas da via.
3. **Estado Vazio (`Empty State`):**
   - Mensagem clara com ação orientadora (ex: *"Nenhum ônibus em trânsito no trecho rural no momento. Consulte o horário tabelado ou selecione outra linha."*).
4. **Erro Tratado (`Error State`):**
   - Mensagem explicativa em linguagem humana e botão explícito *"Tentar Novamente"*.
5. **Dados Parciais / Alerta de Trava Híbrida (`Partial Data / Trava Híbrida Defensiva`):**
   - Quando $|T_{\text{STGCN}} - T_{\text{GPS}}| > 15\text{ min}$, a interface ativa o selo amarelo `[?]` de anomalia viária.
   - O Frontend oculta a previsão teórica da GNN e prioriza a telemetria GPS bruta comprovada.
   - Ponderação de Yap & Cats (2021) de 1,68x é acionada na presença de queima de parada ou superlotação, alertando o usuário sobre a dilatação psicológica da espera.

---

## 3. Diretriz de Preservação de Artefatos Oficiais
- Todo deploy para produção ou homologação é estritamente condicionado à presença intacta da apresentação de slides oficial da banca examinadora (`GrafoParada_Seminario2_CauaLira.pptx`).
- O gatekeeper `pre_flight_check.py` aborta imediatamente se o deck não for encontrado ou se tiver tamanho inferior a 1 MB.
