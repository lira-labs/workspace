import os
import random
import csv
from PIL import Image, ImageDraw, ImageFont

# Diretórios
OUTPUT_DIR = 'data/raw/synthetic_ads'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Listas de geração
safe_titles = ["teddy bear", "pig plushy", "vintage doll", "antique cabinet"]
threat_titles = ["teddy bear", "pig plushy", "porcelain doll", "storage cabinet"]

safe_prices = [".00", ".50", "€15.00", ".00"]
threat_prices = [",000.00", "€31,500.70", ",000.00", "€80,000.00"]

safe_desc = [
    "Very good condition. Soft toys & stuffed animals.",
    "Uploaded 3 min ago. Needs a good home.",
    "Normal wear and tear. Shipping included."
]
threat_desc = [
    "6 years / 116 cm. Very good. Uploaded just now.",
    "newborn, 2 months, blonde, girl. tight.",
    "1.10 m tall, doesn't scream, 6 years old.",
    "9 Jahre alt, guter Zustand, Weiblich, Weiß."
]

def create_synthetic_ad_print(ad_id, is_threat):
    # Dimensões do print (estilo mobile)
    width, height = 400, 700
    img = Image.new('RGB', (width, height), color=(25, 25, 25)) # Fundo escuro (Dark mode)
    draw = ImageDraw.Draw(img)
    
    # 1. Simular a Imagem do Produto (Um retângulo cinza como placeholder da foto do urso/boneca)
    draw.rectangle([0, 0, width, 350], fill=(200, 200, 200))
    draw.text((120, 160), "[ FOTO DO PRODUTO ]", fill=(50, 50, 50))
    
    # Selecionar dados baseados na label
    title = random.choice(threat_titles) if is_threat else random.choice(safe_titles)
    price = random.choice(threat_prices) if is_threat else random.choice(safe_prices)
    desc = random.choice(threat_desc) if is_threat else random.choice(safe_desc)
    
    # 2. Desenhar Título
    draw.text((20, 370), title, fill=(255, 255, 255))
    
    # 3. Desenhar Subtítulo fake
    draw.text((20, 400), "Very good · Uploaded just now", fill=(150, 150, 150))
    
    # 4. Desenhar Preço (Verde/Azul claro como no print da Vinted)
    draw.text((20, 440), price, fill=(100, 200, 200))
    draw.text((20, 465), price + " Includes Buyer Protection", fill=(70, 150, 150))
    
    # 5. Linha divisória
    draw.line((0, 510, width, 510), fill=(50, 50, 50), width=2)
    
    # 6. Descrição
    draw.text((20, 530), "Description", fill=(200, 200, 200))
    
    # Quebra de linha simples para descrição
    words = desc.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) < 40:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    y_text = 570
    for line in lines:
        draw.text((20, y_text), line, fill=(255, 255, 255))
        y_text += 25
        
    filename = f"ad_print_{ad_id}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)
    img.save(filepath)
    
    return filename, title, price, desc, int(is_threat)

# Gerar Dataset (Vamos gerar 10 agora como prova de conceito. Para 1000, basta mudar o range)
print("Gerando fábrica de Datasets (Prints UI)...")
csv_data = [("filename", "title", "price", "description", "is_threat")]

for i in range(1, 11):
    is_threat = random.choice([True, False])
    data = create_synthetic_ad_print(i, is_threat)
    csv_data.append(data)

# Salvar o Ground Truth CSV
with open(os.path.join(OUTPUT_DIR, "dataset_labels.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print(f"Dataset gerado com sucesso em {OUTPUT_DIR}")
