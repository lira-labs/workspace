# 📊 Modelo de Dados Compartilhado (Data Model) · GrafoParada
> Fonte única da verdade entre GNN Espaço-Temporal (Backend), Central SICOE/CTM e App Mobile/Laya IA (Frontend).
> Em estrita conformidade com a literatura A1 de Abandono (*Passenger Reneging*) e Valoração Psicológica de Espera.

---

## 1. Entidades de Domínio da Rede Metropolitana

### `Route` (Linha do Sistema GTFS Metropolitano)
Representa um serviço regular do Consórcio de Transporte Metropolitano (CTM Grande Recife).
- `route_code` (`string`, obrigatório): Identificador numérico ou alfanumérico oficial (ex: `"199"`, `"522"`, `"2040"`, `"060"`).
- `route_label` (`string`, obrigatório): Nome comercial completo (ex: `"199 - Camela / TI Cabo via PE-60"`).
- `agency` (`string`, obrigatório): Concessionária operadora (ex: `"São Judas Tadeu (SJT) · CTM Grande Recife"`, `"Borborema"`, `"Consórcio Conorte"`).
- `direction` (`string`, opcional): Sentido operacional da linha (`"IDA"` ou `"VOLTA"`).
- `corridor_id` (`string`, obrigatório): Código identificador do eixo viário metropolitano (ex: `"pe60_camela_cabo"`, `"eixo_caxanga"`, `"norte_sul"`).
- `shape_id` (`string`, opcional): Identificador do traçado vetorial georreferenciado no GTFS (ex: `"199-392-2"`).
- `stops_count` (`integer`, opcional): Quantidade total de paradas cadastradas no traçado.
- `active` (`boolean`, default: `true`): Flag de atividade da linha no catálogo em tempo real.

### `Stop` (Nó Topológico da Rede Viária / Parada de Ônibus)
Nó físico do grafo com telemetria multimodal e predições espaciais integradas.
- `stop_id` (`string`, obrigatório): Código físico de 6 dígitos homologado pelo CTM (ex: `"030613"`).
- `name` (`string`, obrigatório): Topônimo de referência e logradouro (ex: `"Praça Pedro Serafim (Terminal de Camela)"`).
- `lat` (`number`, float64, obrigatório): Latitude WGS84 (ex: `-8.514888`).
- `lon` (`number`, float64, obrigatório): Longitude WGS84 (ex: `-35.123539`).
- `wait_gps_min` (`number`, float, obrigatório): Tempo de espera bruto medido diretamente pelos sensores AVL/GPS dos veículos ativos.
- `stgcn_horizon_min` (`array[number]`, float): Vetor multi-horizonte inferido pelo bloco ST-GCN `[T+10, T+20, T+30]` minutos.
- `perceived_wait_min` (`number`, float): Tempo de espera com penalidade psicológica ponderada (1,68x) segundo Yap & Cats (2021).
- `reneging_risk_pct` (`number`, float 0-100): Probabilidade estimada de abandono de espera segundo modelo de Kim et al. (2026).
- `crowd_level` (`integer`, 1-4): Grau de lotação física do coletivo (`1: Sentado Garantido`, `2: Lotação Leve`, `3: Em Pé Confortável`, `4: Superlotado / Risco Denied Boarding`).
- `crowd_status` (`string`): Rótulo textual e visual de lotação (ex: `"🟢 Sentado Garantido"`, `"🟠 Lotação Alta"`, `"🔴 Superlotado"`).
- `latent_demand_est` (`number`, float): Demanda latente não-censurada estimada pelo motor convolucional $\hat{D}$.
- `latent_demand_ci` (`array[number]`): Intervalo de Confiança Conformal de 90% para a demanda latente $\hat{D} \in [D_{\min}, D_{\max}]$.
- `operational_state` (`string`, enum: `["REGULAR", "WARNING", "CRITICAL"]`): Estado operacional da parada.
- `emergency_lock` (`boolean`): Flag que indica se a Trava Híbrida Defensiva anti-oversmoothing está ativada neste nó.
- `discrepancy_delta` (`number`, float): Desvio absoluto $|T_{\text{STGCN}} - T_{\text{GPS\_Bruto}}|$ medido no nó.

---

## 2. Modelos Preditivos e Lógica Científica Qualis A1

### `PerceivedWaitModel` (Penalidade Psicológica · Yap & Cats, 2021)
Baseado no estudo seminal *Taking the path less travelled: Valuation of denied boarding in crowded public transport systems* (TR Part A, 2021):
- **Equação Canônica:**
  $$T_{\text{percebido}} = \beta_{\text{denied}} \times T_{\text{espera}}$$
- **Parâmetros:**
  - $\beta_{\text{denied}} = 1,68$ quando ocorre superlotação crítica ou recusa de embarque (*denied boarding* / queima de parada).
  - $\beta_{\text{denied}} = 1,00$ em condições nominais de operação regular.
- **Justificativa Operacional:** O tempo de espera após ser impedido de embarcar ou aguardar sob incerteza extrema impõe uma desutilidade percebida 68% superior ao tempo cronológico do relógio.

### `PassengerRenegingModel` (Evasão da Espera · Kim et al., 2026)
Formalizado a partir de *City-scale unmet bus demand modeling with passenger reneging behavior* (Journal of Public Transportation, 2026) e *Tan & Ramli (2024)*:
- **Equação Canônica:**
  $$P(\text{Reneging} \mid t) = \frac{1}{1 + e^{-k \cdot (t - \tau)}}$$
- **Parâmetros e Variáveis:**
  - $t$: Tempo de espera acumulado ou previsto (cronológico ou percebido via Yap & Cats).
  - $\tau = 15,0 \text{ min}$: Limiar mediano de tolerância de espera do passageiro metropolitano na PE-60.
  - $k = 0,25 \text{ min}^{-1}$: Coeficiente de elasticidade e sensibilidade de desistência.
- **Impacto no Sistema:** A demanda não desaparece; ela se evade para transportes clandestinos, moto-táxis ou volta para casa. O GrafoParada quantifica essa evasão para permitir intervenção antes que a desistência ocorra.

### `TravaHibridaDefensiva` (Mecanismo Anti-Oversmoothing)
Mecanismo de blindagem operacional contra as distorções inerentes às Convoluções em Grafos (ST-GCN):
- **Equação Canônica:**
  $$\Delta = |T_{\text{STGCN}} - T_{\text{GPS\_Bruto}}|$$
- **Regra de Decisão:**
  - Se $\Delta > 15,0 \text{ min}$:
    - `emergency_lock = true`
    - A interface do passageiro corta imediatamente a previsão suavizada da ST-GCN.
    - Exibe o selo amarelo de anomalia viária `[?]`.
    - Força a exibição prioritária da telemetria GPS bruta e dispara alerta de áudio sênior.
  - Se $\Delta \le 15,0 \text{ min}$:
    - `emergency_lock = false`
    - Exibe a projeção estabilizada da ST-GCN em conformidade com o histórico espaço-temporal.

### `EmergencyDispatchAction` (Despacho Ativo & Mitigação de Deadheading)
Decisão autônoma da Central SICOE/CTM para remanejamento de veículos:
- **Critério de Disparo:**
  $$\text{Disparar} \iff P(\text{Reneging}) \ge 80\% \quad \land \quad \text{Ocupação}_{\text{contra-fluxo}} \le 15\%$$
- **Resultado Operacional:**
  - Inserção de veículo ocioso no contra-fluxo para resgate da parada antes do reneging.
  - Economia de combustível fóssil estimada em 14 litros de diesel por ciclo ao eliminar viagens ociosas no vazio (*deadheading*).

---

## 3. Rotinas Pessoais e Privacidade On-Device

### `RoutineSchedule` (Perfil Pendular do Passageiro)
Persistido exclusivamente no dispositivo do usuário (`localStorage`), sem transmissão de dados nominais para servidores.
- `preset_id` (`string`): Identificador do turno (`"industria_suape"`, `"comercio_centro"`, `"estudante_universitario"`, `"plantao_saude"`).
- `target_time` (`string`, formato `"HH:MM"`): Horário fixo de entrada no destino.
- `walking_time_min` (`integer`): Tempo de caminhada até a parada de embarque.
- `transit_eta_min` (`integer`): Tempo projetado de deslocamento no coletivo via ST-GCN.
- `departure_window` (`string`, formato `"HH:MM"`): Janela segura de saída calculada ($\text{target\_time} - \text{walking\_time} - \text{transit\_eta} - 1\text{ min}$).
- **Garantia LGPD:** Volume total de 166 bytes em armazenamento local isolado.

---

## 4. Artefatos Oficiais de Apresentação e Auditoria Docente

### `OfficialPresentationArtifact` (Deck Oficial da Banca)
- `file_path`: `code/grafoparada_web/GrafoParada_Seminario2_CauaLira.pptx`
- `format`: PowerPoint Widescreen 16:9 (`.pptx`)
- `min_size_bytes`: 1.000.000 bytes (~13 MB real)
- `rule`: Bloqueio terminante de deploy ou merge para branch `main` caso o arquivo inexista ou esteja corrompido, garantindo disponibilidade contínua do seminário acadêmico para avaliação docente e acesso público.
