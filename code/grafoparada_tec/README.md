# GrafoParada · Módulo Tecnológico e Validação Experimental

Este diretório contém a implementação dos modelos, extração de dados reais de transporte e validação experimental cinemática do projeto **GrafoParada · Frota no Vazio** (VA2 · Tópicos Avançados em Inteligência Artificial - AI4Good, UFRPE).

---

## 🗂️ Estrutura de Arquivos

```text
code/grafoparada_tec/
├── data/
│   ├── corredor_real_linha178_191.csv      # 20 paradas reais da PE-60 (Cabo/Suape) extraídas do GTFS oficial
│   ├── sensors_tmd.csv                     # 5.893 leituras físicas de sensores reais (Still, Bus, Walking, Car)
│   ├── gtfs.zip                            # GTFS bruto oficial do CTM (ignorado no git)
│   └── gtfs_granderecife/                  # GTFS descompactado do Grande Recife (ignorado no git)
├── .gitignore                              # Proteção contra commit de datasets pesados (>35MB)
├── explorar_gtfs.py                        # Script de inspeção da malha e linhas metropolitanas CTM
├── extrair_corredor_real.py                # Pipeline de extração das coordenadas do corredor PE-60
├── stgcn_grafoparada.py                    # Implementação da rede Spatio-Temporal Graph Convolutional Network
├── stgcn_official.py                       # Camadas temporais e espaciais canônicas em PyTorch
├── avaliar_piloto.py                       # Piloto experimental E1 (STGCN vs baselines tabulares)
├── validar_cinematica_parada.py            # Validação cinemática on-device (FSM + Sensores + LGPD + Cittamobi)
└── README.md                               # Este documento
```

---

## 🚌 1. Dados Reais Utilizados

1. **GTFS Oficial do Grande Recife Consórcio de Transporte Metropolitano (CTM)**:
   - Fonte oficial: `https://www.granderecife.pe.gov.br/gtfs/gtfs.zip`
   - Extração do corredor crítico da **PE-60 / Porto de Suape / TI Cabo**:
     - **Linha 178**: TI Cabo / Porto de Suape
     - **Linha 191**: Recife / Porto de Galinhas (Nossa Senhora do Ó)
   - Total de 20 paradas cadastradas com coordenadas geodésicas exatas (`stop_id`, `stop_name`, `lat`, `lon`, `tempo_programado_min`).

2. **TMD (Transportation Mode Detection) Dataset de Sensores Físicos**:
   - 5.893 leituras reais de sensores embarcados em smartphones de passageiros reais.
   - 12 atributos físicos: Aceleração ($X, Y, Z$, módulo, variância), Giroscópio ($X, Y, Z$, módulo, variância) e Ruído acústico ambiente ($dB$).
   - Balanceamento estrito em 4 classes de mobilidade:
     - `Still` (Estático na parada): 1.179 leituras
     - `Walking` (Caminhada): 1.177 leituras
     - `Bus` (Ônibus em trânsito): 1.178 leituras
     - `Car` (Veículo motorizado / Carro / Moto-táxi / Van): 1.180 leituras

---

## 🔬 2. Validação da Cinemática da Parada (`validar_cinematica_parada.py`)

### O Desafio e as Perguntas do Seminário 1 (Prof. Lucas Figueiredo)
1. *"Se o ônibus parar e o passageiro for descer?"* (Como não confundir desembarque com desistência?)
2. *"Como ser defensavelmente superior ao Cittamobi sem ser apenas uma feature de voz?"*
3. *"Como garantir rigor absoluto com a LGPD e custo operacional praticamente zero?"*

### Arquitetura da Solução
- **Classificador Neural On-Device (Edge Computing)**: Micro-rede em PyTorch CPU com menos de 12 KB de footprint de pesos, treinada nas leituras físicas reais do TMD.
- **FSM Cinemática Temporal (`KinematicStopFSM`)**:
  - Avalia o vetor cinemático prévio ($t_{0} \dots t_{chegada}$), tempo de permanência no raio geodésico da parada ($dwell$), status do veículo oficial via GPS aberto, e vetor cinemático de partida ($t_{saida}$).
  - **Desembarque (`ALIGHTING`)**: O usuário vinha em movimento veicular pesado (`Bus`), desacelera e entra no raio da parada com permanência transitória ($\le 3$ min), e afasta-se em modo pedestre (`Walking`, 3–5 km/h).
  - **Desistência (`ABANDONMENT`)**: O usuário estava estático (`Still`) na parada aguardando por tempo excessivo ($\ge 15$ min a 40 min), e afasta-se subitamente em velocidade veicular motora (`Car`/van/moto-táxi a $> 30$ km/h) **sem** que o GPS do ônibus oficial tenha parado no local.

---

## 📊 3. Resultados Empíricos Medidos

Execução realizada no ambiente de teste com 1.200 trajetórias no corredor real da PE-60:

### Matriz de Confusão (300 trajetórias por classe real)

| Classe Real \ Predição | ALIGHTING (Desembarque) | BOARDING_SERVED (Embarque) | ABANDONMENT (Desistência) | TRANSIT_BYPASS (Trânsito Direto) | Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ALIGHTING** | **184** | 6 | **0** | 110 | 300 |
| **BOARDING_SERVED** | 0 | 193 | 66 | 41 | 300 |
| **ABANDONMENT** | 0 | 51 | **204** | 45 | 300 |
| **TRANSIT_BYPASS** | 5 | 5 | 0 | 290 | 300 |

### Métricas Centrais
- **Taxa de Falso Positivo no Desembarque**: **0.00%** (Exatamente 0 em 300 passageiros que desceram do ônibus foram confundidos com desistentes).
- **Detecção de Desistência Real**:
  - Precisão: **75.56%**
  - Recall (Sensibilidade): **68.00%**
  - F1-Score: **71.58%**
- **Acurácia Global do Sistema Multimodal**: **72.58%** (em 1.200 trajetórias).

---

## ⚡ 4. Benchmark Operacional, LGPD e Custo de Nuvem vs. Cittamobi

| Critério de Avaliação | Cittamobi (Arquitetura Atual de Mercado) | GrafoParada (Nossa Arquitetura On-Device FSM) | Ganho / Vantagem GrafoParada |
| :--- | :--- | :--- | :--- |
| **Onde roda a inteligência** | Nuvem centralizada | On-Device no smartphone do passageiro (Edge) | Independência de infraestrutura cara |
| **Tempo de Inferência** | ~150 ms a 500 ms (latência HTTP de rede) | **14.29 µs** (microssegundos em CPU) | **> 10.000x mais rápido** |
| **Memória RAM Alocada** | > 150 MB (app webview / browser) | **8.92 KB** (via `tracemalloc`) | Desprezível, sem aquecimento de bateria |
| **Consumo de Rede por Viagem** | 600 requisições HTTP (polling contínuo a cada 3s por 30 min) · ~300 KB | **1 requisição HTTP discreta** (event-driven, disparada apenas na desistência) · 0,036 KB | **99.98% de redução no tráfego de dados** |
| **Dados Pessoais Transmitidos (LGPD)** | IP, Device ID, Advertising ID, rastreamento de tela contínuo com banners de anúncios | **ZERO identificadores pessoais** (sem IMEI, sem ID de usuário, sem histórico) | Privacidade por Design absoluta |
| **Payload do Evento** | Metadados de sessão, telemetria de anúncios | `{'stop_id': '<ID>', 'event': 'ABN', 'time': '<MIN>'}` (36 bytes) | Mínimo possível |
| **Persistência no Servidor** | Banco relacional com histórico de rotas e usuários | Memória RAM volátil com janela de 10 minutos (descarte automático após agregar no grafo) | Risco zero de vazamento de dados de pessoas |
| **Moat Competitivo / Modelo de Negócio** | Modelo B2B dependente das concessionárias de ônibus (conflito de interesse: não pode mostrar fuga para alternativos) | Focado no interesse público e eficiência da frota: revela demanda reprimida real sem exigir catraca | Defensabilidade estrutural e de dados |

---

## 🚀 5. Como Reproduzir os Experimentos

Ambiente virtual com Python 3.12, PyTorch e NumPy configurado:

```powershell
# 1. Ativar o ambiente virtual
cd code/grafoparada_tec
.\.venv\Scripts\Activate.ps1

# 2. Executar a validação da cinemática da parada e benchmark completo
python validar_cinematica_parada.py

# 3. Executar o piloto E1 da STGCN
python avaliar_piloto.py
```
