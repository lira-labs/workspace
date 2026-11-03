# ComicForge Studio — Diretrizes de Engenharia Editorial e Geração Visual de HQs

> Documento canônico de arquitetura e referência técnica para conversão de e-books e conteúdos pedagógicos em Histórias em Quadrinhos (HQs) com consistência de personagens, controle de composição e diagramação editorial vetorial.

---

## 1. Repositórios de Referência (Camada Editorial & Diagramação)

| Repositório | Linguagem / Licença | Responsabilidade de Referência |
| :--- | :--- | :--- |
| **[adachi0130/comic-pipeline](https://github.com/adachi0130/comic-pipeline)** | Python · GPL-3.0 | Pipeline ponta a ponta: roteiro → divisão automática em páginas e quadros → prompts por quadro → integração ComfyUI → referências/versionamento → exportação PDF/CBZ. |
| **[new-sankaku/manga-editor-desu](https://github.com/new-sankaku/manga-editor-desu)** | JavaScript · GPL-3.0 | Camada de diagramação: 69 modelos de organização de quadros, 48 estilos de balões, camadas, retículas, tipografia de quadrinhos e exportação em alta resolução (PNG/SVG). |
| **[McMuff86/ComicMaster](https://github.com/McMuff86/ComicMaster)** | Python · MIT | Automação com Python + ComfyUI + IP-Adapter para consistência de personagens, 11 tipos de balões e diagramação automática (PDF/PNG/CBZ). |
| **[cainezen/panel-foundry](https://github.com/cainezen/panel-foundry)** | Web App · Open Source | Interface de criação de capas e páginas, quadros redimensionáveis/posicionáveis, balões de fala/pensamento e exportação PDF. |
| **[gramener/comicgen](https://github.com/gramener/comicgen)** | JavaScript · MIT | Personagens vetoriais em SVG parametrizáveis (poses, expressões e ângulos consistentes sem redesenho aleatório). |
| **[Stanestane/gutterline](https://github.com/Stanestane/gutterline)** | HTML5 · MIT | Composição geométrica de páginas: grades de quadrinhos, divisão diagonal, redimensionamento, sobreposição de quadros e formatos A4/mangá/comic book. |

---

## 2. Repositórios de Referência (Motor de Ilustração & Consistência Visual)

| Prioridade | Repositório / Ferramenta | Licença | Papel no Pipeline Visual |
| :---: | :--- | :---: | :--- |
| **1** | **[comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)** | GPL-3.0 | Motor de orquestração de workflows visuais via API (local ou remoto/cloud GPU, sem exigir GPU pesada na máquina local de 16 GB RAM / Ryzen 7 5700). |
| **2** | **[cubiq/ComfyUI_IPAdapter_plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus)** | GPL-3.0 | Preservação de identidade visual do personagem e transferência de estilo artístico a partir de uma *Character Sheet* aprovada. |
| **3** | **[Fannovel16/comfyui_controlnet_aux](https://github.com/Fannovel16/comfyui_controlnet_aux)** | Apache-2.0 | Controle de pose corporal (OpenPose), pontos faciais, profundidade (Depth), contornos (Canny/Scribble) e lineart de mangá/HQ. |
| **4** | **[HVision-NKU/StoryDiffusion](https://github.com/HVision-NKU/StoryDiffusion)** | MIT | *Consistent Self-Attention* para geração de sequências de quadros mantendo roupas, traços e identidade entre múltiplos quadros consecutivos. |
| **5** | **[HarisUmer/artikon-comic-genai](https://github.com/HarisUmer/artikon-comic-genai)** | Open Source | Arquitetura combinando Stable Diffusion + ControlNet + IP-Adapter + LangGraph + banco de personagens com verificação de consistência. |

---

## 3. Regras de Ouro da Produção de HQ (Padrão Editorial)

1. **Separação Absoluta entre Ilustração e Texto (Zero Texto na Imagem de IA)**:
   - As ilustrações de cada quadro devem ser geradas **100% limpas** (sem balões desenhados pela IA, sem palavras, sem letras deformadas).
   - O *lettering* (recordatórios de narração, balões de fala, pensamento, grito/glitch e onomatopeias) é renderizado separadamente em **SVG/HTML vetorial** sobre os quadros, com rabichos (`pointer tails`) apontando exatamente para o personagem que fala.
2. **Bíblia Visual e *Character Sheet* Antes das Páginas**:
   - Todo personagem recorrente possui ficha visual fixa (aparência física, vestimenta, paleta de cores, acessórios e folha de referência em múltiplos ângulos/expressões) que é injetada como referência em todas as cenas.
3. **Proibição de " Página de Slide com 1 Imagem"**:
   - Uma página de HQ real possui de **4 a 6 quadros ilustrados individualmente**, variando enquadramentos (*plano geral/establishing shot*, *plano médio*, *close-up dramático de reação*, *over-the-shoulder*, *panorâmico widescreen*) e geometria de sarjetas (*gutters* tradicionais, divisões diagonais e *panel-breaking*).
4. **Controle de Qualidade Visual por Quadro**:
   - Cada quadro mantém histórico de prompt e versão, permitindo regenerar ou ajustar um único quadro ou balão sem afetar o restante da página.
