# Scientific Audit · Compasso Cognitivo (3 Revisores)

- **Data:** 18/11/2026 · **Status:** **RASCUNHO ESTRUTURADO (Aguardando Dados Experimentais)**

## Parecer do Revisor Científico
- **Pontos resolvidos:** Inclusão dos concorrentes críticos (`FLoRA Engine`, `ActivityWatch`, `Hutt et al. 2024`, `one sec`); distinção explícita entre atenção visual, comportamental e cognitiva.
- **Bloqueador para submissão:** Seção 4 contém placeholders `[--]` para o estudo com $N=15$ participantes e ablação de falsos alertas; sem esses dados, o artigo seria rejeitado por falta de validação empírica.

## Parecer do Revisor Técnico
- **Pontos resolvidos:** Removido `YOLO11n` inexistente; separado motor heurístico zero-clique do Ollama visual (`gemma3:4b`) e documentado o gadget WPF (`tray.ps1`).
- **Pendência de código/benchmark:** Na branch `compasso-aprovacao`, a UI ainda traz `llama3:8b` como default para análise visual (precisa voltar a `gemma3:4b`); falta medir CPU/RAM/FPS reais no `Compasso.exe` final.

## Parecer do Revisor Editorial
- **Pontos resolvidos:** Zero *AI slop*, argumentação por mecanismos/hipóteses e tabela comparativa objetiva.
- **Pendência para versão final internacional:** Adicionar figuras reais em `figures/`, traduzir para o inglês e adaptar para o template oficial do veículo escolhido (SIGCSE / EAAI / IJCAI).
