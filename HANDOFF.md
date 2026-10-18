# 🤝 Workspace Handoff & Estado de Continuidade
> Documento vivo de passagem de bastão. Lido no início de novas sessões para continuidade imediata sem perda de contexto.

---

## 📌 Metadados da Última Sessão
- **Ultima Atualizacao:** 17/10/2026 23:24
- **Branch Ativo:** `main` (Sincronizado com `develop` e `feature/cp03-distopia-utopia`)
- **Repositório GitHub:** [lira-labs/workspace](https://github.com/lira-labs/workspace.git)
- **Harness Principal:** Google Antigravity (Turbo Mode)
- **Harness de Contingência:** OpenCode (`core/harness/FAILOVER.md`)
- **Ambientes Sincronizados:**
  - *Notebook*: `D:\workspace`
  - *Desktop*: `C:\Users\ccunh\Documents\workspace`

---

## ✅ O que foi Concluído até Agora

### 1. Infraestrutura & Workspace OS
- [x] Sincronização multi-máquina configurada: clone completo no Desktop (`C:\Users\ccunh\Documents\workspace`).
- [x] Sistema de **Auto-Handoff** implementado: regras canônicas em `AGENTS.md`, regras em `.agent/rules/`, skill `.agent/skills/auto-handoff` e script automatizado `core/tools/handoff.ps1`.
- [x] Resolução de problemas no CI (`ci.yml`) e build verde.

### 2. Artefatos da VA2 (`va2/`) — Tópicos Avançados em IA (AI4Good)
- [x] **`va2/brw.md` (Artefato `[3] Brainwriting Híbrido` — Projeto *GrafoParada · Frota no Vazio*)**:
  - **Pivô pós-mentoria (16/10):** A ideia anterior (*Mar Aberto Paulista*, com pulseiras químicas e bóias costeiras) foi substituída após feedback do Prof. Lucas por depender de hardware/consumíveis físicos inviáveis para demonstração em software na disciplina.
  - **Problema e Dados Oficiais:** O "paradoxo da catraca" (apagão da demanda reprimida e má distribuição de frota no transporte público urbano, onde linhas com intervalos de 1 em 1 hora fazem passageiros desistirem antes de girar a catraca). Fundamentado com dados da **NTU** e **IPEA**: perda de **19,1 milhões de passageiros pagantes/dia** (queda de 44% a 46% na década) num setor que custa **R$ 75,7 bilhões/ano**.
  - **Mecanismo e Arquitetura de IA (100% demonstrável em software e independente da catraca fechada):**
    - **Canalizar (*clique que vota*) + Restringir (*trava de presença*):** O passageiro abre a parada no mapa com a localização (GPS) ligada para checar se o ônibus vem; regras determinísticas confirmam a presença física no raio da parada (e desistência antes do embarque) e leem pelo GPS público do ônibus o tempo de parada no ponto (*dwell time*, quando `velocidade = 0` por 15–60s) ou se o veículo passou direto.
    - **Inverter (*frota no vazio*) + ST-GNN (`Aula 07 · redes de grafos`):** Uma Rede Neural de Grafos Espaço-Temporal (ST-GNN) cruza os eventos de espera/desistência nas paradas com o *dwell time* e GPS/GTFS da frota para separar paradas realmente vazias de ônibus que passam direto por já virem lotados, propondo redistribuição de tabela horária sem exigir aumento total de frota.

### 3. Projetos Práticos da VA1 (`code/` e `papers/`)
- [x] **`code/topicos_avancados_ia_cp03/` (Experimento Utopia vs Distopia)** e artigo BRACIS sincronizado no Overleaf (`papers/`).
- [x] **`code/mlp_viewer/`** e **`code/tea_monitor/`** concluídos.

---

## 📋 Próximos Passos Recomendados para a Próxima Sessão

1. **Próximo Artefato da VA2 (`cmp · competidores e contribuição`):**
   - Construir a matriz de competidores e definir a contribuição científica do **GrafoParada · Frota no Vazio** frente aos sistemas tradicionais baseados apenas em bilhetagem eletrônica (OD de catraca) e apps passivos de consulta (Cittamobi/Moovit).
2. **Fluxograma, Arquitetura e Desenho Experimental (`flx` e `exp`):**
   - Preparar os artefatos das aulas de 21/10 (`flx`) e 23/10 (`exp` — *baseline* por média simples de parada vs. *ST-GNN* e *ablation study*) visando a Checagem Geral Ponto a Ponto em **30/10**.
3. **Checagem Pendente da VA1:**
   - Validar com o Prof. Lucas os itens já prontos de `arq·c`, `arq·p`, `arn·c`, `arn·p` e o 4º item de `tex`.

---

## ⚡ Prompt de 1 Linha para o Próximo Agente
> *"Estou iniciando uma nova sessão. Leia o arquivo `HANDOFF.md` e `AGENTS.md` para se situar no estado atual do workspace e continuar a partir das pendências da VA2 (GrafoParada · Frota no Vazio)."*
