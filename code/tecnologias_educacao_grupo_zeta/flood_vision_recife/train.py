import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from src.data.dataset import FloodDataset, get_training_augmentation
from src.models.flood_unet import create_flood_model
import os

def train_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Iniciando treinamento no dispositivo: {device}")

    # Configuração de dados
    images_dir = "data/raw/train_images"
    masks_dir = "data/raw/train_masks"
    
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)

    dataset = FloodDataset(images_dir, masks_dir, transform=get_training_augmentation())
    
    # Prevenção caso o dataset ainda esteja baixando os blobs do LFS
    if len(dataset) == 0:
        print("Dataset vazio ou LFS não sincronizado. Insira imagens em data/raw/train_images.")
        return

    dataloader = DataLoader(dataset, batch_size=4, shuffle=True, num_workers=2)

    # Modelo, Loss e Otimizador
    model = create_flood_model().to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    epochs = 10
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0
        for images, masks in dataloader:
            images = images.to(device)
            masks = masks.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, masks)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
        
        print(f"Epoch {epoch+1}/{epochs} - Loss: {epoch_loss/len(dataloader):.4f}")
        
        # Salva checkpoint
        torch.save(model.state_dict(), f"src/models/flood_unet_epoch_{epoch+1}.pth")

if __name__ == "__main__":
    train_model()
