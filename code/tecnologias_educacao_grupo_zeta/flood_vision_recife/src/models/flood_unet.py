import torch
import segmentation_models_pytorch as smp

def create_flood_model(backbone="efficientnet-b4", encoder_weights="imagenet"):
    """
    Cria a rede neural profunda para segmentação de água.
    Utilizamos a arquitetura U-Net baseada nos achados do V-FloodNet.
    """
    model = smp.Unet(
        encoder_name=backbone,
        encoder_weights=encoder_weights,
        in_channels=3,
        classes=1, # Máscara binária: 1 = Água/Alagamento, 0 = Fundo
    )
    return model
