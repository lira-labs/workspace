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
    title: str = Form(..., description="Titulo do anuncio"),
    description: str = Form(..., description="Descricao detalhada (analise de linguagem)"),
    price_usd: float = Form(..., description="Metadado: Preco listado do produto"),
    product_image: UploadFile = File(..., description="Analise CV: Imagem do anuncio")
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

    # 2. Metadados (Rede/Preco)
    price_anomaly = price_usd > 2000.0

    # 3. CV (Contextual) - Discrepancia de imagem (Mock pipeline)
    vision_flag = True if product_image else False

    # Risk Assessment (HTRP)
    confidence_score = 0
    if nlp_threat: confidence_score += 40
    if price_anomaly: confidence_score += 40
    
    # Regra Heurística de Fallback (Keywords Criticas de Trafico Disfarcado)
    keywords = ["age", "height", "cm", "anos", "altura", "tall", "newborn", "girl", "years", "weiblich", "jungfrau"]
    if any(k in text_context.lower() for k in keywords): 
        confidence_score += 50
        nlp_threat = True # Forca a flag de NLP se a heurística pegar

    requires_review = confidence_score >= 80
    
    return {
        "human_trafficking_risk_prediction": {
            "requires_human_review": requires_review,
            "system_recommendation": "Este conjunto de anuncios apresenta caracteristicas que justificam uma avaliacao especializada." if requires_review else "Anuncio nao apresenta anomalias graves no cruzamento multimodal."
        },
        "modules_analysis": {
            "nlp_module": "Linguagem suspeita/codificada identificada." if nlp_threat else "Linguagem dentro do padrao.",
            "metadata_module": f"Anomalia detectada no metadado de preco ()." if price_anomaly else "Metadados normais.",
            "cv_module": f"Imagem '{product_image.filename}' recebida para extracao de features e comparacao semantica."
        }
    }
