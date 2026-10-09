# MANIFESTO DE PROJETO CIENTÍFICO (PROJECT MANIFEST)

- **Título do Manuscrito:** Investigação e Implementação de Redes Neurais Convolucionais em Tópicos Avançados de Inteligência Artificial
- **Título Curto (Runninghead):** Modelos Convolucionais Avançados em IA
- **Autores:** Cauã Lira (UFRPE)
- **Venue Alvo / Padrão Editorial:** Springer LNCS / LNAI (Padrão BRACIS)
- **Classe TeX:** llncs.cls (v2.25)
- **Estilo Bibliográfico:** splncs04.bst (BibTeX)
- **Compilador Recomendado:** pdfLaTeX (TeX Live)
- **Idioma:** Manuscrito Técnico com Abstract e Keywords em Inglês

## Status das Seções
- [x] `main.tex`: FINAL (Preâmbulo sanitizado, metadados e pacotes essenciais)
- [x] `01_introducao.tex`: FINAL (Funil em 9 etapas, contexto clínico do CCR e 3 contribuições explícitas)
- [x] `02_trabalhos_relacionados.tex`: FINAL (Taxonomia U-Net, CBAM, LACFormer 2023 e lacuna)
- [x] `03_metodologia.tex`: FINAL (Kvasir-SEG, Albumentations, ResNet50V2, SAM com equações, Mish e Dice Loss)
- [x] `04_experimentos.tex`: FINAL (Tabela de benchmarks, ablação em 4 estágios, curvas de treino e inferência cega)
- [x] `05_conclusao.tex`: FINAL (Síntese das evidências, limitações monocêntricas e 3 trabalhos futuros)
- [x] `references.bib`: FINAL (7 referências canônicas verificadas sem alucinação)

## Inventário de Figuras
1. `figures/dataset_samples.png`: Exemplos clínicos reais do Kvasir-SEG e máscaras de especialistas
2. `figures/architecture_rapunet.png`: Diagrama de blocos de alta resolução da RAPUNet-Zeta com detalhamento matemático do SAM
3. `figures/metrics_comparison.png`: Gráfico de barras comparativo de métricas (Dice, mIoU, Acurácia)
4. `figures/training_curves.png`: Curvas empíricas reais de convergência (Dice Loss vs. Dice Score)
5. `figures/segmentation_results.png`: Painel qualitativo de inferência cega (Imagem vs. Ground Truth vs. Predição)

## Inventário de Tabelas
- **Tabela 1:** Avaliação Quantitativa Comparativa no Dataset Kvasir-SEG (U-Net vs. ResUNet vs. RAPUNet-Zeta)
- **Tabela 2:** Estudo de Ablação dos Componentes Arquiteturais (Encoder, Ativação, Atenção)

## Auditoria de Conformidade (Definition of Done)
- [x] Camada 1 (Formato e Template): Respeitado padrão Springer LNCS
- [x] Camada 2 (LaTeX e Compilação): Zero dependências ausentes, todas as imagens e chaves resolvidas
- [x] Camada 3 (Validade Científica): Dados rastreáveis ao Kvasir-SEG e logs do train_zeta.py
- [x] Camada 4 (Integridade de Citações): Referências 100% verificadas
- [x] Camada 5 (Revisão Adversarial): Linguagem acadêmica sóbria, sem marketing ou jargões de IA
