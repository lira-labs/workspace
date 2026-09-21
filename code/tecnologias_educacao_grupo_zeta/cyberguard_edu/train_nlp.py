import torch
import pandas as pd
from torch.utils.data import DataLoader
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from src.data.dataset import CyberGuardDataset
import os

def train_cyberguard():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Iniciando treinamento NLP no dispositivo: {device}")

    # Inicializa Tokenizer e Modelo BERT
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2).to(device)

    # Carrega dados reais do dataset clonado (ec-darkpattern)
    dataset_path = "data/raw/ec-darkpattern/dataset/dataset.tsv"
    print(f"Carregando dataset de: {dataset_path}")
    
    df = pd.read_csv(dataset_path, sep='\t')
    # Remove linhas vazias e garante tipo string/int
    df = df.dropna(subset=['text', 'label'])
    texts = df['text'].astype(str).tolist()
    labels = df['label'].astype(int).tolist()

    # Reduzindo para uma amostra para teste rápido, se necessário
    # texts = texts[:100]
    # labels = labels[:100]

    dataset = CyberGuardDataset(texts, labels, tokenizer)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=2e-5)

    epochs = 3
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for i, batch in enumerate(dataloader):
            optimizer.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            batch_labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=batch_labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            
            # Print de progresso a cada 100 batches
            if (i+1) % 100 == 0:
                print(f"Batch {i+1}/{len(dataloader)} - Loss: {loss.item():.4f}")

        print(f"Epoch {epoch+1}/{epochs} - Loss NLP Média: {epoch_loss/len(dataloader):.4f}")

    # Salva o modelo treinado
    os.makedirs("src/models/weights", exist_ok=True)
    model.save_pretrained("src/models/weights/cyberguard_bert")
    tokenizer.save_pretrained("src/models/weights/cyberguard_bert")
    print("Modelo BERT salvo com sucesso na pasta src/models/weights.")

if __name__ == "__main__":
    train_cyberguard()
