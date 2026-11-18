---
name: research-methodology
description: Desenha Research Questions (RQs), hipóteses testáveis, protocolos experimentais, estudos de ablação, métricas de sistema/usuário e análise de ameaças à validade. Use ao planejar ou revisar Seções de Metodologia e Avaliação.
---

# Research Methodology & Experimental Design

## Procedimento
1. **Derivar RQs e Hipóteses:** Toda RQ deve estar vinculada a um método de mensuração viável e registrado em `research_questions.md`.
2. **Separar Dimensões de Avaliação:**
   - **Sistemas na Borda:** CPU (%), RAM (MB), latência (ms / FPS), tráfego de rede externo (bytes), latência de inferência local sob demanda.
   - **Qualidade de Inferência / Ablação:** comparar sinais isolados (somente SO vs. somente webcam) contra fusão multimodal; medir falsos positivos em cenários críticos (ex.: óculos, baixa luz, leitura em papel, modo hobby/jogos).
   - **Usabilidade & HCAI/SRL ($N$ participantes):** escore SUS (0–100), dimensões Likert (consciência metacognitiva, intrusividade/oportunidade do JITAI, diferenciação hobby vs. estudo, confiança na privacidade local) e análise qualitativa.
3. **Ameaças à Validade:** Declare explicitamente limitações internas (efeito Hawthorne, curta duração do piloto), externas (amostra de curso único, plataforma Windows-only) e de constructo (olhar/cadência não medem diretamente atenção cognitiva).
4. **Honestidade Epistêmica:** Se um experimento ainda não foi executado, declare explicitamente *"Não há evidências experimentais ainda para sustentar X"* e mantenha o protocolo separado dos resultados obtidos.
