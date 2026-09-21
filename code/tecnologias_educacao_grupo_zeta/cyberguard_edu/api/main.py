from fastapi import FastAPI
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = FastAPI(title="CyberGuard Edu API", description="Detecção NLP de Dark Patterns e Textos Suspeitos")

class TextInput(BaseModel):
    text: str

try:
    tokenizer = BertTokenizer.from_pretrained("src/models/weights/cyberguard_bert")
    model = BertForSequenceClassification.from_pretrained("src/models/weights/cyberguard_bert")
    model.eval()
except:
    tokenizer = None
    model = None

@app.post("/analyze")
async def analyze_text(input_data: TextInput):
    if model is None:
        return {"error": "Modelo não treinado ainda. Rode train_nlp.py"}

    inputs = tokenizer(input_data.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    
    status = "Suspeito/Ameaça" if prediction == 1 else "Seguro"
    return {"text": input_data.text, "analysis": status, "engine": "BERT-Transformers"}
