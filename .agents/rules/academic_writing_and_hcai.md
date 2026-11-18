---
name: academic-writing-and-hcai
trigger: model_decision
description: Diretrizes editoriais de escrita científica anti-AI-slop, foco em Human-Centered AI in Education e proteção de templates LaTeX/Overleaf.
---

# Escrita Científica, Human-Centered AI & Proteção Editorial

1. **Identidade Editorial (Human-Centered AI in Education):**
   - Apresente a IA e a telemetria como meios para ampliar autonomia, consciência metacognitiva, tomada de decisão e bem-estar do aprendiz — nunca como vigilância punitiva ou "solução de IA procurando um problema".
   - Alvos editoriais de referência: **SIGCSE** (Educação em Computação), **EAAI/AAAI** (Avanços Educacionais em IA) e **IJCAI** (IA & *Human-Centered AI* / *AI for Social Good*). Adapte sempre às regras oficiais de cada chamada sem presumir requisitos idênticos.
2. **Escrita Científica Sem AI Slop:**
   - **Proibido:** introduções genéricas ("AI is revolutionizing..."), linguagem promocional ("innovative", "groundbreaking", "revolutionary"), conclusões repetitivas e parágrafos inflados.
   - **Obrigatório:** cada parágrafo deve cumprir uma função argumentativa clara, ancorada em **mecanismo, hipótese ou evidência verificável**.
   - Trabalhos Relacionados devem ser organizados por **eixos temáticos comparativos**, nunca como lista isolada de resumos.
3. **Ordem de Produção Científica:**
   - Nunca comece redigindo a Introdução antes de consolidar `PROJECT_BRIEF.md`, `CLAIMS_AND_EVIDENCE.md`, matriz de literatura e metodologia/RQs.
   - Mantenha um manuscrito-base conceitualmente neutro quanto à conferência e faça a adaptação de template/tamanho apenas na etapa de `venue-adaptation`.
4. **Segurança LaTeX & Overleaf:**
   - Nunca substitua ou altere silenciosamente classes/estilos oficiais (`.cls`, `.bst`) sem autorização explícita.
   - Nunca armazene tokens do Overleaf (`.git/config`, `.md`, `.bib`, `.tex`).
   - Sempre execute o Quality Gate (`validate_latex_project.py` + compilação/auditoria) antes de concluir qualquer entrega de manuscrito.
