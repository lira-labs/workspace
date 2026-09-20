import cv2
import torch
import numpy as np
from src.models.flood_unet import create_flood_model

class FloodDetector:
    def __init__(self, model_path=None, device="cpu"):
        self.device = device
        self.model = create_flood_model()
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=device))
        self.model.to(self.device)
        self.model.eval()

    def preprocess(self, image):
        # Resize para múltiplo de 32 (requisito da arquitetura U-Net)
        img = cv2.resize(image, (512, 512))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img / 255.0
        img = np.transpose(img, (2, 0, 1)) # HWC to CHW
        img = torch.tensor(img, dtype=torch.float32).unsqueeze(0)
        return img.to(self.device)

    def predict(self, image):
        tensor_img = self.preprocess(image)
        with torch.no_grad():
            output = self.model(tensor_img)
            mask = torch.sigmoid(output).squeeze().cpu().numpy()
        return (mask > 0.5).astype(np.uint8) * 255
