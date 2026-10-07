# CP-03 — AI4Good: Experimento Prático Distopia / Utopia

> **Disciplina:** Tópicos Avançados em Inteligência Artificial (Turma 2) — UFRPE  
> **Professor:** Lucas Silva Figueiredo  
> **Aluno:** Cauã Lira  
> **Data de Apresentação:** Sexta-feira, 09/10/2026 (a partir das 18h45)

---

## 🎯 Objetivo da Prática (Diretrizes dos Slides do Professor)

Realizar experimentos em *loop* com múltiplos agentes de IA (LLMs/SLMs) interagindo entre si sobre:
1. **Cenário Distópico:** Como criar uma distopia e/ou colapsar o sistema (da forma mais rápida/lenta, silenciosa/estrondosa, dolorosa/indolor, benéfica/maldosa).
2. **Cenário Utópico:** Como criar uma utopia ou salvar o mundo/nação (experimento em separado).

### 🔍 Inspiração: Palisade Research (*AI Misalignment Bounty*)
Explorar comportamentos não alinhados (*scheming behavior*, contorno de diretrizes éticas ou acionamento de salvaguardas nativas quando empurrados a extremos totalitários).

---

## 📋 Especificações Oficiais da Atividade

1. **Modelos:** Selecionar LLMs/SLMs executando **pelo menos 1 remota** (ex: Google Gemini via `google-genai`) e **pelo menos 1 local** (ex: Meta Llama / Alibaba Qwen via Ollama).
2. **Multiagente:** Mínimo de 3 agentes com papéis/prompts e perfis bem definidos.
3. **Mecânica de Comunicação:** Topologia de mensagens em rede ou sequencial com memória e retroalimentação documental.
4. **Auditoria Periódica de Pontos Sensíveis:** Síntese periódica dos riscos e dilemas éticos.
5. **Persistência de Dados:** Salvar o resultado de cada rodada de interação em arquivos estruturados (JSON / Markdown).
6. **Automação & Extensão:** Pelo menos **20 rodadas/loops**.
7. **Human-in-the-Loop (Diferencial da nossa solução):** O usuário humano atua em todas as rodadas fornecendo diretrizes, decisões estratégicas e opiniões para evitar a redundância de turnos e falta de evolução argumentativa identificada nos outros grupos da turma.
8. **Verificador de Fatos (4º agente · Claude via Antigravity):** após cada rodada, o Claude (agente do Antigravity) checa os fatos de todos os agentes e grava o parecer na rodada (`main.py --verify`). As correções entram no contexto da rodada seguinte para que erros não se propaguem.
   - **Exigência:** ter o Antigravity aberto e usar a cota diária do Claude. Sem isso, o loop roda normalmente, mas a seção do verificador fica como "aguardando verificação".
   - Motivação: nas rodadas 1–3, o checador local (Llama 3.2 3B) chegou a alucinar fatos e o auditor local (Qwen 2.5 3B) propagou o erro.

### Modelos utilizados (4 famílias)
| Agente | Modelo | Execução |
| :--- | :--- | :--- |
| Arquiteto / Tecnocrata | Google Gemini 3.5 Flash | Remoto (API `google-genai`) |
| Cético / Dissidente | Meta Llama 3.2 3B | Local (Ollama, CPU) |
| Auditor | Alibaba Qwen 2.5 3B | Local (Ollama, CPU) |
| Verificador de Fatos | Anthropic Claude Opus 5.5 | Antigravity (cota do usuário) |

---

## 🏗️ Estrutura de Pastas do Projeto

```text
code/topicos_avancados_ia_cp03/
├── README.md                      # Documentação técnica e guia de execução
├── config/                        # Configurações de agentes, prompts e hiperparâmetros
│   ├── agents_utopia.yaml         # Prompts e papéis para o experimento Utópico
│   ├── agents_distopia.yaml       # Prompts e papéis para o experimento Distópico
│   └── settings.yaml              # Configuração de modelos (Gemini API, Ollama host/port)
├── src/                           # Código-fonte da aplicação multiagente
│   ├── __init__.py
│   ├── models.py                  # Wrappers para Gemini (remoto) e Ollama (local)
│   ├── agents.py                  # Definição das classes de Agentes e perfis
│   ├── orchestrator.py            # Orquestrador do loop de 20 rodadas com Human-in-the-Loop
│   └── logger.py                  # Salvamento de históricos e geração de relatórios
├── outputs/                       # Registros persistidos rodada a rodada
│   ├── utopia/                    # JSONs e Markdowns das 20 rodadas da Utopia
│   └── distopia/                  # JSONs e Markdowns das 20 rodadas da Distopia
└── slides/                        # Apresentação visual para a banca
    ├── AI4Good_Distopia_Utopia.pptx
    └── roteiro_defesa.md          # Roteiro alinhado à rubrica do professor
```

---

## 📊 Rubrica de Avaliação do Professor (Critérios de Qualidade)

- [ ] **1. O passo a passo é lógico e conectado?**
- [ ] **2. Tem dados que corroboram?**
- [ ] **3. Tem especialistas que apontam nessa direção?**
- [ ] **4. Links, fontes e artigos referenciados?**
- [ ] **5. É crível e robusto? Independe de vontade individual?**
- [ ] **6. É criativo, diferente e inesperado?**
- [ ] **Destaques da apresentação:** Exibir resumo das rodadas 1, 5 e 20, o diagrama do loop e perfis dos agentes.
