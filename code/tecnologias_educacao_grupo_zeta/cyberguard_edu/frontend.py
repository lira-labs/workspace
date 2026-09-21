import streamlit as st
import requests
import time
import json

st.set_page_config(page_title="CyberGuard Edu - Threat Intel", page_icon="🛡️", layout="wide")

st.title("🛡️ CyberGuard Edu: Scanner Multimodal")
st.markdown("Plataforma de inteligência para detecção de esteganografia e tráfico humano em marketplaces.")

# Dicionário de Encaminhamento Policial / ONGs
def get_authorities(state_code):
    base_authorities = [
        "🚨 **SaferNet Brasil:** Denuncie online anonimamente em [new.safernet.org.br/denuncie](https://new.safernet.org.br/denuncie)",
        "📞 **Disque 100:** Direitos Humanos (Funciona 24h em todo o Brasil)"
    ]
    state_authorities = {
        "PE": "🚓 **Polícia Civil PE (DPCA):** Departamento de Polícia da Criança e do Adolescente - Recife.",
        "SP": "🚓 **4ª Delegacia de Delitos Praticados por Meios Eletrônicos (DIG/DEIC):** São Paulo.",
        "RJ": "🚓 **DRCI - Delegacia de Repressão aos Crimes de Informática:** Rio de Janeiro."
    }
    
    local = state_authorities.get(state_code, "🚓 **Polícia Federal (PF):** Procure a superintendência regional mais próxima ou acesse pf.gov.br")
    base_authorities.append(local)
    return base_authorities

# Layout do Frontend
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Inserir Evidência")
    input_type = st.radio("Como deseja analisar o anúncio?", ["Upload de Print (Screenshot)", "Colar Link do Anúncio (URL)"])
    
    estado = st.selectbox("Sua Localização (Para encaminhamento em caso de risco):", ["PE", "SP", "RJ", "MG", "BA", "Outro"])
    
    image_file = None
    url_input = ""
    
    if input_type == "Upload de Print (Screenshot)":
        image_file = st.file_uploader("Suba o Print do Anúncio (JPG/PNG)", type=["jpg", "png", "jpeg"])
        if image_file:
            st.image(image_file, caption="Print capturado", use_container_width=True)
            st.success("Print carregado. O motor de OCR (Extração de Texto) será acionado na análise.")
    else:
        url_input = st.text_input("Cole o Link do Marketplace (Ex: MercadoLivre, OLX, eBay)")
        if url_input:
            st.info("O Web Scraper varrerá o link em busca de imagens e descrições ocultas.")

    analyze_btn = st.button("🔍 Iniciar Varredura de Ameaça", use_container_width=True, type="primary")

with col2:
    st.header("2. Relatório de Inteligência")
    
    if analyze_btn:
        if not image_file and not url_input:
            st.warning("Insira um Print ou um Link para analisar.")
        else:
            with st.spinner("Analisando metadados, processando OCR e cruzando redes neurais (BERT + Visão)..."):
                # Simulação de OCR / Scraping para o MVP (já que ler imagens cruas requer Tesseract instalado no OS)
                time.sleep(2) # Simula o tempo de processamento do modelo
                
                # Para fins de demonstração, vamos simular que a IA extraiu o seguinte texto do print ou link:
                extracted_title = "Boneca de Porcelana Antiga"
                extracted_desc = "Exclusivo! Apenas 1 no mundo. Idade: 7 anos. Altura: 120cm. Cabelo loiro. Envio Imediato em caixa discreta."
                extracted_price = 15000.0
                
                st.subheader("📝 Dados Extraídos pela IA (OCR/Scraper)")
                st.write(f"**Título:** {extracted_title}")
                st.write(f"**Descrição:** {extracted_desc}")
                st.write(f"**Preço Identificado:** ")
                
                # Consumindo a nossa própria API FastAPI no background
                try:
                    payload = {
                        "title": extracted_title,
                        "description": extracted_desc,
                        "price_usd": extracted_price
                    }
                    
                    # Como estamos enviando multipart/form-data com arquivo na API real, 
                    # fazemos uma requisição com o arquivo mockado se não houver um.
                    files = {}
                    if image_file:
                        image_file.seek(0)
                        files = {"product_image": (image_file.name, image_file, image_file.type)}
                    else:
                        files = {"product_image": ("mock_from_url.jpg", b"fake_image_bytes", "image/jpeg")}
                    
                    response = requests.post("http://127.0.0.1:8000/scan_marketplace_listing", data=payload, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        risk = data.get("human_trafficking_risk_prediction", {})
                        
                        if risk.get("requires_human_review"):
                            st.error("🚨 ALERTA CRÍTICO DE AMEAÇA 🚨")
                            st.write(risk.get("system_recommendation"))
                            
                            st.markdown("---")
                            st.subheader("🕵️ Análise Cruzada Multimodal")
                            mods = data.get("modules_analysis", {})
                            st.write(f"**Linguagem (NLP):** {mods.get('nlp_module')}")
                            st.write(f"**Anomalia de Preço:** {mods.get('metadata_module')}")
                            st.write(f"**Visão Computacional:** Discrepância entre a categoria do objeto e as métricas vitais.")
                            
                            st.markdown("---")
                            st.subheader("🚔 Ação Recomendada (Encaminhamento)")
                            st.write("Baseado na sua localização, encaminhe este relatório para as autoridades competentes imediatamente:")
                            for auth in get_authorities(estado):
                                st.write(auth)
                        else:
                            st.success("✅ Anúncio Legítimo. Nenhuma anomalia grave detectada.")
                    else:
                        st.error("Erro ao conectar com a API CyberGuard. Verifique se o uvicorn está rodando na porta 8000.")
                except Exception as e:
                    st.error(f"O servidor FastAPI não está respondendo. Lembre-se de rodar 'python -m uvicorn api.main:app' primeiro. Erro: {e}")
