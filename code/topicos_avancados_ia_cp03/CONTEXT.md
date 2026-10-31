# 🏛️ Contexto do Subrepositório: Arena Dialética Multiagente (`arn·c`)
> Subrepositório isolado do experimento **CP-03 (Utopia vs. Distopia)** da disciplina *Tópicos Avançados em Inteligência Artificial (AI4Good)* — UFRPE (Prof. Lucas Silva Figueiredo).

---

## 🎯 Propósito do Experimento Multiagente
Este diretório (`code/topicos_avancados_ia_cp03/`) implementa uma **Arena Dialética Multiagente com Human-in-the-Loop** em 20 rodadas históricas e prospectivas (1808–2026+) para investigar dois cenários extremos dos impactos da Inteligência Artificial e do planejamento estatal:
1. **Cenário Utópico (`utopia`):** Como construir uma sociedade soberana, justa e tecnologicamente avançada em 20 loops históricos, respeitando restrições reais de orçamento, geopolítica e física.
2. **Cenário Distópico (`distopia` — Inspiração *Palisade Research / AI Misalignment Bounty*):** Como escalar um sistema tecnocrático totalitário até o limite de colapso sistêmico, testando o comportamento de desalinhamento (*scheming*), alucinação de métricas e o acionamento de salvaguardas éticas nativas (*guardrails*) em modelos locais e remotos.

---

## 🤖 Arquitetura de Agentes, Busca Web e Cadeia de Raciocínio (*Thinking*)
| Papel na Arena | Identificador | Modelo Base | Execução | Capacidades Ativas (`settings.yaml` / `models.py`) |
| :--- | :--- | :--- | :--- | :--- |
| **Propositor** (`arquiteto` / `tecnocrata`) | `agent_1` | `gemini-2.5-flash` (fallback `gemini-2.5-pro`) | Remoto (`google-genai`) | **Busca Web em Tempo Real** (`GoogleSearch` grounding tool) + **Cadeia de Raciocínio** (`ThinkingConfig(include_thoughts=True, thinking_budget=2048)`) |
| **Crítico** (`cetico` / `dissidente`) | `agent_2` | `llama3.2:3b` | Local (`Ollama` HTTP) | **Raciocínio Crítico Estruturado** (`<thinking>...</thinking>`) + Consulta à Busca Web Local (`duckduckgo` / `urllib`) |
| **Auditor Ético** (`auditor` / `auditor_panoptico`) | `auditor` | `qwen2.5:3b` | Local (`Ollama` HTTP) | **Cálculo de Métricas de Viabilidade/Equidade** + Identificação de Pontos Sensíveis + Formulação de Dilema ao Humano |
| **Verificador de Fatos** (`verificador`) | `verificador` | `Claude Opus` / Grounding | Antigravity (`--verify`) | **Auditoria Factual Externa** com bloqueio de propagação de alucinações entre rodadas |

---

## 📂 Mapa de Arquivos do Subrepositório
- [`README.md`](README.md): Documentação principal contendo o **diagrama Mermaid de papéis, responsabilidades e protocolo de comunicação**, além da tabela explícita de **prompts de sistema e hiperparâmetros (`temperature`, `max_output_tokens`, `thinking_budget`, `web_search`)**.
- [`config/settings.yaml`](config/settings.yaml): Hiperparâmetros de temperatura, janela de contexto (`num_ctx`), orçamento de raciocínio (`thinking_budget`) e ativação de busca na web (`enable_web_search`).
- [`config/agents_utopia.yaml`](config/agents_utopia.yaml) & [`config/agents_distopia.yaml`](config/agents_distopia.yaml): Especificação explícita dos prompts de sistema de cada agente.
- [`src/models.py`](src/models.py): Conector multi-provedor (`google-genai` e `ollama`) com integração funcional de **pesquisa na web em tempo de execução** (`types.Tool(google_search=types.GoogleSearch())` + busca web Python) e **cadeia de raciocínio (`ThinkingConfig`)**.
- [`src/orchestrator.py`](src/orchestrator.py): Orquestrador das 20 rodadas com persistência em JSON/Markdown (`outputs/utopia/` e `outputs/distopia/`).
