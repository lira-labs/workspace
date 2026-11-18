---
name: venue-adaptation
description: Adapta um manuscrito-base independente de conferência (PT-BR ou EN) às exigências oficiais de SIGCSE, EAAI/AAAI, IJCAI ou SBC sem distorcer evidências científicas.
---

# Venue Adaptation & Submission Formatting

Consulte [references/publication-venues.md](./references/publication-venues.md) antes de adaptar o manuscrito para um veículo específico.

## Princípio Central
Mantenha o **manuscrito-base independente de conferência** (estrutura canônica + evidências + matriz de literatura). Só aplique cortes de página, troca de `.cls` e ajustes de enquadramento após confirmar o veículo oficial.

## Protocolo de Adaptação
1. **Verificar CFP Oficial Vigente:** Confirme prazos, limite de páginas, política de anonimato (*double-blind* vs *single-blind*), formato oficial (ACM `acmart`, AAAI `aaai27.sty`, IJCAI `ijcai.sty`, Springer `llncs.cls`, SBC `sbc-template.sty`) e trilha exata.
2. **Ajustar Enquadramento Sem Mudar Fatos:**
   - **SIGCSE:** destaque contexto pedagógico de Computação, desenho da avaliação com estudantes e replicabilidade educacional.
   - **EAAI / AAAI:** destaque arquitetura Human-AI, raciocínio contextual e impacto em aprendizagem.
   - **IJCAI (*Human-Centered AI* / *AI for Social Good*):** destaque agência humana, privacidade na borda, mitigação de vieses/falsos positivos e avaliação empírica sólida.
3. **Auditar Anonimato e Limites:** Se a submissão for *double-blind*, remova nomes, afiliação UFRPE, e-mails e links identificáveis do repositório/Overleaf antes de exportar o PDF de submissão.
