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
│   ├── gtfs.zip                            # GTFS bruto oficial do CTM (ignorado no git)
│   └── gtfs_granderecife/                  # GTFS descompactado do Grande Recife (ignorado no git)
├── prototipo_grafoparada.html              # Protótipo Interativo Completo (Smartphone Modo Bolso + Painel CTM 20 Paradas)
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

# Executar o piloto experimental E1/E2 original
.\code\grafoparada_tec\.venv\Scripts\python.exe code\grafoparada_tec\avaliar_piloto.py
```
