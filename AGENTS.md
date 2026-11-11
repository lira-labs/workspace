# Workspace Root - Normas do Agente
> Ponto de entrada canônico do Workspace. Lido obrigatoriamente antes de qualquer tarefa por qualquer Harness (Antigravity, OpenCode, Claude Code).

<!-- norms:start -->
- **SISTEMA DE ARQUIVOS É A FONTE DA VERDADE**: Nada vive apenas na memória do chat ou em configs voláteis. Se existe e importa, é um arquivo versionado.
- **STORAGE AGNÓSTICO DE HARNESS**: O workspace é o dono do seu estado, nunca o harness. Antigravity (principal) e OpenCode (backup) operam sobre os mesmos arquivos.
- **PROTOCOLO AUTOMÁTICO DE CONTINUIDADE (AUTO-HANDOFF)**:
  - *No Início de Sessão*: O agente DEVE executar `git pull` e ler `HANDOFF.md` imediatamente para carregar o contexto da última máquina e reportar o status e próximos passos ao usuário.
  - *Na Conclusão de Tarefa / Fim de Sessão*: O agente DEVE atualizar `HANDOFF.md` com os metadados (data/hora), progresso alcançado e pendências, e realizar o commit e push para o GitHub automaticamente.
- **SEGREDOS FORA DO GIT**: Senhas, tokens, chaves de API e credenciais ficam em `.env` ou `segredos.env` (sempre no `.gitignore`).
- **NÃO ASSUMA, PERGUNTE**: Em caso de ambiguidade sobre o desenho experimental, requisitos ou estrutura do artigo, entreviste o usuário.
- **EDITAR > CRIAR**: Prefira refatorar, modularizar e aprimorar arquivos existentes a criar novos arquivos dispersos.
- **DIVISÃO RÍGIDA DE DOMÍNIOS**:
  - `code/`: Todo o desenvolvimento de modelos, scripts de treino, pipelines de dados e visualizações de IA.
  - `papers/`: Toda a produção de artigos científicos, relatórios técnicos, seções `.tex`, figuras e referências `.bib`.
  - `core/`: Utilitários, scripts de automação, documentações de harness e ferramentas de suporte.
- **GIT FLOW OBRIGATÓRIO & BLINDAGEM DE PRODUÇÃO**:
  - `main`: Versão oficial estável de produção (o que o professor, a banca e o público veem em `grafoparadaweb.vercel.app`). NUNCA editar diretamente nem commitar código experimental sem teste prévio.
  - `feature/grafoparada-*` ou `develop`: Laboratório de desenvolvimento, iteração e testes. Descontinuado o uso de branches legadas de outras matérias (como `feature/if-2va-pqc-telessaude`).
  - *Gatekeeper Pré-Deploy Obrigatório*: Antes de qualquer merge ou promoção para a `main`, executar obrigatoriamente `uv run python code/grafoparada_tec/pre_flight_check.py` (valida sintaxe JS via Node VM, integridade física do GTFS e 20/20 na suíte de testes). Se houver qualquer falha, o merge para a `main` é terminantemente bloqueado.
- **ARMAZENAMENTO PESADO NO GOOGLE DRIVE (5 TB)**: Datasets volumosos, vídeos, checkpoints e pesos de modelos de IA (`.pt`, `.ckpt`, `.safetensors`, `.onnx`) NUNCA são commitados no Git nem consom o SSD local. Ficam sempre em `G:\Meu Drive\IA_Projetos\` (`datasets/`, `checkpoints/`, `outputs/`), compartilhados instantaneamente entre o Notebook e o Desktop.
- **LIMPEZA E HIGIENE**: Arquivos de build (LaTeX `.aux`, `.log`, caches Python `__pycache__`) nunca são commitados.
- **DIRETRIZ DE SEQUENTIAL ART & HQ/EBOOK (ANTI-AI-SLOP)**:
  - *As 3 Camadas Indissociáveis*:
    1. **Narrativa**: O que está acontecendo? (enredo, personagens, conflito pedagógico e desfecho).
    2. **Sequência**: Por que este quadro vem depois do anterior? (relação causa-efeito, ritmo e a sarjeta/calha como conexão mental do leitor).
    3. **Linguagem Visual**: Como a imagem, enquadramento cinematográfico, balão e sarjeta guiam o leitor?
  - *A Pergunta Mestre do Pipeline*: O agente NUNCA começa perguntando 'Que imagem vou gerar?', mas sim: **'Que parte da história este quadro precisa contar, e qual é a melhor forma visual de mostrar isso?'**
  - *Gramática Autêntica de HQ*: Sarjetas nítidas, Recordatórios canônicos (tempo/espaço/narrador), Balões semânticos (fala comum, pensamento-nuvem com esferas, glitch/elétrico para robô sem filtro, socrático acolhedor) e Onomatopeias integradas (SFX).
  - *Simbiose HQ + eBook*: A ação sequencial dos quadrinhos integra-se organicamente aos encartes didáticos (Caderno de Campo de Cauã, Relatório de Auditoria Pedagógica da UFRPE, Terminal CRT de Código e Manual de Prompts Copiáveis).
<!-- norms:end -->

---

## 🗺️ Mapa de Roteamento de Contexto
Antes de modificar qualquer arquivo, consulte o `CONTEXT.md` do diretório correspondente:
- Passagem de Bastão / Estado da Sessão: [`HANDOFF.md`](HANDOFF.md)
- Raiz: [`CONTEXT.md`](CONTEXT.md)
- Códigos e Modelos: [`code/CONTEXT.md`](code/CONTEXT.md)
- Artigo e Pesquisa: [`papers/CONTEXT.md`](papers/CONTEXT.md)
- Ferramentas e Harness: [`core/CONTEXT.md`](core/CONTEXT.md)
