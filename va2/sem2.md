# sem2 · Cauã da Cunha Lira

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), feito a partir do
> [tec.md](tec.md), do [flx.md](flx.md), do [exp.md](exp.md) e do [sem1.md](sem1.md).
> código no painel: `sem2`.

**link dos slides:** [va2/slides_sem2.html](https://grafoparadaweb.vercel.app/slides_sem2.html) e [va2/GrafoParada_Sem2_Roteiro.pptx](https://grafoparadaweb.vercel.app/GrafoParada_Sem2_Roteiro.pptx) *(versão Canva em [va2/GrafoParada_Seminario2_CauaLira.pptx](GrafoParada_Seminario2_CauaLira.pptx) — ver auditoria no fim)*

**a versão que roda:** branch `main` (tag `sem2`) em [github.com/lira-labs/workspace](https://github.com/lira-labs/workspace) · app ao vivo em [grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app)

**a máquina:** desktop/PC com `AMD Ryzen 7 5700G with Radeon Graphics` · `Windows 11` · `Python 3.12.15` · `PyTorch 2.14.1+cpu` + smartphone/navegador conectado em [grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app)

**a gravação de reserva:** [va2/entrega_ai4good.mp4](https://github.com/lira-labs/workspace/blob/main/va2/entrega_ai4good.mp4) *(regravar a segunda passada sem cortes na mesma máquina após concluir os Passos 3 e 4 na versão final)*

---

## passo 1 · as quatro frases, sem IA

> `<!-- guia-ia -->`: **as quatro frases têm que ser suas, escritas e faladas por você sem ler (< 1 min ao todo).** Os tópicos abaixo trazem apenas os fatos e números reais medidos no repositório para você formular cada frase com suas palavras:

1. **a demo:** *[sua frase]* — Âncoras reais: passageiro/trabalhador no Grande Recife usa GPS dinâmico + destino no app (`393` linhas reais do GTFS CTM, Laya IA e rotas multi-etapas SEI) para ver qual ônibus/conexão pegar e a hora certa de sair sem esperar no vazio.
2. **o custo:** *[sua frase]* — Âncoras reais (`medir_custo_sem2.py`): STGCN (20 nós) em CPU = **`0,96 ms`** e **`324,7 MB`** de Working Set físico (`2,22 KB` heap; treino 25 épocas = `0,86 s`); FSM on-device (15 passos) = **`56,68 µs`** e **`11,02 KB`**; contra o estimado no [`flx.md`](flx.md): **`< 0,5 s` (`500 ms`) / `~300 MB`** na STGCN (`< 10 s` com treino) e **`14,29 µs` / `8,92 KB`** no passo único on-device. R$ 0,00 local. Diferença explicada pelas DLLs do runtime LibTorch/Windows (`+8,2%` nos MB) e pela inferência ~520× menor que `500 ms`.
3. **a falha:** *[sua frase]* — Âncoras reais (`medir_custo_sem2.py` · slide 3): entrada = bloqueio pontual de **`45,0 min`** no Nó 10 (Trevo de Ipojuca / PE-60); saída da STGCN = **`14,3 min`** (super-suavização); o certo = **`45,0 min`** + alerta `[?]`; quem sofre = trabalhador/estudante na PE-60 que perde o transporte alternativo e perde o turno. Ensina que `|GPS − STGCN| > 15 min` exige trava híbrida para cortar a IA.
4. **o que mudou:** *[sua frase]* — Âncoras reais: no [`sem1.md`](sem1.md) / [`avaliar_piloto.py`](../code/grafoparada_tec/avaliar_piloto.py) (5 paradas), a regressão tabular (`2,46 min` MAE) bateu a STGCN (`4,42 min`); mantivemos a STGCN para testar escala em [`motor_evolucao_prototipo.py`](../code/grafoparada_tec/motor_evolucao_prototipo.py) (20 paradas da PE-60 em simulação sintética): a STGCN fez **`1,51 min`** contra **`1,93 min`** da linear tabular (121 colunas para 70 treinos) e **`7,13 min`** da persistência. Validação em rua real ainda depende de GPS contínuo do CTM.

---

## slide 1 · ponta a ponta · ~80 s

- **uma ideia:** a tela do sistema rodando ao vivo ([grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app)), com usuário, entrada real, saída e ação permitida.
- **aparece:** quem usa, entrada real (GPS + destino entre `393 linhas` do GTFS CTM), saída na tela (rota SEI, previsão e voz PT-BR), o que deixa fazer + link da demo ao vivo.
- **o sistema roda:** demonstrado ao vivo do repositório (sem vídeo pré-gravado como principal).
- **pontos de apoio na sua fala (não ler):**
  - abrir o app ao vivo no celular/tela na pergunta de localização (`Onde você está agora?`);
  - rodar uma consulta real (ex.: Camela -> Ipojuca/Olinda ou linha do GTFS CTM + assistente Laya);
  - mostrar a saída na tela e explicar em 1 frase o que o passageiro faz com ela antes de ir para o ponto.

## slide 2 · quanto custa, medido · ~50 s

- **uma ideia:** tempo total e pico de memória de uma execução real do repositório, lado a lado com o estimado no [`flx.md`](flx.md).
- **saída real de `uv run --project code/grafoparada_tec python code/grafoparada_tec/medir_custo_sem2.py`:**

```text
Maquina: AMD Ryzen 7 5700G with Radeon Graphics | SO: Windows 11
Runtime: Python 3.12.15 | PyTorch 2.14.1+cpu (CPU)

[1. ON-DEVICE / CELULAR - FSM CINEMATICA V3]
  - Tempo medio por inferencia (500x): 56.68 us (0.0567 ms)
  - Pico de heap Python por ciclo (tracemalloc): 11.02 KB
  - Estimativa no flx.md: 14,29 us (passo unico) e 8,92 KB de RAM (validar_cinematica_parada.py)

[2. SERVIDOR / STGCN 20 NOS PE-60 (CPU PYTORCH)]
  - Parametros treinaveis: 34,627
  - Tempo de treino (25 epocas, 64 amostras): 0.86 s
  - Tempo medio por inferencia completa em CPU (200x): 0.96 ms
  - Heap Python na inferencia (tracemalloc): 2.22 KB (0.002 MB)
  - Pico de Working Set fisico total (C++/LibTorch + Python): 324.7 MB
  - Estimado no flx.md: < 10 s (treino 25 epocas + inferencia); < 0,5 s (inferencia) e ~300 MB de RAM
```

- **diferença explicada:** os tensores da inferência usam só `2,22 KB` em `0,96 ms` (~520× abaixo do teto de `500 ms`), mas o processo completo segura `324,7 MB` (`+8,2%` sobre `~300 MB`) por causa das bibliotecas dinâmicas do PyTorch/LibTorch carregadas no Windows. Na FSM de 15 passos (`56,68 µs` e `11,02 KB`), o tempo soma toda a trajetória contra `14,29 µs` do passo único no `flx.md`. Custo financeiro local: `R$ 0,00`.

## slide 3 · a falha mostrada · ~60 s

- **uma ideia:** entrada que erra, saída errada, o certo ao lado e quem sofre.
- **a entrada:** choque abrupto no Nó 10 (Trevo de Ipojuca · PE-60) com atraso de GPS em **`45,0 min`** (demais paradas em `10,0 min`).
- **a saída, como saiu:** a STGCN previu **`14,3 min`** no Nó 10 (super-suavização apagou `30,7 min` do pico).
- **o certo (ao lado):** **`45,0 min`** + selo de alerta **`[?]` Interdição** (`avaliar_trava_hibrida_defensiva` detecta `|45,0 − 14,3| = 30,7 min > 15,0 min` e força exibição do GPS bruto).
- **quem sofre:** o trabalhador ou estudante na parada da PE-60 que confia no `14,3 min`, deixa passar o transporte alternativo e perde o turno/aula.
- **demonstração no app:** botão *"Simular Choque / Interdição na Via (Demonstração da Falha · Sem2)"* exibe `14,3*` vs GPS bruto `45,0 min`.

## slide 4 · o que mudou desde o sem1 · ~45 s

- **uma ideia:** o que valia no `sem1`, o que vale no `sem2` e o porquê.
- **no sem1 (5 paradas · [`avaliar_piloto.py`](../code/grafoparada_tec/avaliar_piloto.py)):** regressão tabular de corredor (`2,46 min` MAE) bateu a STGCN (`4,42 min` MAE).
- **agora no sem2 (20 paradas PE-60 · [`motor_evolucao_prototipo.py`](../code/grafoparada_tec/motor_evolucao_prototipo.py)):** mantivemos a STGCN para testar escala. Em dados sintéticos de difusão no corredor de 20 paradas (70 treino / 50 teste):
  - Persistência: **`7,13 min`** MAE
  - Regressão tabular achatada (121 colunas para 70 casos): **`1,93 min`** MAE
  - STGCN com grafo Laplaciano: **`1,51 min`** MAE
- **limite honesto:** a melhoria de MAE ocorreu em simulação sintética; validar o ganho em campo exige streaming contínuo de GPS/VEM do CTM.

## slide 5 · fecho e ponte para o sem3 · ~25 s

- **uma ideia:** resumo do que roda hoje e qual falha vira medida no `sem3` (`25/11`).
- **aparece:** hoje (`393 linhas` GTFS reais, `0,96 ms` em CPU, `R$ 0,00` local, trava `[?]`) + pergunta do `sem3` (`25/11`): quantos choques de trânsito a trava híbrida captura contra a STGCN pura.

---

## passo 3 · ensaio cético (conversa nova) · PENDENTE

> **Status:** `[ ]` **Pendente.** Abrir uma **conversa nova** (limpa, que não ajudou a montar este roteiro), colar suas **4 frases reais**, os slides e a saída de `medir_custo_sem2.py` usando o prompt abaixo, responder as 5 perguntas de cabeça e registrar aqui apenas a **pergunta mais difícil** e **o que mudou no roteiro/slide/demo por causa dela**.

- **a pergunta mais difícil:** *[preencher após rodar o Passo 3 numa conversa nova]*
- **o que mudei por causa dela:** *[preencher o que ajustou na frase, no slide ou na demo]*

---

## passo 4 · cronômetro e vídeo de reserva · PENDENTE

> **Status:** `[ ]` **Pendente.** Cronometrar duas passadas seguidas em voz alta, de cabeça, entre **3 e 5 minutos**, com a demo rodando ao vivo na máquina da apresentação, e gravar a segunda passada sem cortes.

- **passada 1 (tempo medido):** *[preencher após cronometrar]*
- **passada 2 sem cortes (tempo medido):** *[preencher após cronometrar + atualizar `va2/entrega_ai4good.mp4` se a versão mudou]*

---

## itens de verificação (preencher só após passos 1, 3 e 4 reais)

- [ ] **ponta a ponta, ao vivo:** usuário concreto, entrada real do problema, saída na tela e o que deixa fazer, rodando do repositório.
- [ ] **quanto custa, medido:** tempo total (`0,96 ms` STGCN / `56,68 µs` FSM) e pico de memória (`324,7 MB` Working Set / `11,02 KB` FSM), máquina identificada (`AMD Ryzen 7 5700G`, `Python 3.12.15`), diferença para o `flx.md` explicada.
- [ ] **a falha mostrada:** entrada (`45,0 min` Nó 10), saída errada (`14,3 min`), certo ao lado (`45,0 min` + `[?]`) e quem sofre (trabalhador/estudante na PE-60).
- [ ] **o que mudou desde o sem1:** `sem1` (`2,46 vs 4,42` em 5 paradas) -> decisão de manter STGCN -> `sem2` (`1,51 vs 1,93 vs 7,13` em 20 paradas sintéticas) e limite de validação em campo.

---

## apêndice factual · transparência de dados (referência para a banca)

| Componente | Origem real no repositório |
| :--- | :--- |
| Paradas, linhas e trajetos | GTFS oficial do Grande Recife (`393 linhas`, `gtfs_real_network.json`) |
| Medições de tempo, memória e falha | Execução local de `code/grafoparada_tec/medir_custo_sem2.py` |
| Comparativo 5 vs 20 paradas | `avaliar_piloto.py` e `motor_evolucao_prototipo.py` (dados sintéticos de difusão) |
| Telemetria contínua AVL/VEM | Não pública no CTM (dependência explícita para validação em campo) |
