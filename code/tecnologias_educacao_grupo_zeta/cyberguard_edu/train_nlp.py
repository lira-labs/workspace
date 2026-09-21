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

    # Carrega dados do dataset clonado (ec-darkpattern)
    # Para o MVP, usaremos dados fictícios se o dataset não estiver formatado perfeitamente
    # No mundo real, aqui fazemos o parse do CSV deles.
    texts = ["Buy now or lose everything!", "Normal product description here.", "Hidden message 123", "Sale ends in 5 mins!"]
    labels = [1, 0, 1, 1]  # 1 = Suspeito/Dark Pattern, 0 = Normal

    dataset = CyberGuardDataset(texts, labels, tokenizer)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    optimizer = AdamW(model.parameters(), lr=2e-5)

    epochs = 3
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for batch in dataloader:
            optimizer.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} - Loss NLP: {epoch_loss/len(dataloader):.4f}")

    # Salva o modelo treinado
    os.makedirs("src/models/weights", exist_ok=True)
    model.save_pretrained("src/models/weights/cyberguard_bert")
    tokenizer.save_pretrained("src/models/weights/cyberguard_bert")
    print("Modelo BERT salvo com sucesso.")

if __name__ == "__main__":
    train_cyberguard()
