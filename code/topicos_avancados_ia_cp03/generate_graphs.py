import json
import os
import matplotlib.pyplot as plt

def load_data(scenario):
    rounds = []
    viability = []
    equity = []
    
    path = f'outputs/{scenario}'
    for i in range(1, 21):
        filename = f'rodada_{i:02d}.json'
        filepath = os.path.join(path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                rounds.append(i)
                viability.append(data.get('metricas', {}).get('viabilidade', 0))
                equity.append(data.get('metricas', {}).get('equidade_social', 0))
    return rounds, viability, equity

def plot_scenario(scenario, title):
    rounds, viab, eq = load_data(scenario)
    
    plt.figure(figsize=(12, 6))
    plt.plot(rounds, viab, marker='o', label='Viabilidade', color='blue', linewidth=2)
    plt.plot(rounds, eq, marker='s', label='Equidade Social', color='green', linewidth=2)
    
    plt.title(title, fontsize=16)
    plt.xlabel('Rodada', fontsize=14)
    plt.ylabel('Métrica (%)', fontsize=14)
    plt.xticks(range(1, 21))
    plt.ylim(0, 100)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{scenario}_metrics.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    if not os.path.exists('outputs/utopia') or not os.path.exists('outputs/distopia'):
        print("Diretórios de output não encontrados.")
    else:
        plot_scenario('utopia', 'Utopia: Viabilidade vs Equidade (Rodadas 1-20)')
        plot_scenario('distopia', 'Distopia: Viabilidade vs Equidade (Rodadas 1-20)')
        print("Gráficos gerados com sucesso!")
