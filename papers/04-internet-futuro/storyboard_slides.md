# Storyboard Editorial — Telessaúde Segura no Interior (2ª VA · Internet do Futuro)

> **Autor:** Cauã Lira (Licenciatura em Computação · UFRPE)  
> **Disciplina:** Internet do Futuro · Profa. Jeisa Pereira de Oliveira Domingues  
> **Formato:** Vídeo de apresentação (8m30s a 9m00s, teto de 10 min) · 9 slides 16:9  
> **Base:** `papers/04-internet-futuro/roteiro_video.md` e `papers/04-internet-futuro/main.tex`

---

## Etapa 1: DNA da Apresentação & Identidade Visual

- **Propósito:** Tirar a Criptografia Pós-Quântica da teoria de grandes bancos e mostrar como ela protege exames e prontuários no interior do Brasil quando combinada com Satélites LEO, Computação de Borda e Zero Trust.
- **Tom e Voz:** Simples, humano, direto e conversacional (tom de sala de aula explicando para colegas). Zero jargões desnecessários, zero listas longas de bullet points.
- **Regra de Ouro Anti-Slop:**
  1. Todos os títulos comunicam uma **ideia ou ação** (nunca rótulos genéricos como "Introdução" ou "Conclusão").
  2. Máximo de **30 a 40 palavras visíveis** por slide.
  3. **Variedade intencional:** dois slides consecutivos nunca usam o mesmo layout.
- **Paleta Oficial (alinhada ao documento LaTeX):**
  - **Azul Principal (PQC / Central):** `#1F3A5F`
  - **Azul Claro (Cards suaves):** `#E8EEF5`
  - **Verde Borda (Edge Computing):** `#2E7D5B`
  - **Laranja Satélite (Satélites LEO):** `#C8642B`
  - **Roxo Zero Trust (Controle de Acesso):** `#6A4C93`
  - **Cinza Apoio:** `#5A5A5A`
  - **Fundo Editorial:** `#FFFFFF` / `#F8FAFC`

---

## Etapa 2: Arco Narrativo & Mapa de Variedade Visual

| Slide | Tempo | Layout / Composição | Título de Ação | Mídia Principal |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 00:00–00:50 | Capa Editorial Limpa | *Telessaúde segura no interior: protegendo exames por décadas com criptografia pós-quântica* | `figures/brasao_ufrpe.png` |
| **2** | 00:50–02:00 | Split Assimétrico (2 cenas reais) | *Dados de saúde duram décadas, mas a criptografia atual tem prazo de validade* | `figures/posto_sertao.jpg` + `figures/colha_agora.jpg` |
| **3** | 02:00–03:15 | Número Herói + Contraste Visual | *A criptografia pós-quântica roda nos computadores de hoje, mas exige chaves bem maiores* | `figures/ibm_quantum.jpg` + Novo gráfico (32 B vs 3.309 B) |
| **4** | 03:15–04:30 | Grade 2x2 de Cards Coloridos | *Quatro tecnologias se unem para cobrir os pontos fracos umas das outras* | Novo infográfico de 4 cards (sem foto) |
| **5** | 04:30–06:00 | Diagrama em 4 Camadas + Barra Transversal | *Os dados saem protegidos do posto e atravessam o satélite sem exposição* | Novo diagrama limpo (base `fig:arquitetura`) + `figures/starlink_antena.jpg` |
| **6** | 06:00–07:15 | Cena Humana + Fluxo Numerado (1 a 6) | *O exame do Seu José chega seguro ao cardiologista em 6 passos* | `figures/seu_jose_ecg.jpg` + Novo fluxo vertical 1–6 (base `fig:caminho`) |
| **7** | 07:15–08:30 | Tabela de Métricas Limpa + Faixa de Limites | *Quatro métricas testam o posto piloto, sem esconder os riscos* | Nova tabela limpa (base `tab:metricas`) + tags FOFA |
| **8** | 08:30–09:15 | Foto Hero com Cartão Flutuante | *A tecnologia já existe hoje; o próximo passo é um piloto com o SUS* | `figures/chuva_borda.jpg` |
| **9** | 09:15–09:40 | Encerramento Minimalista em 2 Colunas | *Segurança pós-quântica para proteger a dignidade de quem mora longe* | Tipografia limpa (opcional: detalhe sutil `figures/ribeirinha_prenatal.jpg` ou fundo limpo) |

---

## Etapa 3: Storyboard Detalhado (Slides 1 a 9)

### Slide 1 · Capa Editorial Limpa (`00:00 – 00:50`)
- **Layout:** Faixa superior fina em `#1F3A5F`, brasão centralizado no topo, título grande à esquerda/centro com respiro amplo, metadados acadêmicos alinhados na base.
- **Título de Ação:** *Telessaúde segura no interior: protegendo exames por décadas com criptografia pós-quântica*
- **Texto Visível no Slide (~36 palavras):**
  - **Título:** Telessaúde segura no interior: protegendo exames por décadas com criptografia pós-quântica
  - **Subtítulo:** Satélites LEO, Computação de Borda e Zero Trust
  - **Rodapé:** Cauã Lira · Licenciatura em Computação · UFRPE | 2ª VA — Internet do Futuro · Profa. Jeisa Domingues
- **Mídia:** `papers/04-internet-futuro/figures/brasao_ufrpe.png`
- **Sincronia com a Fala:** Apresentação pessoal, conexão com o seminário da 1ª VA (PQC) e gancho humano: proteger exames no interior isolado.

---

### Slide 2 · Split Assimétrico com Duas Cenas Reais (`00:50 – 02:00`)
- **Layout:** Título de ação no topo; área principal dividida em duas colunas assimétricas (50%/50%) com fotos grandes em moldura limpa e legenda curta abaixo de cada imagem.
- **Título de Ação:** *Dados de saúde duram décadas, mas a criptografia atual tem prazo de validade*
- **Texto Visível no Slide (~35 palavras):**
  - **Título:** Dados de saúde duram décadas, mas a criptografia atual tem prazo de validade
  - **Legenda Esquerda:** Sem fibra ou 4G, o posto no interior depende de satélite.
  - **Legenda Direita:** Ataque "colha agora, abra depois": cópias de hoje expostas no futuro.
- **Mídia:**
  - Esquerda: `papers/04-internet-futuro/figures/posto_sertao.jpg`
  - Direita: `papers/04-internet-futuro/figures/colha_agora.jpg`
- **Sincronia com a Fala:** Lei da Telessaúde (2022), realidade do sertão e Amazônia, sigilo vitalício de prontuários (LGPD) e o risco imediato do ataque *colha agora, descriptografe depois*.

---

### Slide 3 · Número Herói + Contraste Visual (`02:00 – 03:15`)
- **Layout:** Coluna esquerda (40%) com foto real do computador quântico; coluna direita (60%) com contraste visual de **Número Herói** mostrando o salto de tamanho das chaves + frase-síntese na base.
- **Título de Ação:** *A criptografia pós-quântica roda nos computadores de hoje, mas exige chaves bem maiores*
- **Texto Visível no Slide (~36 palavras):**
  - **Título:** A criptografia pós-quântica roda nos computadores de hoje, mas exige chaves bem maiores
  - **Número Herói (Gráfico):** `32 B` (atual) → `3.309 B` (ML-DSA)
  - **Apoio Foto:** Padrões NIST 2024: ML-KEM (chaves) e ML-DSA (assinaturas).
  - **Gancho:** Aparelhos simples não aguentam esse peso sozinhos.
- **Mídia:**
  - Esquerda: `papers/04-internet-futuro/figures/ibm_quantum.jpg`
  - Direita: **Novo gráfico de contraste limpo** (2 barras horizontais proporcionais comparando X25519/Ed25519 `32 B` vs ML-KEM-768 `1.184 B` e ML-DSA-65 `3.309 B`, baseado em `tab:chaves`).
- **Sincronia com a Fala:** Desmistificar que PQC não precisa de computador quântico para rodar, explicar ML-KEM e ML-DSA (NIST 2024) e puxar a limitação da 1ª VA para introduzir os colegas.

---

### Slide 4 · Grade 2x2 de Cards Coloridos (`03:15 – 04:30`)
- **Layout:** Grid 2x2 simétrico com cards de borda esquerda colorida (identidade de cada tecnologia) sobre fundo `#F8FAFC`. Sem fotos para dar respiro visual após os slides 2 e 3.
- **Título de Ação:** *Quatro tecnologias se unem para cobrir os pontos fracos umas das outras*
- **Texto Visível no Slide (~37 palavras):**
  - **Título:** Quatro tecnologias se unem para cobrir os pontos fracos umas das outras
  - **Card 1 (`#1F3A5F`):** **PQC (Cauã):** protege hoje e no futuro.
  - **Card 2 (`#C8642B`):** **Satélites LEO (Alexander):** conectam áreas isoladas.
  - **Card 3 (`#2E7D5B`):** **Borda (Daniel):** processa no posto.
  - **Card 4 (`#6A4C93`):** **Zero Trust (João Victor):** valida cada acesso.
- **Mídia:** **Novo infográfico em grade 2x2** com ícones vetoriais mínimos (cadeado, satélite, mini servidor, escudo) adaptado de `tab:papeis`.
- **Sincronia com a Fala:** Dar crédito aos seminários dos colegas (Alexander, Daniel e João Victor Vasconcelos) e explicar a complementaridade: a borda alivia o peso da PQC; a PQC esconde os dados da dona do satélite; o Zero Trust bloqueia invasores locais.

---

### Slide 5 · Diagrama em 4 Camadas + Barra Transversal (`04:30 – 06:00`)
- **Layout:** Fluxo horizontal em 4 blocos conectados da esquerda para a direita no centro do slide, sustentados por uma barra roxa transversal na base ("Zero Trust"). Miniatura discreta da antena no canto superior direito.
- **Título de Ação:** *Os dados saem protegidos do posto e atravessam o satélite sem exposição*
- **Texto Visível no Slide (~37 palavras):**
  - **Título:** Os dados saem protegidos do posto e atravessam o satélite sem exposição
  - **Bloco 1:** 1. Aparelhos: ECG e tablet
  - **Bloco 2:** 2. Borda: assina e cifra
  - **Bloco 3:** 3. Satélite LEO: só transporta
  - **Bloco 4:** 4. Hospital: valida e guarda
  - **Barra Base:** Zero Trust: confere cada passo
- **Mídia:**
  - Principal: **Novo diagrama limpo em 4 camadas + base transversal** (versão simplificada para slides de `fig:arquitetura` do `main.tex`, com as 4 cores oficiais).
  - Apoio (canto superior direito): `papers/04-internet-futuro/figures/starlink_antena.jpg`
- **Sincronia com a Fala:** Explicar cada camada na ordem exata do roteiro (Dispositivos → Borda com fila offline → Transporte LEO cego ao conteúdo → Hospital Central → Zero Trust contínuo).

---

### Slide 6 · Cena Humana + Fluxo Numerado Passo a Passo (`06:00 – 07:15`)
- **Layout:** Foto humana ocupando 45% à esquerda; 55% à direita com linha vertical numerada de 1 a 6 (círculos coloridos conectados, zero parágrafos).
- **Título de Ação:** *O exame do Seu José chega seguro ao cardiologista em 6 passos*
- **Texto Visível no Slide (~35 palavras):**
  - **Título:** O exame do Seu José chega seguro ao cardiologista em 6 passos
  - **Passo 1:** 1. ECG no posto
  - **Passo 2:** 2. Zero Trust valida
  - **Passo 3:** 3. Borda assina (ML-DSA)
  - **Passo 4:** 4. Satélite LEO transporta
  - **Passo 5:** 5. Hospital confere
  - **Passo 6:** 6. Médico abre vídeo
- **Mídia:**
  - Esquerda: `papers/04-internet-futuro/figures/seu_jose_ecg.jpg`
  - Direita: **Novo infográfico vertical 1–6** (adaptação enxuta de `fig:caminho` do `main.tex`).
- **Sincronia com a Fala:** Contar a história do Seu José (67 anos, dor no peito no distrito rural) percorrendo os 6 passos até a teleconsulta com o cardiologista no Recife.

---

### Slide 7 · Tabela de Métricas Limpa + Faixa de Limites (`07:15 – 08:30`)
- **Layout:** Tabela limpa e espaçada no centro (4 linhas, fundo alternado `#E8EEF5` / `#FFFFFF`) ocupando 75% da altura; faixa horizontal discreta na base destacando os limites reais do projeto.
- **Título de Ação:** *Quatro métricas testam o posto piloto, sem esconder os riscos*
- **Texto Visível no Slide (~36 palavras):**
  - **Título:** Quatro métricas testam o posto piloto, sem esconder os riscos
  - **Linha 1:** Conexão → atraso < 5%
  - **Linha 2:** Dados extras → < 5 KB
  - **Linha 3:** Mini PC → sem travar
  - **Linha 4:** Queda de 1h → 100% salvo
  - **Faixa Base:** Limites: chuva, energia e satélite privado.
- **Mídia:** **Nova tabela editorial limpa** (versão reduzida de `tab:metricas` com ícones simples de status + faixa inferior inspirada em `fig:fofa`).
- **Sincronia com a Fala:** Apresentar benefícios (LGPD + imunidade quântica), limitações honestas (chaves, chuva, empresa privada) e as 4 métricas práticas para validar um posto piloto (incluindo mini PC de ~R$ 1.500 e desligamento da antena por 1 hora).

---

### Slide 8 · Foto Hero com Cartão Flutuante (`08:30 – 09:15`)
- **Layout:** Foto em tela cheia (ou 100% lateral com gradiente suave `#1F3A5F` à esquerda) servindo de fundo para um cartão branco flutuante com 3 linhas diretas de conclusão.
- **Título de Ação:** *A tecnologia já existe hoje; o próximo passo é um piloto com o SUS*
- **Texto Visível no Slide (~33 palavras):**
  - **Título:** A tecnologia já existe hoje; o próximo passo é um piloto com o SUS
  - **Cartão Flutuante:**
    - Pronto hoje: NIST 2024 + LEO + Mini PC
    - Desafio: energia solar e capacitação
    - Futuro: piloto SUS + UFRPE
- **Mídia:** `papers/04-internet-futuro/figures/chuva_borda.jpg`
- **Sincronia com a Fala:** Fechar a viabilidade técnica ("não precisamos esperar 2035"), apontar os desafios reais de gestão pública e encerrar com a mensagem humana: PQC para salvar vidas e proteger a dignidade no interior.

---

### Slide 9 · Encerramento Minimalista em Duas Colunas (`09:15 – 09:40`)
- **Layout:** Fundo limpo `#FFFFFF` com barra lateral esquerda em `#1F3A5F`. Coluna esquerda com lista enxuta de fontes-chave; coluna direita com agradecimento em destaque e e-mail.
- **Título de Ação:** *Segurança pós-quântica para proteger a dignidade de quem mora longe*
- **Texto Visível no Slide (~39 palavras):**
  - **Título:** Segurança pós-quântica para proteger a dignidade de quem mora longe
  - **Coluna Esquerda (Fontes):**
    - NIST FIPS 203 & 204 (2024)
    - Bernstein & Lange (Nature, 2017)
    - Del Portillo (2019) · Shi et al. (2016)
    - NIST Zero Trust (2020) · Lei Telessaúde & LGPD
  - **Coluna Direita (Contato):**
    - Obrigado!
    - `caua.lira@ufrpe.br`
- **Mídia:** Tipografia limpa e espaçada (sem imagem competindo com as referências).
- **Sincronia com a Fala:** Agradecer à Profa. Jeisa e aos colegas pelos seminários que enriqueceram a arquitetura, abrindo para dúvidas.

---

## Etapa 4: Checklist Anti-Slop & Plano de Mídia

### Verificação de Qualidade
- [x] **Títulos de ação:** Todos os 9 slides têm títulos que comunicam uma ideia completa.
- [x] **Limite de palavras:** Todos os slides ficam entre **33 e 39 palavras visíveis** (teto rigoroso de 40 palavras).
- [x] **Zero bullet points longos:** Substituídos por split de imagens, número herói, grade 2x2, diagrama em camadas, fluxo numerado 1–6, tabela limpa e cartão flutuante.
- [x] **Variedade de layout:** Nenhum par consecutivo repete composição.

### Inventário de Arquivos de `papers/04-internet-futuro/figures/`
- **Usadas diretamente nos slides:**
  - `brasao_ufrpe.png` → Slide 1
  - `posto_sertao.jpg` → Slide 2
  - `colha_agora.jpg` → Slide 2
  - `ibm_quantum.jpg` → Slide 3
  - `starlink_antena.jpg` → Slide 5 (apoio)
  - `seu_jose_ecg.jpg` → Slide 6
  - `chuva_borda.jpg` → Slide 8
- **Não usadas no deck principal (reserva visual):**
  - `starlink_satelites.jpg` (pode ficar como alternativa para o Slide 4/5 caso prefira foto no lugar de ícone)
  - `ribeirinha_prenatal.jpg` (cenário 2 citado brevemente na fala, não precisa sobrecarregar os slides)
- **Novos gráficos/infográficos a produzir para os slides:**
  1. **Slide 3:** Gráfico de contraste de barras `32 B` vs `1.184 B` / `3.309 B`.
  2. **Slide 4:** Infográfico Grade 2x2 das 4 tecnologias parceiras.
  3. **Slide 5:** Diagrama horizontal de 4 camadas + barra transversal Zero Trust.
  4. **Slide 6:** Fluxo vertical numerado (passos 1 a 6) do ECG do Seu José.
  5. **Slide 7:** Tabela limpa de 4 métricas + faixa de limites.
