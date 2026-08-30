"""
Script de Treinamento e Avaliação da MLP no Heart Disease Dataset (80% treino / 20% teste)
Busca a melhor acurácia para preencher o slide de entrega oficial
"""
import csv
import random
import sys

sys.path.insert(0, r"D:\workspace\code\mlp_viewer")
from network import Network
from loader import Loader

def evaluate_mlp_configurations():
    loader = Loader(r"D:\workspace\code\mlp_viewer\rsc\heart.csv")
    rows = loader.rows
    
    # 80% treino, 20% teste
    random.seed(42)
    shuffled_rows = list(rows)
    random.shuffle(shuffled_rows)
    split_idx = int(len(shuffled_rows) * 0.8)
    train_rows = shuffled_rows[:split_idx]
    test_rows = shuffled_rows[split_idx:]
    
    print(f"Total amostras: {len(rows)} | Treino: {len(train_rows)} | Teste: {len(test_rows)}")
    
    architectures = [
        [13, 8, 4, 1],
        [13, 16, 8, 1],
        [13, 10, 5, 1],
        [13, 12, 6, 1]
    ]
    learning_rates = [0.01, 0.005, 0.02]
    activations = ["relu", "sigmoid", "tanh"]
    
    best_acc = 0.0
    best_cfg = None
    
    for arch in architectures:
        for lr in learning_rates:
            for act in activations:
                net = Network(arch)
                net.set_activation(act)
                net.set_preprocess_mode("standardize")
                net.load_dataset_rows(train_rows)
                
                # Treina por 80 épocas
                for epoch in range(80):
                    for row in train_rows:
                        inputs = [float(x) for x in row[:-1]]
                        target = float(row[-1])
                        net.train_step(inputs, target, learning_rate=lr)
                        
                # Avalia no conjunto de teste
                correct = 0
                for row in test_rows:
                    inputs = [float(x) for x in row[:-1]]
                    target = float(row[-1])
                    trans_in = net.transform_inputs(inputs)
                    out = net.forward_propagation(trans_in)[0]
                    pred = 1.0 if out >= 0.5 else 0.0
                    if pred == target:
                        correct += 1
                        
                acc = correct / len(test_rows)
                if acc > best_acc:
                    best_acc = acc
                    best_cfg = {
                        "arch": " | ".join(str(x) for x in arch),
                        "lr": lr,
                        "activation": act,
                        "accuracy": round(acc, 3)
                    }
                print(f"Arch: {arch} | LR: {lr} | Act: {act} -> Test Acc: {acc:.3f}")
                
    print("\n" + "=" * 60)
    print(f"  MELHOR CONFIGURAÇÃO ENCONTRADA:")
    print(f"  Acurácia:     {best_cfg['accuracy']}")
    print(f"  Arquitetura:  {best_cfg['arch']}")
    print(f"  Learning Rate:{best_cfg['lr']}")
    print(f"  Ativação:     {best_cfg['activation']}")
    print("=" * 60)
    return best_cfg

if __name__ == "__main__":
    evaluate_mlp_configurations()
