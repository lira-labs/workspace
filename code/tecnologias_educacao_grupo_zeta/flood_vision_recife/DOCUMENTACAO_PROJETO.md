# 🌊 FloodVision Edu: Sistema de Rotas Escolares Seguras (Recife)

**Disciplina:** Tecnologias na Educação
**Equipe:** Grupo Zeta

---

## 1. O Problema e a Conexão Educacional
Durante os períodos de chuva extrema na cidade do Recife, a locomoção de ônibus escolares e estudantes torna-se crítica e perigosa. Atualmente, a identificação de alagamentos depende de relatos informais ou de sensores caros.
**A Solução (Tech for Good):** Utilizar Inteligência Artificial (Visão Computacional) conectada às câmeras de trânsito (CCTV) para segmentar e medir o nível de inundações em tempo real, alertando escolas e pais sobre rotas intransitáveis.

---

## 2. A Arquitetura Técnica (Estado da Arte)
Para garantir profundidade técnica e nos afastar de protótipos superficiais, a infraestrutura foi montada seguindo padrões da indústria de Engenharia de Machine Learning:

### 🧠 A. Modelo Neural Profundo
- **Arquitetura:** U-Net com backbone **EfficientNet-B4** (via segmentation-models-pytorch).
- **Por que?** É o mesmo núcleo extrator de características utilizado no *V-FloodNet* (artigo base), comprovadamente superior em tarefas complexas de segmentação de reflexos de água.
- **Função de Perda:** BCEWithLogitsLoss otimizada com Adam.

### 🎥 B. Backend de Alta Performance
- **Framework:** FastAPI (Python).
- **Por que?** Ao contrário de dashboards simples, o FastAPI é assíncrono e suporta altíssima concorrência. Ele está preparado para, no futuro, receber dezenas de frames por segundo de câmeras RTSP (Real-Time Streaming Protocol).

### 🌧️ C. Pipeline de Dados (Realidade de Recife)
- **Dataset:** 9.4 Gigabytes do repositório oficial *V-FloodNet* (via Hugging Face), incluindo o WaterDataset (imagens) e vídeos reais de enchentes urbanas.
- **Data Augmentation:** Uso pesado da biblioteca Albumentations. O modelo não aprende apenas com fotos limpas; injetamos matematicamente MotionBlur (borrão de movimento), GaussNoise (ruído de câmera barata de segurança) e alterações de contraste para simular chuvas noturnas e neblina.

---

## 3. Status Atual do Repositório
A base estrutural está **100% implementada** no repositório central (lira-labs/workspace):
- [x] Scaffold do projeto ML (Pastas src, data, pi).
- [x] Download completo do Dataset (10 GB armazenados via Git LFS).
- [x] Lógica de Dataloaders e Augmentation (dataset.py).
- [x] Loop de Treinamento em PyTorch (	rain.py).
- [x] Rotas de API FastAPI prontas para inferência.

**Próximo Passo (Fase de Computação):** Extrair os arquivos .zip do dataset bruto e rodar o 	rain.py para gerar o arquivo de pesos (.pth), tornando a IA funcional.
