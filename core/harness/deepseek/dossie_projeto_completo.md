# 📋 DOSSIÊ TÉCNICO OFICIAL · GRAFOPARADA (UFRPE 2026)


## 1. FUNDAMENTAÇÃO TEÓRICA & ESTADO DA ARTE A1

# 📚 Fundamentação Teórica Qualis A1 & Estado da Arte · GrafoParada
> **Disciplina:** Tópicos Avançados em Inteligência Artificial (AI4Good) · UFRPE  
> **Autor:** Cauã da Cunha Lira (`caua.lira@ufrpe.br`)  
> **Orientador / Professor:** Prof. Lucas Silva Figueiredo  
> **Tema:** Modelagem de Abandono de Passageiros (*Passenger Reneging*), Demanda Latente Censurada e Despacho de Frota no Vazio (*Deadheading Mitigation*)

---

## 1. Contexto & O Ponto Cego da Literatura Atual

No transporte público metropolitano, as concessionárias e órgãos gestores (como o Grande Recife Consórcio de Transporte - CTM) mensuram sua demanda quase que exclusivamente pelos **validadores de bilhetagem eletrônica (VEM / Smart Card Data)**.

Contudo, essa métrica sofre de **censura à direita**: ela registra apenas a *demanda atendida*. O passageiro que chega à parada, espera 30 ou 40 minutos sob chuva ou escuridão e desiste (recorrendo ao transporte clandestino, moto-táxi, app de carona ou voltando para casa) **nunca passa pela catraca e se torna estatisticamente invisível**.

A literatura internacional recente categoriza rigorosamente esse ecossistema comportamental em cinco fenômenos bem delimitados:

| Fenômeno | Definição Formal na Literatura | Artigo de Referência Chave | Como o GrafoParada Trata |
| :--- | :--- | :--- | :--- |
| **Balking** | Decisão de *nem iniciar a espera* ao prever atraso ou irregularidade extrema. | *Wardman et al. (2014) · TR Part B* | O app calcula a **Janela Segura de Saída** (ex: *saia às 06h08*), evitando que o usuário saia antes e desista. |
| **Reneging** | *Abandono da espera* na parada após aguardar determinado tempo sem que o veículo chegue. | **Kim, Yun & Kim (2026)** · *J. Public Transportation* | O motor local infere o tempo de permanência na parada e a Central CTM detecta o pico de *demanda não-atendida*. |
| **Denied Boarding** | Veículo chega à parada, mas o passageiro é *impedido de embarcar* por superlotação ou queima. | **Tan & Ramli (2024)** · *Transportation (A1)*<br>**Yap & Cats (2021)** · *TR Part A (A1)* | Sensor Forense de Queima de Parada detecta o ônibus passando sem parar e aciona resgate de transbordo. |
| **Active Boarding Delay** | Passageiro *escolhe esperar* o próximo ônibus para conseguir assento livre. | **Drabicki et al. (2023)** · *RTBM (A1)*<br>**Chen et al. (2023)** · *TR Part A (A1)* | A telemetria informa se o próximo ônibus tem assentos garantidos (verde) ou lotação média (laranja). |
| **Bus Bunching** | Emparelhamento de ônibus em comboio, gerando buracos excessivos de intervalo (*headway*). | **Drabicki, Kucharski & Cats (2023)** · *Transportation (A1)* | A Central CTM redistribui frotas ociosas (deadheading) para cobrir o buraco antes do comboio se formar. |

---

## 2. Destaques dos Artigos A1 e sua Aplicação Metodológica

### A. O Artigo Mais Próximo da Literatura (Kim et al., 2026)
- **Título:** *City-scale unmet bus demand modeling with passenger reneging behavior* (Journal of Public Transportat
...


## 2. RESPOSTAS À BANCA NO ROTEIRO DE APRESENTAÇÃO

qa-box {
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 16px;
      margin-top: 30px;
    }
    .qa-box h3 {
      font-size: 1.05rem;
      font-weight: 800;
      color: #92400e;
      margin-bottom: 12px;
    }
    .qa-item {
      margin-bottom: 14px;
    }
    .qa-q {
      font-weight: 700;
      color: #78350f;
      margin-bottom: 4px;
      font-size: 0.92rem;
    }
    .qa-a {
      font-size: 0.92rem;
      color: var(--text);
    }
    .quick-links {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }
    .quick-link-btn {
      display: inline-block;
      text-decoration: none;
      background: #f1f5f9;
      color: #0f172a;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 0.82rem;
      font-weight: 700;
      border: 1px solid #cbd5e1;
    }
  </style>
</head>
<body>

  <header>
    <div class="badge">UFRPE · AI4Good · Seminário 2</div>
    <h1>GrafoParada: Roteiro da Fala na Aula</h1>
    <div class="meta">Cauã da Cunha Lira · Quarta, 11/11 · Duração cronometrada: 4 minutos</div>
  </header>

  <div class="quick-links">
    <a href="https://grafoparadaweb.vercel.app" target="_blank" class="quick-link-btn">📱 Abrir App ao Vivo</a>
    <a href="https://grafoparadaweb.vercel.app/slides_sem2.html" target="_blank" class="quick-link-btn">📊 Slides Web</a>
    <a href="https://grafoparadaweb.vercel.app/GrafoParada_Seminario2_CauaLira.pptx" target="_blank" class="quick-link-btn">📥 Baixar PPTX Limpo</a>
  </div>

  <div class="box-regras">
    <h3>Como conduzir em sala (Critérios do Prof. Lucas):</h3>
    <ul style="padding-left: 20px; font-size: 0.9rem;">
      <li><strong>Fale de cabeça, não leia:</strong> O slide é minimalista e só serve de apoio visual para sua fala.</li>
      <li><strong>Demo ao vivo:</strong> Celular espelhado rodando dados reais do GTFS (400 linhas) e Cittamobi ao vivo.</li>
      <li><strong>Seja direto na falha:</strong> O professor pontua quem demonstra onde a IA erra de verdade.</li>
      <li><strong>Tempo total:</strong> 4 minutos cravados (duas passadas cronometradas com sucesso).</li>
    </ul>
  </div>

  <!-- AS 4 FRASES SEM IA -->
  <div class="frases-aluno">
    <h2>🎯 As 4 Frases (Decore para falar de cabeça em 1 min):</h2>
    <div class="frase-item">
      <strong>1. A Demo:</strong> O estudante ou passageiro no Grande Recife abre o app, consulta qualquer uma das 400 linhas reais do GTFS (como a Linha 522 da UFRPE ou a Linha 060), vê a previsão em 4 minutos e sai de casa no horário exato sem mofar no ponto de ônibus.
    </div>
    <div class="frase-item">
      <strong>2. O Custo:</strong> No celular levou 4,98 milissegundos e 12 KB de RAM; no servidor a STGCN levou 0,77 milissegundo e 358 MB no processo PyTorch na CPU. A estimativa inicial de arquitetura previa menos de 500 ms e 300 MB, e a diferença é que a CPU calculou muito mais rápido e o runtime segura bibliotecas no SO.
    </div>
    <div class="frase-item">
      <strong>3. A Falha:</strong> Num choque súbito com 45 minutos de retenção simulada na via, a STGCN previu 18 minutos porque suavizou o atraso pelo grafo. Quem sofre é o passageiro que perde a prova ou o turno, e o erro ensina que choques pontuais exigem uma trava híbrida que corte a IA.
    </div>
    <div class="frase-item">
      <strong>4. O Que Mudou:</strong> No sem1 uma conta simples bateu a rede em 5 paradas e eu ia descartar a STGCN; mantive a STGCN para testar em escala: na malha expandida de 20 paradas, em dados simulados por difusão espaço-temporal, a STGCN obteve 1,51 minuto de erro contra 1,93 minuto da regressão linear e 7,13 da persistência, mostrando que o grafo mitiga a explosão dimensional quando a rede cresce.
    </div>
  </div>

  <!-- SLIDE 1 -->
  <div class="slide-card">
    <div class="slide-header">
      <div class="slide-title">Slide 1 · Ponta a Ponta (Demo ao Vivo)</div>
      <div class="slide-time">⏱️ 80 segundos</div>

...


## 3. ARQUITETURA ST-GCN (RESUMO)

```python
"""
STGCN aplicado ao GrafoParada · Frota no Vazio
Alteração Mínima: Troca o grafo genérico por um corredor de 5 paradas de ônibus reais
e os dados de tráfego por tempos de espera (minutos) nas paradas ao longo do tempo.
"""

import numpy as np
import torch
import networkx as nx
from stgcn_official import STGCN, compute_normalized_laplacian


def run_grafoparada_demo():
    print("=" * 65)
    print("GrafoParada · Frota no Vazio (STGCN para Espera em Paradas)")
    print("Alteração Mínima: Corredor de Linha Distrital com 5 Paradas")
    print("=" * 65)

    torch.manual_seed(42)
    np.random.seed(42)

    # 1. Definição do Corredor de 5 Paradas Reais
    paradas = [
        "P1 - Camela Centro",
        "P2 - PE-60 Entroncamento",
        "P3 - Ipojuca Sede (Terminal)",
        "P4 - Suape Acesso Industrial",
        "P5 - Gaibu Retorno"
    ]
    num_nodes = len(paradas)
    in_channels = 1   # Minutos de espera observados na parada
    history_len = 12  # Últimos 12 passos (janelas de 10 min = 2 horas)
    horizon = 3       # Previsão para os próximos 3 passos (t+10, t+20, t+30 min)

    # 2. Grafo do Corredor (Linha Sequencial com Conexão de Retorno)
    G = nx.DiGraph()
    for i, nome in enumerate(paradas):
        G.add_node(i, name=nome)
    for i in range(num_nodes - 1):
        G.add_edge(i, i + 1, weight=1.0)
        G.add_edge(i + 1, i, weight=0.5) # tráfego no sentido oposto

    adj = nx.to_numpy_array(G)
    l_matrix = compute_normalized_laplacian(adj)

    print(f"[*] Corredor modelado como grafo viário ({num_nodes} paradas consecutivas):")
    for i, p in enumerate(paradas):
        vizinhos = [paradas[j] for j in range(num_nodes) if adj[i, j] > 0]
        print(f"    - [{p}] -> conecta com: {len(vizinhos)} parada(s) vizinha(s)")

    # 3. Modelo STGCN ajustado para 5 nós
    model = STGCN(num_nodes=num_nodes, in_channels=in_channels, out_horizon=horizon)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
    criterion = torch.nn.MSELoss()

    # 4. Dados do Problema: Simulação de atraso severo se acumulando em P1 e propagando para P2
    # Espera normal = 10 a 15 min; Espera em gargalo (comboio / falha de frota) = 45 a 60 min
    batch_size = 16
    x_dados = torch.full((batch_size, in_channels, history_len, num_nodes), 15.0)
    # Injetando o gargalo de atraso acumulado em P1 e P2 nas últimas janelas temporais
    x_dados[:, :, 8:, 0] += torch.tensor([25.0, 35.0, 45.0, 50.0]) # P1 acumulando espera
    x_dados[:, :, 9:, 1] += 
```
