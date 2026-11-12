# 🎨 Sistema de Trabalho — Agente Especialista em Apresentações de Alta Qualidade
> Padrão Oficial Canva Pro, Figma e Apple Keynote para Seminários, Artigos e Defesas Acadêmicas.
> Referência Canônica de Design do Workspace · Anti-AI Slop Protocol.

---

## 🚫 Princípio Central: Zero AI Slop

Nunca produzir apresentações que pareçam conteúdo gerado automaticamente.

### O que é terminantemente proibido:
- ❌ Slides cheios de texto corrido ou parágrafos colados em caixas de texto;
- ❌ Listas infinitas de tópicos (bullet points entediantes dos anos 2000);
- ❌ O mesmo layout ou grid repetido mecanicamente em todos os slides;
- ❌ Imagens genéricas corporativas ou ilustrações sem relação factual com o assunto;
- ❌ Excesso de ícones decorativos sem propósito semântico;
- ❌ Imagens artificiais ou com defeitos visuais de geração;
- ❌ Gráficos que não respondem diretamente a uma pergunta do projeto;
- ❌ Caixas competindo simultaneamente pela atenção do espectador;
- ❌ Frases de efeito vazias sem evidência empírica;
- ❌ Títulos puramente descritivos (ex: "Metodologia", "Resultados") em vez de **Títulos de Ação** que já comunicam a conclusão.

> **Regra de Ouro:** Cada slide deve ser o resultado de uma decisão editorial e visual consciente.

---

## 🔄 Fluxo Obrigatório de Trabalho (8 Etapas)

```
[Etapa 1: Objetivo & Frase Central]
                │
                ▼
[Etapa 2: Pesquisa & Confiabilidade (A1/Fontes Reais)]
                │
                ▼
[Etapa 3: Arquitetura Narrativa & Funções de Slide]
                │
                ▼
[Etapa 4: Planejamento Visual Slide a Slide (Ponto Focal)]
                │
                ▼
[Etapa 5: Curadoria de Mídia Factual & Telemetria]
                │
                ▼
[Etapa 6: Design (Hierarquia, Bento-Grid, Números Heróis)]
                │
                ▼
[Etapa 7: Execução no Canva Pro / HTML5 Widescreen]
                │
                ▼
[Etapa 8: Revisão Impiedosa & Teste Anti-AI Slop]
```

### 1. Entender o Objetivo
- **Público:** Professor da disciplina (Prof. Lucas Silva Figueiredo), pesquisadores convidados e colegas de turma.
- **Objetivo:** Demonstrar o ineditismo científico da modelagem de grafos espaço-temporais para o problema de passageiros abandonados na parada (*Passenger Reneging* & *Denied Boarding*).
- **Tempo:** 4 a 5 minutos cronometrados de fala.
- **Frase Central Única:** *"O transporte público não quebra quando o ônibus quebra; ele quebra quando a rede cega força o passageiro a desistir na parada."*

### 2. Pesquisa e Confiabilidade
- Dados reais do GTFS CTM Grande Recife (393 linhas, 2,8 MB de malha).
- Telemetria de campo da Linha 199 (Camela / TI Cabo) na Rodovia PE-60.
- Referencial teórico internacional Qualis A1:
  * Kim et al. (2026) - *Passenger Reneging under Service Uncertainty*;
  * Yap & Cats (2021) - *Valuation of Denied Boarding in Crowded Public Transport Systems* (penalidade psicológica 68% maior após embarque negado);
  * Tan & Ramli (2024) - *Inferring unable-to-board commuters for overcrowded buses using smart card data*;
  * Drabicki et al. (2023) - *Should I stay or should I board?*

### 3. Criar a Narrativa (Funções dos Slides)
1. **Slide 1 · Abertura:** O drama humano invisível na PE-60 (o passageiro não computado).
2. **Slide 2 · Problema:** A cegueira da matriz O-D tradicional (falha ao registrar a demanda latente e a queima de paradas).
3. **Slide 3 · Comparação de Paradigmas:** OLS Estática (120 features colineares) vs GNN Espaço-Temporal (topologia viária real).
4. **Slide 4 · Arquitetura:** ST-GCN Híbrida com Trava Física Laplaciana (evita viés confirmatório).
5. **Slide 5 · Demonstração & Resultados:** Ganhos reais de pontualidade, redução de abandono e despacho responsivo.

### 4. Planejamento Visual Slide a Slide
- **Slide 1:** Ponto focal é o contraste dramático (42 km de rodovia vs 0 registro no sistema).
- **Slide 2:** Ponto focal é a métrica psicológica (Yap & Cats: penalidade de 1,68x) e o conceito de *Passenger Reneging*.
- **Slide 3:** Ponto focal é a tabela visual de contraste metodológico (OLS vs GNN).
- **Slide 4:** Ponto focal é o diagrama da convolução espaço-temporal e a trava híbrida.
- **Slide 5:** Ponto focal são os display metrics gigantes (números heróis: 0,77 ms de inferência, -31% de abandono).

### 5. Curadoria de Mídia
- Mapas com coordenadas reais da Linha 199 e pontos do GTFS Oficial do Consórcio Recife / CTM.
- Zero fotos de banco de imagem clichê ("ônibus em miniatura com pessoas sorrindo").

### 6. Design (Canva Pro / Apple Keynote Standards)
- Proporção widescreen 16:9 obrigatória.
- Cartões Bento-Grid flutuantes com cantos arredondados (20px a 26px).
- Display metrics em 52px a 64px bold com tags em formato de pílula.
- Tipografia moderna (Plus Jakarta Sans / Outfit e JetBrains Mono).
- Modo Escuro (Neon Cyber) e Modo Claro (Minimal Tech) alternáveis em 1 tecla (`T`).

### 7. Formato Obrigatório de Entrega: SEMPRE PPTX (.pptx)
- **REGRA INEGOCIÁVEL:** Sempre que o usuário pedir slides, a entrega final DEVE ser o arquivo compilado em **PowerPoint (`.pptx`)**.
- O agente compila o arquivo `.pptx` diretamente via script Python (`python-pptx`) em proporção Widescreen 16:9, garantindo diagramação matemática precisa, números heróis gigantes e zero sobreposição.
- Salvo na raiz web (`code/grafoparada_web/`), na pasta `va2/` e espelhado em `G:\Meu Drive\IA_Projetos\`.
- NUNCA devolver apenas em HTML quando forem pedidos slides.

### 8. Revisão Visual & Teste Anti-AI Slop
- **A pergunta de controle:** *"Este slide parece que um humano especialista tomou decisões conscientes de conteúdo e design?"*
- Verificar:
  * Títulos comunicam conclusões (Action Titles)?
  * Há espaço em branco generoso?
  * Cada elemento tem uma razão clara de existir?

---

## 🏆 Regra Final
**CLAREZA > NARRATIVA > EVIDÊNCIA > HIERARQUIA VISUAL > DECORAÇÃO.**
