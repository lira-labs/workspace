# PROJECT BRIEF · Compasso Cognitivo

- **Repositório de Código:** `https://github.com/grupo-zeta/prob-tech-fit-cp01` (branch ativa mais recente: `compasso-aprovacao`, atualizações de Igor até 16/11/2026; fontes Python em `feat/compasso-estudo-ia`).
- **Repositório Overleaf / LaTeX:** `https://www.overleaf.com/project/6a922427f1ca2007335f685f` (template atual `llncs.cls` + `splncs04.bst`, commit `1c26c85`).
- **Autores:** José Albérico Rocha da Silva, Igor Alexandre da Silva Santos, Luis Eduardo Tavares Gomes da Silva, Cauã da Cunha Lira (UFRPE — Tecnologias na Educação 2026.2, Prof. Lucas Silva).
- **Foco Editorial:** Educação + Inteligência Artificial Centrada no Humano (PT-BR para disciplina agora; versão final em EN mirando SIGCSE / EAAI / IJCAI *Human-Centered AI*).

## O que o sistema implementa de fato hoje
1. **Aplicativo Desktop Windows *Local-First*:** servidor local (`127.0.0.1:8765`, SQLite em `%LOCALAPPDATA%\Compasso`), distribuído como `Compasso.exe` + `_internal/`.
2. **Telemetria Nativa de SO (`app.py`):** `GetForegroundWindow` ($1\text{ Hz}$) + hooks Win32 `WH_KEYBOARD_LL`/`WH_MOUSE_LL` + `GetLastInputInfo` contando teclas, cliques, rolagens, distância do mouse e ociosidade **sem gravar texto digitado**.
3. **Extensão de Navegador (`extension/`):** bloqueio/permissão via *Declarative Net Request* em Chrome/Edge/Brave durante sessões ativas.
4. **Visão Computacional na Borda (`vision.js` + `app.js`):** MediaPipe Holistic local (~$110\text{ ms}$ por frame) estimando direção do olhar pelas íris (calibração rápida ou 5 pontos), pose da cabeça (`yaw`, `pitch`, `roll`), postura corporal (33 pontos), piscadas e heurística de olhar inferior / inclinação cervical (`gaze_direction === 'down'` ou `head_pitch > 15°` por $\ge 5\text{ s}$). **NÃO utiliza YOLO11n.**
5. **Copiloto Autônomo Zero-Clique (`app.js`):** motor determinístico baseado em regras/estatísticas locais que aprende a mediana dos ciclos de foco (padrão inicial ~34 min), detecta travamento (`auto.stuck`), fragmentação ($\ge 6$ trocas em 10 min), modo hobby/jogos (silenciando alertas e aplicando descanso visual 20-20-20 após 45 min) e micropausa respiratória 4-4-4.
6. **Gadget Circular Nativo WPF (`tray.ps1`):** widget circular translúcido sem bordas na área de trabalho com anel de risco, ponteiros alternáveis e sussurros no *hover*.
7. **Revisão Visual Multimodal Opcional (`context_tools.py`):** capturas GDI da janela ativa sob consentimento explícito por sessão (máx. 48/sessão, retenção 24h), enviadas ao **Ollama local** (`gemma3:4b`) ou chave OpenAI própria do usuário. *(Pendência de código: corrigir default `llama3:8b` na UI para `gemma3:4b`, pois `llama3:8b` não processa imagens.)*
