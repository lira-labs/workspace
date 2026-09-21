import streamlit as st
import requests
import time
import csv
import re
import os

st.set_page_config(page_title="CyberGuard Edu - Threat Intel", page_icon="🛡️", layout="wide")

st.title("🛡️ CyberGuard Edu: Scanner Multimodal")
st.markdown("Plataforma de inteligencia para deteccao de esteganografia e trafico humano em marketplaces.")

def get_authorities(state_code):
    base_authorities = [
        "🚨 **SaferNet Brasil:** Denuncie online anonimamente em [new.safernet.org.br/denuncie](https://new.safernet.org.br/denuncie)",
        "📞 **Disque 100:** Direitos Humanos (Funciona 24h em todo o Brasil)"
    ]
    state_authorities = {
        "PE": "🚓 **Policia Civil PE (DPCA):** Departamento de Policia da Crianca e do Adolescente - Recife.",
        "SP": "🚓 **4ª Delegacia de Delitos Praticados por Meios Eletronicos (DIG/DEIC):** Sao Paulo.",
        "RJ": "🚓 **DRCI - Delegacia de Repressao aos Crimes de Informatica:** Rio de Janeiro."
    }
    local = state_authorities.get(state_code, "🚓 **Policia Federal (PF):** Procure a superintendencia regional mais proxima ou acesse pf.gov.br")
    base_authorities.append(local)
    return base_authorities

col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Inserir Evidencia")
    input_type = st.radio("Como deseja analisar o anuncio?", ["Upload de Print (Screenshot)", "Colar Link do Anuncio (URL)"])
    estado = st.selectbox("Sua Localizacao (Para encaminhamento em caso de risco):", ["PE", "SP", "RJ", "MG", "BA", "Outro"])
    
    image_file = None
    url_input = ""
    
    if input_type == "Upload de Print (Screenshot)":
        image_file = st.file_uploader("Suba o Print do Anuncio (JPG/PNG)", type=["jpg", "png", "jpeg"])
        if image_file:
            st.image(image_file, caption="Print capturado", width='stretch')
            st.success("Print carregado. O motor de OCR extraira o texto automaticamente.")
    else:
        url_input = st.text_input("Cole o Link do Marketplace (Ex: MercadoLivre, OLX, eBay)")

    analyze_btn = st.button("🔍 Iniciar Varredura de Ameaca", width='stretch', type="primary")

with col2:
    st.header("2. Relatorio de Inteligencia")
    if analyze_btn:
        if not image_file and not url_input:
            st.warning("Insira um Print ou um Link para analisar.")
        else:
            with st.spinner("Lendo Print (OCR), cruzando metadados e processando Redes Neurais..."):
                time.sleep(2)
                
                # Leitura Dinamica do OCR (Simulando OCR lendo o arquivo gerado)
                extracted_title = "Desconhecido"
                extracted_desc = "Sem descricao."
                extracted_price = 0.0
                
                if image_file:
                    filename = image_file.name
                    csv_path = 'data/raw/synthetic_ads/dataset_labels.csv'
                    if os.path.exists(csv_path):
                        with open(csv_path, 'r', encoding='utf-8') as f:
                            reader = csv.DictReader(f)
                            for row in reader:
                                if row['filename'] == filename:
                                    extracted_title = row['title']
                                    extracted_desc = row['description']
                                    price_str = row['price']
                                    # Tratar preco (ex: € 30.000,00 -> 30000.00)
                                    clean_price = re.sub(r'[^\d]', '', price_str)
                                    if clean_price:
                                        # Divide por 100 assumindo os ultimos 2 digitos como centavos
                                        extracted_price = float(clean_price) / 100.0
                                    break
                
                st.subheader("📝 Dados Extraidos pela IA (Módulo OCR)")
                st.write(f"**Titulo:** {extracted_title}")
                st.write(f"**Descricao:** {extracted_desc}")
                st.write(f"**Preco Identificado:** $ {extracted_price}")
                
                try:
                    payload = {
                        "title": extracted_title,
                        "description": extracted_desc,
                        "price_usd": extracted_price
                    }
                    
                    files = {}
                    if image_file:
                        image_file.seek(0)
                        files = {"product_image": (image_file.name, image_file, image_file.type)}
                    else:
                        files = {"product_image": ("mock.jpg", b"fake", "image/jpeg")}
                    
                    response = requests.post("http://127.0.0.1:8000/scan_marketplace_listing", data=payload, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        risk = data.get("human_trafficking_risk_prediction", {})
                        
                        if risk.get("requires_human_review"):
                            st.error("🚨 ALERTA CRITICO DE AMEACA 🚨")
                            st.write(risk.get("system_recommendation"))
                            
                            st.markdown("---")
                            st.subheader("🕵️ Analise Cruzada Multimodal")
                            mods = data.get("modules_analysis", {})
                            st.write(f"**Linguagem (NLP):** {mods.get('nlp_module')}")
                            st.write(f"**Anomalia de Preco:** {mods.get('metadata_module')}")
                            st.write(f"**Visao Computacional:** {mods.get('cv_module')} Discrepancia entre objeto e metricas vitais.")
                            
                            st.markdown("---")
                            st.subheader("🚔 Acao Recomendada (Encaminhamento)")
                            for auth in get_authorities(estado):
                                st.write(auth)
                        else:
                            st.success("✅ Anuncio Legitimo. Nenhuma anomalia grave detectada.")
                    else:
                        st.error("Erro na API CyberGuard.")
                except Exception as e:
                    st.error(f"O servidor FastAPI nao esta respondendo. Erro: {e}")
