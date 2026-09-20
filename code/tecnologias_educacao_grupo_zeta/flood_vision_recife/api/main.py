from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from src.inference.detector import FloodDetector
from fastapi.responses import JSONResponse

app = FastAPI(title="FloodVision Edu API", description="API de inferência para detecção de rotas alagadas.")
# Incializa o detector (no futuro, apontará para o modelo treinado real)
detector = FloodDetector(device="cpu")

@app.post("/predict")
async def predict_flood(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Executa a inferência profunda
    mask = detector.predict(img)
    
    # Calcula a porcentagem de área alagada
    water_ratio = np.sum(mask > 0) / mask.size
    
    status = "ALERTA: Rota Bloqueada" if water_ratio > 0.15 else "Seguro"
    
    return JSONResponse(content={
        "status": status,
        "water_percentage": round(water_ratio * 100, 2),
        "message": "Inferência processada via CNN EfficientNet-B4."
    })
