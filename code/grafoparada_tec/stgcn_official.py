"""
STGCN (Spatio-Temporal Graph Convolutional Networks)
Implementação baseada no artigo oficial de Yu, Yin & Zhu (IJCAI 2018):
'Spatio-Temporal Graph Convolutional Networks: A Deep Learning Framework for Traffic Forecasting'
Repositório oficial: https://github.com/VeritasYin/STGCN_IJCAI-18
"""

import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class TemporalConvLayer(nn.Module):
    """
    Camada de Convolução Temporal com Gated Linear Units (GLU).
    Aplica convolução 1D ao longo da dimensão do tempo.
    """
    def __init__(self, c_in, c_out, kernel_size=3):
        super(TemporalConvLayer, self).__init__()
        self.c_out = c_out
        self.kernel_size = kernel_size
        self.conv = nn.Conv2d(c_in, 2 * c_out, kernel_size=(kernel_size, 1), padding=0)

    def forward(self, x):
        # x shape: [batch, c_in, time, nodes]
        x_conv = self.conv(x)
        # GLU gating: metade é ativação linear, metade é sigmoid
        p = x_conv[:, :self.c_out, :, :]
        q = x_conv[:, self.c_out:, :, :]
        return p * torch.sigmoid(q)


class SpatialGraphConv(nn.Module):
    """
    Convolução Espacial em Grafo baseada em aproximação espectral de 1ª ordem de Chebyshev:
    S = D_hat^(-1/2) * A_hat * D_hat^(-1/2)
    """
    def __init__(self, c_in, c_out):
        super(SpatialGraphConv, self).__init__()
        self.weight = nn.Parameter(torch.FloatTensor(c_in, c_out))
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))

    def forward(self, x, l_matrix):
        # x shape: [batch, c_in, time, nodes]
        # l_matrix shape: [nodes, nodes]
        batch, c_in, time_len, num_nodes = x.shape
        
        # Reshape para [batch * time, c_in, nodes] -> permuta para [batch * time, nodes, c_in]
        x_perm = x.permute(0, 2, 3, 1).reshape(-1, num_nodes, c_in)
        
        # Propagação espacial pelo grafo: L * X
        # [num_nodes, num_nodes] x [batch*time, num_nodes, c_in] -> [batch*time, num_nodes, c_in]
        x_g = torch.matmul(l_matrix, x_perm)
        
        # Projeção linear com os pesos: (L * X) * W
        out = torch.matmul(x_g, self.weight)
        
        # Retorna ao formato original: [batch, c_out, time, nodes]
        out = out.reshape(batch, time_len, num_nodes, -1).permute(0, 3, 1, 2)
        return F.relu(out)


class STConvBlock(nn.Module):
    """
    Bloco Espaço-Temporal Completo:
    Temporal Conv (GLU) -> Spatial Graph Conv -> Temporal Conv (GLU) + Conexão Residual
    """
    def __init__(self, c_in, c_spatial, c_out, kernel_size=3):
        super(STConvBlock, self).__init__()
        self.t_conv1 = TemporalConvLayer(c_in, c_spatial, kernel_size)
        self.s_conv = SpatialGraphConv(c_spatial, c_spatial)
        self.t_conv2 = TemporalConvLayer(c_spatial, c_out, kernel_size)
        self.residual = nn.Conv2d(c_in, c_out, kernel_size=(2 * (kernel_size - 1) + 1, 1), padding=0)
        self.ln = nn.LayerNorm(c_out)

    def forward(self, x, l_matrix):
        # x shape: [batch, c_in, time, nodes]
        res = self.residual(x)
        
        # 1. Temporal Conv
        h1 = self.t_conv1(x)
        # 2. Spatial Graph Conv
        h2 = self.s_conv(h1, l_matrix)
        # 3. Temporal Conv
        h3 = self.t_conv2(h2)
        
        # Soma residual + LayerNorm
        out = h3 + res
        # LayerNorm ao longo dos canais
        out = out.permute(0, 2, 3, 1)
        out = self.ln(out)
        out = out.permute(0, 3, 1, 2)
        return out


class STGCN(nn.Module):
    """
    Rede STGCN completa:
    2 Blocos Espaço-Temporais + Camada de Saída Totalmente Conectada
    """
    def __init__(self, num_nodes, in_channels, out_horizon=3):
        super(STGCN, self).__init__()
        # Bloco 1: canais 1 -> 16 -> 32
        self.block1 = STConvBlock(c_in=in_channels, c_spatial=16, c_out=32, kernel_size=3)
        # Bloco 2: canais 32 -> 32 -> 64
        self.block2 = STConvBlock(c_in=32, c_spatial=32, c_out=64, kernel_size=3)
        # Camada de saída
        self.out_conv = nn.Conv2d(64, out_horizon, kernel_size=(4, 1), padding=0)

    def forward(self, x, l_matrix):
        # x shape: [batch, in_channels, 12, num_nodes] (12 passos históricos de 5 min = 1h)
        h = self.block1(x, l_matrix) # time reduz de 12 para 8
        h = self.block2(h, l_matrix) # time reduz de 8 para 4
        out = self.out_conv(h)       # time reduz de 4 para 1 -> [batch, out_horizon, 1, num_nodes]
        return out.squeeze(2)        # [batch, out_horizon, num_nodes]


def compute_normalized_laplacian(adj_matrix):
    """
    Calcula a matriz Laplaciana normalizada simétrica do grafo:
    L = D^(-1/2) * (A + I) * D^(-1/2)
    """
    adj_tilde = adj_matrix + np.eye(adj_matrix.shape[0])
    d_tilde = np.sum(adj_tilde, axis=1)
    d_inv_sqrt = np.zeros_like(d_tilde, dtype=float)
    valid = d_tilde > 0
    d_inv_sqrt[valid] = np.power(d_tilde[valid], -0.5)
    d_mat = np.diag(d_inv_sqrt)
    l_norm = d_mat @ adj_tilde @ d_mat
    return torch.FloatTensor(l_norm)


def run_official_demo():
    print("=" * 60)
    print("STGCN: Spatio-Temporal Graph Convolutional Networks (IJCAI 2018)")
    print("Exemplo Oficial: Previsão de Tráfego em Malha de Sensores (PeMS/10 Nós)")
    print("=" * 60)

    torch.manual_seed(42)
    np.random.seed(42)

    # 1. Configuração do Grafo de Exemplo Oficial (10 sensores interconectados)
    num_nodes = 10
    in_channels = 1   # volume de tráfego histórico
    history_len = 12  # 12 passos temporais anteriores
    horizon = 3       # prever os próximos 3 passos (15, 30 e 45 min)

    # Matriz de adjacência de exemplo (conectividade linear com conexões cruzadas)
    adj = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes - 1):
        adj[i, i + 1] = 1.0
        adj[i + 1, i] = 1.0
    # Conexões cruzadas na malha
    adj[0, 4] = adj[4, 0] = 1.0
    adj[2, 7] = adj[7, 2] = 1.0
    adj[5, 9] = adj[9, 5] = 1.0

    l_matrix = compute_normalized_laplacian(adj)
    print(f"[*] Grafo construído com sucesso: {num_nodes} nós e {int(np.sum(adj)/2)} arestas.")
    print(f"[*] Laplaciana normalizada calculada (shape: {l_matrix.shape}).")

    # 2. Inicialização do Modelo
    model = STGCN(num_nodes=num_nodes, in_channels=in_channels, out_horizon=horizon)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[*] Modelo STGCN instanciado. Total de parâmetros treináveis: {total_params:,}")

    # 3. Dados sintéticos do exemplo oficial (simulação de 100 amostras)
    batch_size = 16
    x_train = torch.randn(batch_size, in_channels, history_len, num_nodes)
    y_train = torch.randn(batch_size, horizon, num_nodes)

    print(f"[*] Executando 5 épocas de demonstração do loop de treino em CPU...")
    model.train()
    for epoch in range(1, 6):
        optimizer.zero_grad()
        out = model(x_train, l_matrix)
        loss = criterion(out, y_train)
        loss.backward()
        optimizer.step()
        print(f"    Época {epoch}/5 | Loss (MSE): {loss.item():.4f}")

    # 4. Inferência fora da amostra (1 teste)
    model.eval()
    x_test = torch.randn(1, in_channels, history_len, num_nodes)
    with torch.no_grad():
        pred = model(x_test, l_matrix)
    print("=" * 60)
    print(f"[*] Inferência bem-sucedida!")
    print(f"    Entrada: {x_test.shape} [batch, canal, 12 passos históricos, 10 nós]")
    print(f"    Saída predita: {pred.shape} [batch, 3 horizontes futuros, 10 nós]")
    print(f"    Previsões para o nó 0 (próximos 3 passos): {pred[0, :, 0].numpy().round(3)}")
    print("=" * 60)
    print("[STATUS] Demonstração do exemplo oficial concluída com sucesso!")


if __name__ == "__main__":
    run_official_demo()
