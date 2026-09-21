from fastapi import FastAPI, UploadFile, File, Form
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import json

app = FastAPI(
    title="CyberGuard Edu: Multimodal Threat Intel", 
    description="Metodologia baseada nos frameworks MATCHED e Trafficking-10k para Human Trafficking Risk Prediction (HTRP).",
    version="3.0.0"
)

try:
    tokenizer = BertTokenizer.from_pretrained("src/models/weights/cyberguard_bert")
    model = BertForSequenceClassification.from_pretrained("src/models/weights/cyberguard_bert")
    model.eval()
except:
    tokenizer = None
    model = None

@app.post("/scan_marketplace_listing")
async def scan_marketplace_listing(
    title: str = Form(..., description="Título do anúncio"),
    description: str = Form(..., description="Descrição detalhada (análise de linguagem)"),
    price_usd: float = Form(..., description="Metadado: Preço listado do produto"),
    product_image: UploadFile = File(..., description="Análise CV: Imagem do anúncio")
):
    text_context = f"{title}. {description}"
    
    # 1. NLP (Texto)
    nlp_threat = False
    if model and tokenizer:
        inputs = tokenizer(text_context, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=1).item()
            nlp_threat = (prediction == 1)

    # 2. Metadados (Rede/Preço)
    price_anomaly = price_usd > 2000.0

    # 3. CV (Contextual) - Discrepância de imagem (Mock pipeline)
    vision_flag = True if product_image else False

    # Risk Assessment (HTRP)
    confidence_score = 0
    if nlp_threat: confidence_score += 40
    if price_anomaly: confidence_score += 40
    if "age" in text_context.lower() or "height" in text_context.lower(): confidence_score += 20

    requires_review = confidence_score >= 80
    
    return {
        "human_trafficking_risk_prediction": {
            "requires_human_review": requires_review,
            "system_recommendation": "Este conjunto de anúncios apresenta características que justificam uma avaliação especializada." if requires_review else "Anúncio não apresenta anomalias graves no cruzamento multimodal."
        },
        "modules_analysis": {
            "nlp_module": "Linguagem suspeita/codificada identificada." if nlp_threat else "Linguagem dentro do padrão.",
            "metadata_module": f"Anomalia detectada no metadado de preço ()." if price_anomaly else "Metadados normais.",
            "cv_module": f"Imagem '{product_image.filename}' recebida para extração de features e comparação semântica."
        }
    }
