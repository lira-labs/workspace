import os
import random
import csv
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'data/raw/synthetic_ads')
BASE_IMAGES_DIR = os.path.join(SCRIPT_DIR, 'data/raw/synthetic_images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Listar imagens base
base_images = [f for f in os.listdir(BASE_IMAGES_DIR) if f.endswith(('.jpg', '.png'))]
if not base_images:
    print("Nenhuma imagem base encontrada em", BASE_IMAGES_DIR)
    exit()

safe_titles = ["teddy bear", "pig plushy", "vintage doll", "antique cabinet"]
threat_titles = ["teddy bear", "pig plushy", "porcelain doll", "storage cabinet"]

safe_prices = [".00", ".50", "€15.00", ".00", "€35.00", ".99"]
threat_prices = [",000.00", "€31,500.70", ",000.00", "€80,000.00", ",000.00", "€100,000.00"]

safe_desc = [
    "Very good condition. Soft toys & stuffed animals.",
    "Uploaded 3 min ago. Needs a good home.",
    "Normal wear and tear. Shipping included.",
    "Found this in the attic. Looks cute.",
    "Barely used. Perfect for a gift."
]
threat_desc = [
    "6 years / 116 cm. Very good. Uploaded just now.",
    "newborn, 2 months, blonde, girl. tight.",
    "1.10 m tall, doesn't scream, 6 years old.",
    "9 Jahre alt, guter Zustand, Weiblich, Weiß.",
    "120cm, obedient, ready to ship today, 8 years.",
    "new arrival, 140cm tall, quiet, no issues."
]

def create_synthetic_ad_print(ad_id, is_threat):
    width, height = 400, 700
    img = Image.new('RGB', (width, height), color=(25, 25, 25))
    draw = ImageDraw.Draw(img)
    
    # 1. Colar a imagem base real (Crop para caber)
    base_img_name = random.choice(base_images)
    base_img_path = os.path.join(BASE_IMAGES_DIR, base_img_name)
    try:
        product_img = Image.open(base_img_path).convert("RGB")
        # Resize e crop
        product_img = product_img.resize((400, 400))
        product_img = product_img.crop((0, 0, width, 350))
        img.paste(product_img, (0, 0))
    except Exception as e:
        draw.rectangle([0, 0, width, 350], fill=(200, 200, 200))
    
    title = random.choice(threat_titles) if is_threat else random.choice(safe_titles)
    price = random.choice(threat_prices) if is_threat else random.choice(safe_prices)
    desc = random.choice(threat_desc) if is_threat else random.choice(safe_desc)
    
    draw.text((20, 370), title, fill=(255, 255, 255))
    draw.text((20, 400), "Very good · Uploaded just now", fill=(150, 150, 150))
    draw.text((20, 440), price, fill=(100, 200, 200))
    draw.text((20, 465), price + " Includes Buyer Protection", fill=(70, 150, 150))
    draw.line((0, 510, width, 510), fill=(50, 50, 50), width=2)
    draw.text((20, 530), "Description", fill=(200, 200, 200))
    
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

print("Gerando fabrica de 1000 Datasets (Prints UI com fotos reais)...")
csv_data = [("filename", "title", "price", "description", "is_threat")]

for i in range(1, 1001):
    is_threat = random.choice([True, False])
    data = create_synthetic_ad_print(i, is_threat)
    csv_data.append(data)

with open(os.path.join(OUTPUT_DIR, "dataset_labels.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)

print(f"1000 imagens geradas com sucesso em {OUTPUT_DIR}")
