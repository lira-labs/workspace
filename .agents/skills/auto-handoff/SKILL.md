---
name: auto-handoff
description: Gerencia e automatiza a passagem de bastão (handoff) entre máquinas (Notebook e PC) sincronizando HANDOFF.md e Git.
---

# Auto-Handoff Workflow

Esta habilidade sincroniza automaticamente o estado de trabalho entre máquinas através do repositório GitHub e do arquivo canônico `HANDOFF.md`.

## Modos de Operação

### 1. Início de Sessão (Pull & Context Sync)
Executado no início de conversas:
1. Executar `powershell -ExecutionPolicy Bypass -File .\core\tools\handoff.ps1 -Pull` ou `git pull origin <branch>`.
2. Ler `HANDOFF.md`.
3. Reportar ao usuário o resumo da última sessão e sugerir o próximo passo imediato.

### 2. Fechamento de Sessão (Save & Push)
Executado após concluir alterações ou a pedido do usuário:
1. Atualizar em `HANDOFF.md` os metadados (`Última Atualização`, `Branch Ativo`), o que foi concluído e os próximos passos.
2. Executar `powershell -ExecutionPolicy Bypass -File .\core\tools\handoff.ps1 -Push -Message "<mensagem>"`.
3. Notificar o usuário que a outra máquina já pode puxar as atualizações.
