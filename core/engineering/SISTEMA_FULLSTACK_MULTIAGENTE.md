# 🏗️ Sistema de Desenvolvimento Multiagente — Full Stack de Alta Qualidade
> Referência Canônica de Engenharia de Software do Workspace.
> Protocolo Obrigatório para Orquestração, Contratos e Quality Gate.

---

## 🎯 Objetivo de Engenharia

Entregar aplicações:
1. **Visualmente profissionais:** Com hierarquia visual clara, responsividade real e sem vícios de IA.
2. **Funcionalmente corretas:** Validando entradas, saídas e casos extremos.
3. **Arquiteturalmente coerentes:** Sem criar arquiteturas concorrentes no mesmo projeto.
4. **Integradas de ponta a ponta:** Frontend consome exatamente os tipos e respostas reais do Backend.
5. **Testáveis & Testadas:** Testes de unidade, integração e gatekeepers automatizados.
6. **Livres de AI Slop:** Decisões conscientes de UI e engenharia, nunca templates decorativos vazios.

---

## 🚫 Princípio Fundamental: Proibido Codificar Sem Entender

```
[1. Entender o Problema]
            │
            ▼
[2. Inspecionar o Projeto & Tecnologias]
            │
            ▼
[3. Consultar/Definir Contratos em /contracts]
            │
            ▼
[4. Planejar a Alteração com Papéis Definidos]
            │
            ▼
[5. Implementação Isolada por Contrato]
            │
            ▼
[6. Execução & Testes Automatizados]
            │
            ▼
[7. Inspeção Visual (Desktop + Mobile)]
            │
            ▼
[8. Correção de Defeitos & Entrega Final]
```

> *"Não apresentou erro de compilação" NÃO significa "o trabalho está pronto".*

---

## 👥 Papéis do Sistema Multiagente

### 1. Orquestrador
- Decompõe o objetivo macro em tarefas granulares.
- Cria o plano de execução e define critérios de aceitação.
- Controla os contratos compartilhados para impedir que Frontend ou Backend inventem campos.
- Coordena a suíte de testes e o gatekeeper final.

### 2. Arquiteto de Software
- Analisa a base existente e desenha a estrutura modular.
- Mantém `CLAREZA > MODA TECNOLÓGICA` e `CONTRATOS EXPLÍCITOS > SUPOSIÇÕES`.
- Formaliza a especificação OpenAPI (`contracts/api-contract.yaml`) e o modelo de dados (`contracts/data-model.md`).

### 3. Backend Engineer
- Implementa endpoints, lógica de domínio e validação estrita de dados.
- Trata erros de forma previsível e descritiva.
- Nunca diz apenas "API pronta"; entrega payload, schema de resposta, erros tratados e curl/script de teste funcional.

### 4. Frontend Engineer
- Começa entendendo a **tarefa do usuário**, e não escolhendo cores.
- **Tolerância Zero a AI Slop:**
  * Proibido gradientes decorativos sem função;
  * Proibido glassmorphism falso ou cards aninhados desnecessariamente;
  * Proibido emojis como ícones de interface profissional corporativa;
  * Proibido dashboards com gráficos fictícios ou dados mockados em produção.
- **Os 5 Estados Obrigatórios da UI:**
  1. `Carregando (Skeleton / Loading)`
  2. `Sucesso com Dados`
  3. `Estado Vazio (Empty State orientador)`
  4. `Erro Tratado (com ação de tentar novamente)`
  5. `Dados Parciais / Incompletos`

### 5. Pesquisador Técnico
- Investiga documentação primária oficial, papers científicos A1 e licenças open-source antes da adoção de dependências.

### 6. Engenheiro de Testes & Integração
- Garante a cobertura de caminhos felizes, bordas, payloads inválidos e integração real (zero dados inventados).

### 7. Crítico Visual (Quality Gate)
- Executa a aplicação e inspeciona visualmente as telas em múltiplos viewports (Desktop widescreen e Mobile viewport real).
- Aplica o Checklist Anti-AI Slop antes de autorizar o deploy.

---

## 📁 Estrutura Canônica de Contratos (`contracts/`)

```
contracts/
├── api-contract.yaml       # Especificação OpenAPI 3.0 / Endpoints
├── data-model.md           # Esquemas de entidades e relações
└── integration-notes.md    # Notas de consumo, headers e autenticação
```

---

## 📡 Comunicação Padronizada entre Agentes

Qualquer handoff entre módulos deve conter:
- **CONTEXTO:** O que está sendo desenvolvido.
- **ALTERAÇÃO:** O que foi modificado nos arquivos.
- **IMPACTO:** Módulos e agentes que devem ser notificados.
- **CONTRATO:** Alterações em payloads, tipos ou rotas.
- **TESTES:** Evidências de execução com saídas de terminal.
- **PENDÊNCIAS:** O que falta para a conclusão completa.

---

## 🏆 Checklist de Conclusão (10 Itens Obrigatórios)

- [ ] 1. O requisito foi atendido em sua totalidade.
- [ ] 2. O código foi executado sem warnings graves.
- [ ] 3. Todos os testes relevantes foram executados e passaram.
- [ ] 4. Frontend e Backend integrados sem divergências de campos.
- [ ] 5. Contrato em `/contracts` sincronizado com a implementação.
- [ ] 6. Interface inspecionada visualmente em desktop e mobile.
- [ ] 7. Os 5 estados da UI (loading, sucesso, vazio, erro, parcial) foram tratados.
- [ ] 8. Todos os elementos visuais possuem razão funcional clara.
- [ ] 9. O design passou no teste impiedoso Anti-AI Slop.
- [ ] 10. O sistema permanece rigorosamente coerente com a arquitetura geral do workspace.
