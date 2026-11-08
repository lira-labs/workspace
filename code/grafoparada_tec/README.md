# GrafoParada v4.0 · Protótipo Interativo, Motor On-Device e Validação Experimental

Este diretório contém a implementação completa, os dados reais de transporte e sensores físicos, o motor de evolução e reavaliação contínua (`v1.0 → v2.0 → v3.0 → v4.0`) e o **Protótipo Interativo Web/Mobile** do projeto **GrafoParada · Frota no Vazio** (VA2 · Tópicos Avançados em Inteligência Artificial - AI4Good, UFRPE).

---

## 🗂️ Estrutura de Arquivos

```text
code/grafoparada_tec/
├── data/
│   ├── corredor_real_linha178_191.csv      # 20 paradas reais da PE-60 (Cabo/Suape) extraídas do GTFS oficial CTM
│   ├── sensors_tmd.csv                     # 5.893 leituras físicas de sensores reais (Still, Bus, Walking, Car)
│   ├── benchmark_evolucao_v4.json          # Artefato JSON gerado pelo motor de avaliação v1.0 -> v4.0
│   ├── auditoria_cittamobi_real_pe60.json  # Cruzamento real da API m3p do Cittamobi vs. 20 paradas GTFS da PE-60
│   ├── gtfs.zip                            # GTFS bruto oficial do CTM (ignorado no git)
│   └── gtfs_granderecife/                  # GTFS descompactado do Grande Recife (ignorado no git)
├── prototipo_grafoparada.html              # Protótipo Interativo Completo (Smartphone Modo Bolso + Painel CTM + Auditoria Cittamobi)
├── auditoria_cittamobi_real.py             # Auditoria empírica ao vivo da API m3p do Cittamobi (agência a=202 Grande Recife)
├── motor_evolucao_prototipo.py             # Motor de evolução e benchmark iterativo (v1.0 -> v2.0 -> v3.0 -> v4.0)
├── validar_cinematica_parada.py            # Ponto de entrada de validação cinemática, rotina, LGPD e grafo PE-60
├── avaliar_piloto.py                       # Piloto experimental E1 (5 paradas) e E2 (Protocolo de Decisão Passo 8)
├── stgcn_grafoparada.py                    # Demonstração base da STGCN (Tecnologia Base Demonstrável)
├── stgcn_official.py                       # Camadas temporais e espaciais canônicas da STGCN em PyTorch
├── explorar_gtfs.py                        # Script de inspeção da malha e linhas metropolitanas CTM
├── extrair_corredor_real.py                # Pipeline de extração das coordenadas do corredor PE-60
└── README.md                               # Este documento
```

---

## 📈 1. Evolução e Reavaliação Contínua do Protótipo (`v1.0 → v4.0`)

Para responder com rigor científico aos questionamentos do **Prof. Lucas Figueiredo** no Seminário 1, executamos 4 ciclos sucessivos de engenharia e reavaliação sobre **1.200 trajetórias reais** no corredor da PE-60:

| Iteração do Protótipo | Mudança de Engenharia Aplicada | Acurácia Sensores | Acurácia Global | Falso Positivo Desembarque | Recall Desembarque | F1-Score Desistência |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **v1.0 Baseline** | MLP raso (12 features brutas) + FSM olhando apenas 1 quadro isolado | 75,29% | 67,75% | **0,00%** | 56,33% | 71,93% |
| **v2.0 Feature Eng** | 26 atributos físicos (Crest factor, log-energia, razão giro/acel) + `ResSensorNetV2` (`BatchNorm` + `GELU` + `CosineAnnealingLR`) | 86,96% | 84,67% | **0,00%** | 84,00% | 79,07% |
| **v3.0 Fusão Multimodal** | `Soft-Voting` probabilístico multi-janela + Velocidade escalar geodésica ($v = \Delta d / \Delta t$) + Sincronia GTFS | **97,42%** | **99,67%** | **0,00%** | **99,33%** | **99,67%** |

### Matriz de Confusão Final (`v3.0` · 1.200 Trajetórias na PE-60)

| Classe Real \ Predição | ALIGHTING (Desembarque) | BOARDING_SERVED (Embarque) | ABANDONMENT (Desistência) | TRANSIT_BYPASS (Passagem) | Total |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ALIGHTING** | **298** | 2 | **0 (0,00%)** | 0 | 300 |
| **BOARDING_SERVED** | 0 | **298** | 2 | 0 | 300 |
| **ABANDONMENT** | 0 | 0 | **300 (100%)** | 0 | 300 |
| **TRANSIT_BYPASS** | 0 | 0 | 0 | **300 (100%)** | 300 |

---

## 🎧 2. Motor On-Device de Aprendizado de Rotina (`OnDeviceRoutineLearner`)

Focado na recomendação do Prof. Lucas (*"focar e fazer muito bem esse lance de vermos a rotina, ter cuidado com LGPD e custo operacional"*):

- **Problema identificado na 1ª tentativa (Hard-Binning)**: Dividir o dia em janelas fixas (`minuto // 45`) causava divisão artificial de visitas na volta do trabalho às `17:15` (`1035 min`, fronteira exata entre os baldes 22 e 23), limitando o recall a `88,89%`.
- **Solução implementada (`v4.0`)**: **Clusterização Deslizante de Centróide Temporal ($\pm 35\text{ min}$)** combinada com média móvel exponencial (`EWMA`).
- **Resultados medidos em 30 dias simulados na PE-60**:
  - **Convergência do Cold-Start**: Aprende a rotina do trabalhador autonomamente no **4º dia útil** (confiança $\ge 75\%$).
  - **Recall de Disparo Proativo de Voz no Bolso (pós-convergência)**: **100,00%** (avisa no fone sem precisar puxar o celular na rua).
  - **Taxa de Falso Disparo em Finais de Semana / Passeios Casuais**: **0,00%**.
  - **Pegada de Armazenamento Local**: **166 bytes** salvos apenas no aparelho (`0 bytes` enviados à nuvem).

---

## 🧠 3. Escalabilidade Espaço-Temporal: 5 Paradas vs. 20 Paradas Reais da PE-60

Testamos empiricamente a tese defendida no Seminário 1 sobre por que manter a STGCN na arquitetura:

| Escala da Malha | Persistência (Hoje) | Regressão Tabular Achatada (s/ Grafo) | STGCN (Grafo Laplaciano + Desistência) | Vencedor e Explicação Científica |
| :--- | :---: | :---: | :---: | :--- |
| **Corredor Curto (5 Paradas · Piloto E1)** | MAE = 14,91 min | **MAE = 2,46 min** (9 pesos) | MAE = 4,42 min (34.627 pesos) | **Regressão Tabular** vence pelo princípio da parcimônia em linha curta |
| **Corredor Real Completo PE-60 (20 Paradas · Linha 178/191)** | MAE = 7,13 min | MAE = 1,93 min (121 colunas acopladas) | **MAE = 1,51 min** (pesos compartilhados em $L^2, L^3$) | **STGCN vence (-21,8% de erro)** quando ondas de atraso nascem em pontos variados das 20 paradas |

---

## 🖥️ 4. Como Usar o Protótipo Interativo e Rodar os Testes

### Abrir o Protótipo Visual Interativo
Abra o arquivo [`prototipo_grafoparada.html`](file:///c:/Users/ccunh/Documents/workspace/code/grafoparada_tec/prototipo_grafoparada.html) em qualquer navegador moderno para interagir com:
1. **Aba 1 (App On-Device & Modo Bolso)**: Simulador de celular com áudio sintetizado em português (`Web Speech API`), probabilidades `Soft-Voting` em tempo real e inspetor de pacotes de rede de 36 bytes.
2. **Aba 2 (Painel Operacional CTM · 20 Paradas da PE-60)**: Mapa interativo das 20 paradas reais (TI Cabo → Porto de Suape), alternância *Catraca Cega vs. GrafoParada*, auditoria humana com selo `[?]` e gerador de remanejamento GTFS.
3. **Aba 3 (Evolução Científica v1.0 → v4.0)**: Tabelas comparativas de todos os ciclos de reavaliação.
4. **Aba 4 (Calculadora de Escala LGPD & Custo vs. Cittamobi)**: Simulador deslizante de 5.000 a 500.000 passageiros/dia.

### Executar os Benchmarks via Terminal

```powershell
# Executar o motor completo de evolução e reavaliação (v1.0 -> v4.0)
.\code\grafoparada_tec\.venv\Scripts\python.exe code\grafoparada_tec\validar_cinematica_parada.py

# Executar a auditoria empírica ao vivo da API m3p do Cittamobi (Grande Recife a=202)
.\code\grafoparada_tec\.venv\Scripts\python.exe code\grafoparada_tec\auditoria_cittamobi_real.py

# Executar o piloto experimental E1/E2 original
.\code\grafoparada_tec\.venv\Scripts\python.exe code\grafoparada_tec\avaliar_piloto.py
```

---

## 🔍 5. Engenharia Reversa e Auditoria Empírica do Servidor Real Cittamobi (`m3p API`)

Utilizando os repositórios públicos de engenharia reversa da plataforma Cittamobi no GitHub (`ericklucena/cittamobi-wp` para o Grande Recife `a=202`, `ITWhiteRaccoon/BusTracker`, `marciofao/cittamobi` e o projeto de Machine Learning sobre o Google BigQuery da Cittamobi `Leonardo0liveira/ML-Cittamobi`), executamos o script [`auditoria_cittamobi_real.py`](file:///c:/Users/ccunh/Documents/workspace/code/grafoparada_tec/auditoria_cittamobi_real.py) contra `https://api.cittamobi.com.br/m3p/js/`:

1. **O "Apagão" de Rastreamento na PE-60 / Suape (`activeVehicles: 0`)**:
   - Localizamos os IDs internos reais das linhas do corredor na agência `a=202` (Grande Recife): **Linha 0178 / 178** (`serviceId: 9655998`, `9655999`, `9656486`, `13185570`, `13185571`), **Linha 0198 / 198** (`9656040`, `9656041`, `13185572`, `13185573`), **Linha 0197** (`9656042`, `9656043`) e **Linha 119 Garapu** (`6663`, `6666`), operadas por **Expresso Vera Cruz** (`companyId=655935`) e **São Judas Tadeu** (`companyId=112`).
   - Em todas as 20 paradas mapeadas na PE-60 (ex.: `#2966405` TI Cabo, `#2966771` PE-060 km 09, `#2966773` Trevo Ipojuca), a API `m3p` retorna `activeVehicles: 0` e `services: []` (`52 bytes`), confirmando na prática por que o trabalhador fica às cegas na pista.
2. **Peso Real de Rede e Polling de 15s (`Vehicles.xaml.cs`)**:
   - Um único carregamento do mapa em Cabo/PE-60 (`stops/viewport`) transfere **142.363 bytes (`139,0 KB`, 534 paradas)**, e no centro do Recife transfere **274.520 bytes (`268,1 KB`, 1.000 paradas)**, seguido de um `DispatcherTimer` de **15 segundos** (`100 requisições` em 25 min). O GrafoParada reduz o tráfego em **99,99%** (`0 bytes` na rotina normal e `36 bytes` em desistência).
3. **Por que o ML de Cliques da Cittamobi falha (`F1 = 40,85%` vs. `99,67%`)**:
   - O estudo `Leonardo0liveira/ML-Cittamobi` mostra que prever embarque/conversão apenas por eventos de clique na tela do app (`stop_event_rate` no BigQuery) atinge no máximo **`F1 = 40,85%` (Random Forest) a `48,01%` (CatBoost)** (`AUC = 0,618`), pois 70% das consultas não correspondem a viagens reais. Ao fundir sensores físicos on-device (`ResSensorNetV2`) com velocidade geodésica ($v = \Delta d/\Delta t$), o GrafoParada atinge **`F1 = 99,67%`** com **`0,00%` de falso positivo no desembarque**.
