# FloodVision Edu (Recife)

Sistema avançado de Visão Computacional para detecção de ruas alagadas (Urban Flood Detection) baseado na arquitetura EfficientNet-B4.

## Arquitetura Profunda
Diferente de protótipos simples, este repositório segue os padrões de produção em Deep Learning:
- **Modelo:** U-Net com backbone efficientnet-b4 (estado da arte em extração de features, otimizado para imagens complexas como chuvas).
- **Dados:** Suporte para o FloodNet ou V-FloodNet WaterDataset.
- **Backend:** FastAPI preparado para receber frames de câmeras CCTV em tempo real.
- **Pipeline:** Uso de Albumentations para aumento de dados simulando chuvas, ruídos noturnos e variação de câmera.

## Estrutura
- data/: Datasets crus e processados.
- src/models/: Definições da arquitetura neural.
- src/inference/: Scripts de inferência em vídeos e imagens.
- pi/: Rotas assíncronas em FastAPI.
