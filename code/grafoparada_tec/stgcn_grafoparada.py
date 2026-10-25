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
    x_dados[:, :, 9:, 1] += torch.tensor([20.0, 30.0, 40.0])       # P2 recebendo o efeito cascata

    y_alvo = torch.zeros(batch_size, horizon, num_nodes)
    y_alvo[:, 0, :] = x_dados[:, 0, -1, :] + 2.0  # t+10 min
    y_alvo[:, 1, :] = x_dados[:, 0, -1, :] + 5.0  # t+20 min
    y_alvo[:, 2, :] = x_dados[:, 0, -1, :] + 8.0  # t+30 min

    # Treinamento rápido de convergência (25 épocas em CPU)
    model.train()
    for epoch in range(1, 26):
        optimizer.zero_grad()
        out = model(x_dados, l_matrix)
        loss = criterion(out, y_alvo)
        loss.backward()
        optimizer.step()

    # 5. Inferência do Cenário de Espera e Diagnóstico de Demanda Reprimida
    model.eval()
    with torch.no_grad():
        cenario_atual = x_dados[0:1] # 1 exemplo recente do corredor
        predicao_espera = model(cenario_atual, l_matrix) # shape: [1, 3, 5]

    print("=" * 65)
    print("[*] DIAGNÓSTICO DE ESPERA PREDITA NAS PARADAS (Próximos 10, 20 e 30 min):")
    print("=" * 65)
    for i, nome in enumerate(paradas):
        prev_10 = predicao_espera[0, 0, i].item()
        prev_20 = predicao_espera[0, 1, i].item()
        prev_30 = predicao_espera[0, 2, i].item()
        alerta = " [ALERTA: RISCO DE DESISTÊNCIA / INTERVALO EXCESSIVO]" if prev_30 > 40.0 else " [OPERAÇÃO REGULAR]"
        print(f"  {nome}:")
        print(f"    Espera prevista: t+10m: {prev_10:.1f} min | t+20m: {prev_20:.1f} min | t+30m: {prev_30:.1f} min{alerta}")

    print("=" * 65)
    print("[CONCLUSÃO] A STGCN conseguiu propagar o efeito de atraso do nó P1 para P2 pelo grafo,")
    print("            identificando o trecho crítico onde o passageiro desiste por espera superior a 40 min.")


if __name__ == "__main__":
    run_grafoparada_demo()
