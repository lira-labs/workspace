import json
import os
import re
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
                
                # Default to 0
                v = 0
                e = 0
                
                # Check if it's explicitly in "metricas" dictionary
                if 'metricas' in data:
                    v = data['metricas'].get('viabilidade', 0)
                    e = data['metricas'].get('equidade_social', 0)
                else:
                    # Fallback to regex parsing the auditor response
                    auditor_text = data.get('auditor', {}).get('response', '')
                    # Regex to find Viabilidade and Equidade
                    match_v = re.search(r'Viabilidade[^\d]*(\d{1,3})', auditor_text, re.IGNORECASE)
                    match_e = re.search(r'Equidade[^\d]*(\d{1,3})', auditor_text, re.IGNORECASE)
                    
                    if match_v:
                        v = int(match_v.group(1))
                    if match_e:
                        e = int(match_e.group(1))
                
                viability.append(v)
                equity.append(e)
    return rounds, viability, equity

def plot_scenario(scenario, title):
    rounds, viab, eq = load_data(scenario)
    
    plt.figure(figsize=(10, 5))
    plt.plot(rounds, viab, marker='o', label='Viabilidade Econômica', color='#1f77b4', linewidth=2.5, markersize=8)
    plt.plot(rounds, eq, marker='s', label='Equidade Social', color='#2ca02c', linewidth=2.5, markersize=8)
    
    # Shade area under curves
    plt.fill_between(rounds, viab, alpha=0.1, color='#1f77b4')
    plt.fill_between(rounds, eq, alpha=0.1, color='#2ca02c')
    
    plt.title(title, fontsize=16, fontweight='bold', pad=15)
    plt.xlabel('Rodada Histórica', fontsize=12)
    plt.ylabel('Métrica (%)', fontsize=12)
    plt.xticks(range(1, 21))
    plt.yticks(range(0, 101, 10))
    plt.ylim(0, 105)
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='lower right', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'{scenario}_metrics.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    if not os.path.exists('outputs/utopia') or not os.path.exists('outputs/distopia'):
        print("Diretórios de output não encontrados.")
    else:
        plot_scenario('utopia', 'Utopia: Viabilidade vs Equidade Social (1808-2026)')
        plot_scenario('distopia', 'Distopia: Viabilidade vs Equidade Social (1808-2026)')
        print("Gráficos gerados com sucesso!")
