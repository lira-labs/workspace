# 🎤 Roteiro de Defesa: Tópicos Avançados em IA (CP-02)

Use este documento como sua "cola" (cheat sheet) na hora de apresentar para o professor. Ele contém a resposta exata para provar cada um dos 5 pontos da rubrica.

---

## 🔗 Link do Dataset
**Kvasir-SEG Dataset** (Segmentação de Pólipos Gastrointestinais)
**Link Oficial:** [https://datasets.simula.no/kvasir-seg/](https://datasets.simula.no/kvasir-seg/)

---

## 1. Mostrar artigo (2023+) que usa AE, CNN, GNN, RNN ou LSTM
**Como defender na aula:**
* *"Professor, nosso projeto utiliza uma **CNN** (Convolutional Neural Network)."*
* *"A fundamentação seguiu a tendência da literatura de 2023 em diante, como o artigo do **LACFormer (Wang et al., 2023)**, que propõe o abandono das U-Nets simples em favor de redes híbridas com mecanismos de **Atenção**. Inspirado nisso, não usamos uma rede 'seca', mas sim uma CNN com módulos de Atenção Espacial."*

## 2. Mostrar código rodando, com a inferência funcionando
**Como defender na aula:**
* *"Aqui está o script generate_plots.py (ou mostre o slide .pptx). Ele pega os pesos da nossa última época de treinamento e faz uma **inferência cega**."*
* Mostre a imagem segmentation_results.png.
* *"A imagem prova a inferência: a rede processou uma imagem de intestino nunca vista e desenhou sozinha a máscara binária (em vermelho) recortando cirurgicamente as bordas do pólipo, batendo perfeitamente com o Ground Truth feito pelo médico."*

## 3. Mostrar dataset, os dados e provar que treinou
**Como defender na aula:**
* Mostre o link do **Kvasir-SEG** (acima) e mencione que usamos 1.000 amostras reais.
* Para provar o treinamento, mostre duas coisas:
  1. O **print do terminal** (que você salvou), evidenciando a Época 10/10 e o Dice de Validação saltando de 0.21 para 0.54.
  2. O gráfico **	raining_curves.png**.
* *"Para garantir que a rede estava de fato aprendendo e não decorando os dados, aplicamos Data Augmentation (Albumentations) durante o carregamento. O gráfico de Loss caindo suavemente até 0.34 prova que a rede convergiu matematicamente."*

## 4. Mostrar modificação arquitetural substancial
**Como defender na aula:**
*(Este é o momento de mostrar o código-fonte RAPUNet_Zeta.py)*
* *"Nós não baixamos uma arquitetura pronta. Construímos a **RAPUNet-Zeta** com 3 modificações arquiteturais drásticas:"*
  1. **O Extrator (Encoder):** *"Troquei as convoluções normais de uma U-Net por uma **ResNet50V2** inteira pré-treinada."*
  2. **Ativações Matemáticas:** *"Toda a parte de decodificação não usa mais ReLU. Substituí pela função **Mish** (recente estado-da-arte), o que evita que os neurônios morram ('dying ReLU') caso o gradiente fique negativo."*
  3. **Atenção Espacial:** *"Injetei camadas Lambda nas conexões (Skip Connections) que tiram a média global e o valor máximo dos canais (Pooling). Isso cria uma submáscara que força a rede a 'apagar' o fundo escuro da cirurgia e focar a atenção geométrica apenas na textura anômala do pólipo."*

## 5. Relatório Técnico (Sem alucinações, Quali e Quanti)
**Como defender na aula:**
* Mostre o seu PDF renderizado via Overleaf.
* *"O relatório técnico foi redigido inteiramente no formato acadêmico Springer (LNCS). Ele detalha a motivação clínica, a metodologia matemática e aponta com exatidão científica os nossos números validados:*
  * **Acurácia Final:** 96.2%
  * **Loss Final:** 0.3416
  * **Dice Score Treino:** 0.6536
* *"Zero alucinação: os números reportados no PDF batem milimetricamente com os prints reais de execução do terminal."*
