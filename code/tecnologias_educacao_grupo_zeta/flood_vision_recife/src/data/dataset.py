import os
import cv2
import numpy as np
import torch
from torch.utils.data import Dataset
import albumentations as A

class FloodDataset(Dataset):
    def __init__(self, images_dir, masks_dir, transform=None):
        self.images_dir = images_dir
        self.masks_dir = masks_dir
        # Pega apenas arquivos válidos
        self.images = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.png'))]
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_name = self.images[idx]
        img_path = os.path.join(self.images_dir, img_name)
        mask_path = os.path.join(self.masks_dir, img_name.replace('.jpg', '.png'))

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Se não houver máscara ainda, cria uma vazia para teste
        if os.path.exists(mask_path):
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        else:
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

        # Binariza a máscara
        mask = (mask > 0).astype(np.float32)

        if self.transform:
            augmented = self.transform(image=image, mask=mask)
            image = augmented['image']
            mask = augmented['mask']

        # HWC para CHW
        image = np.transpose(image, (2, 0, 1)).astype(np.float32) / 255.0
        
        return torch.tensor(image), torch.tensor(mask).unsqueeze(0)

# Augmentations robustos para simular condições de rua/CCTV no Recife
def get_training_augmentation():
    return A.Compose([
        A.Resize(512, 512),
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(p=0.2),
        A.MotionBlur(p=0.2), # Câmeras balançando na chuva
        A.GaussNoise(p=0.1)
    ])
