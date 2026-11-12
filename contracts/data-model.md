# 📊 Modelo de Dados Compartilhado (Data Model)
> Fonte única da verdade entre GNN Espaço-Temporal (Backend) e App Mobile/Laya IA (Frontend).

---

## 1. Entidades Principais

### `Route` (Linha do Sistema)
- `route_code`: Identificador oficial da linha (ex: `"199"`, `"522"`, `"060"`).
- `route_label`: Nome comercial oficial (ex: `"199 - Camela / TI Cabo"`).
- `agency`: Operadora concessionária (ex: `"São Judas Tadeu (SJT) · CTM Grande Recife"`).
- `direction`: Sentido da viagem (`"IDA"` ou `"VOLTA"`).
- `corridor_id`: Eixo viário metropolitano (ex: `"pe60_camela_cabo"`).

### `Stop` (Nó Topológico da Rede / Parada)
- `stop_id`: Código oficial da parada no CTM (ex: `"030613"`).
- `name`: Nome legível de localização e referência (ex: `"Praça Pedro Serafim (Terminal de Camela)"`).
- `lat` / `lon`: Coordenadas geodésicas WGS84.
- `wait_gps_min`: Tempo de espera medido via telemetria GPS direta.
- `stgcn_horizon_min`: Vetor com horizontes previstos pela convolução em grafo `[T+1, T+2, T+3]`.
- `operational_state`: Estado operacional (`"REGULAR"`, `"WARNING"`, `"CRITICAL"`).
- `crowd_status`: Nível estimado de lotação (ex: `"🟢 Sentado Garantido"` ou `"🟠 Lotação Alta"`).

### `RoutineSchedule` (Rotina On-Device do Usuário)
- `preset_id`: Identificador de perfil rápido (`"casa"`, `"trabalho"`, `"faculdade"`).
- `target_time`: Horário planejado de chegada ao destino.
- `departure_window`: Horário seguro calculado para sair de casa a pé (`target_time - walking_time - transit_eta`).
- *Garantia LGPD:* Persistido exclusivamente em `localStorage` local (166 bytes); 0 bytes transmitidos para servidores externos.

### `TravaHibridaDefensiva` (Mecanismo Anti-Oversmoothing)
- `discrepancy_delta`: `|Previsão_STGCN - Telemetria_GPS_Bruta|`.
- `threshold`: 15 minutos.
- `action`: Se `discrepancy_delta > 15`, a interface corta a exibição da IA, exibe o alerta amarelo `[?]` e notifica o usuário por voz.
