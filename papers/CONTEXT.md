# Papers Subtree Context — Relatórios Técnicos & Manuscritos
> Diretório dedicado à produção acadêmica e relatórios técnicos da disciplina *Tópicos Avançados em Inteligência Artificial (AI4Good)*.
> Estrutura modular e organizada por projeto para compilação local e sincronização com o Overleaf.

---

## 📂 Organização por Projeto (Subpastas Dedicadas)

### 1. `01-mlp/` — Relatório Técnico MLP Interativa (`mlp·p`)
- **Arquivo Principal:** `report-mlp.tex` (também espelhado na raiz para o Overleaf)
- **Figuras:** `01-mlp/figures/antes.png`, `01-mlp/figures/depois.png`
- **Código Relacionado:** `code/mlp_viewer/` (MLP em grafo computacional do zero sobre Heart Disease e Diabetes)

### 2. `02-arch/` — Relatório Técnico Arquitetura Deep Learning (`arq·p`)
- **Arquivo Principal:** `report-arch.tex` (também espelhado na raiz para o Overleaf)
- **Seções Modulares:** `02-arch/sections/` (`01_introducao.tex` a `05_conclusao.tex`)
- **Figuras:** `02-arch/figures/` (`architecture_rapunet.png`, `dataset_samples.png`, `metrics_comparison.png`, `segmentation_results.png`, `training_curves.png`)
- **Código Relacionado:** `code/topicos_avancados_ia_cp02/` (RAPUNet-Zeta sobre Kvasir-SEG)

### 3. `03-arena/` — Relatório Técnico Arena Dialética Multiagente (`arn·p`)
- **Arquivo Principal:** `report-arena.tex` (também espelhado na raiz para o Overleaf)
- **Figuras:** `03-arena/figures/` (`utopia_metrics.png`, `distopia_metrics.png`, `harness.png`)
- **Código Relacionado:** `code/topicos_avancados_ia_cp03/` (Arena Utopia vs. Distopia em 20 rodadas)

---

## 🔄 Como Compilar no Overleaf
No menu superior esquerdo do Overleaf (**Menu**), selecione no campo **Main document** o relatório desejado:
- Para `mlp·p`: Selecione `report-mlp.tex`
- Para `arq·p`: Selecione `report-arch.tex`
- Para `arn·p`: Selecione `report-arena.tex`

Para sincronizar automaticamente com o Overleaf via linha de comando:
```powershell
powershell -ExecutionPolicy Bypass -File "core/tools/sync_overleaf.ps1" -Action push -CommitMessage "sua mensagem"
```
