# Protocolo Automático de Continuidade e Sincronização (Auto-Handoff)

Este projeto é desenvolvido alternando entre dois ambientes físicos (Notebook e Desktop), utilizando o GitHub (`lira-labs/workspace`) como repositório central.

## Regras Obrigatórias para o Antigravity

1. **Pre-flight Automático (Abertura de Sessão)**:
   - Na primeira interação de qualquer sessão nesta pasta, execute silenciosamente a sincronização com o GitHub (`git pull origin <branch>` ou `.\core\tools\handoff.ps1 -Pull`).
   - Leia o arquivo `HANDOFF.md` na raiz do workspace.
   - Informe ao usuário o estado recebido da outra máquina (última atualização, branch e próximos passos recomendados).

2. **Post-flight Automático (Fechamento / Conclusão de Tarefa)**:
   - Ao concluir uma solicitação, tarefa de desenvolvimento, marco de pesquisa ou quando o usuário sinalizar encerramento ("concluí", "vou pro notebook", "até mais", etc.):
     - Atualize os campos de metadados em `HANDOFF.md` com a data/hora local atual e branch ativo.
     - Documente as alterações e itens concluídos na seção correspondente de `HANDOFF.md`.
     - Liste os próximos passos práticos para quando a sessão for retomada na outra máquina.
     - Execute o commit das alterações com mensagem padronizada (ex: `feat: ...`, `fix: ...`, `docs: handoff sync`).
     - Realize o `git push` para o GitHub (`.\core\tools\handoff.ps1 -Push -Message "..."`).
