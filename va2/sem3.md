# sem3 · Cauã da Cunha Lira

> roteiro do [seminário · iteração 3, como vai ser o teste](../4-seminario-teste.md), feito a partir do
> [exp.md](exp.md), [cmp.md](cmp.md) e [sem2.md](sem2.md).
> código no painel: `sem3` · de 4 a 6 slides · 5 a 7 minutos.

**link dos slides:** [Ver no Canva](https://www.canva.com/d/KsDvgkjJgBk2Cxr) · [Editar no Canva](https://www.canva.com/d/ZdkDfrWBdPQDITL) · [Baixar PPTX](https://grafoparadaweb.vercel.app/GrafoParada_Sem3_CauaLira.pptx) *(cópia em `va2/GrafoParada_Sem3_CauaLira.pptx`)*

**o commit da regra:** pré-registrado na branch `main` em **17/11/2026** (antes da apresentação de 18/11) com a frase 2, a métrica **TCGNS** + **Falso Alarme** e os limiares congelados de **passou**, **caiu** e **inconclusivo**.

**a máquina e a versão:** desktop/PC com `AMD Ryzen 7 5700G with Radeon Graphics` · `Windows 11` · `Python 3.12.15` · `PyTorch 2.14.1+cpu` · script [`code/grafoparada_tec/experimento_sem3_choques.py`](../code/grafoparada_tec/experimento_sem3_choques.py) na branch `main` (tag `sem3`).

**a ética:** teste **100% técnico sem pessoas** (180 cenários sintéticos pareados na topologia de 20 paradas da PE-60). O experimento humano E2 previsto no [`exp.md`](exp.md) não entra nesta semana de 7 dias por exigir avaliação prévia de comitê de ética (Res. CNS 510/2016 e Ofício CONEP 17/2022 não dispensam coleta que integre pesquisa/TCC).

---

## as quatro frases, sem IA

> `<!-- guia-ia -->`: **as quatro frases têm que ser faladas com as suas palavras em menos de 1 minuto (sem ler).** Abaixo estão os pontos-chave e os números reais do seu repositório para você falar de cabeça:

1. **o competidor:** *[sua frase em voz alta]* — C3 **ST-GCN pura (sem trava)**, C2 **Regressão Tabular de Corredor** (`1,93 min` MAE em 20 paradas no `sem2.md` / `2,46 min` em 5 paradas no `avaliar_piloto.py`) e C1 **Persistência / jeito de hoje** (`7,13 min` MAE em 20 paradas e `97%` de erro sem aviso no piloto de 5 paradas). Apps como Cittamobi e Moovit ficam fora da tabela por serem fechados e não rodarem nos cenários controlados; literatura relacionada ([Horn et al., 2025](https://doi.org/10.1109/ITSC60802.2025.11423733); [Mansurova et al., 2025](https://doi.org/10.3390/data10080119); [Niemann Tygesen et al., 2023](https://doi.org/10.1145/3615899.3627934)) confirma a relevância do problema, sem benchmark aberto direto de falsos negativos $> 40\text{ min}$.
2. **o que quero mostrar:** quero mostrar que a **Trava Híbrida Defensiva `[?]` (`|GPS − ST-GCN| > 15 min`)** reduz **os choques graves (> 40 min) perdidos sem aviso** para **o passageiro na parada** na PE-60, comparada à **ST-GCN pura e aos baselines tabulares/persistência**.
   - **Passou:** `TCGNS <= 5%` e `Falso Alarme <= 10%` com suporte do **IC 95% de Clopper–Pearson** por cenário.
   - **Caiu:** `TCGNS > 15%` ou `Falso Alarme > 20%`.
   - **Inconclusivo:** `5% < TCGNS <= 15%`, `10% < Falso Alarme <= 20%`, ou se o intervalo de confiança de 95% cruzar os limites.
3. **a comparação:** **180 cenários novos pareados** (`seeds 2000–2179`, congeladas e separadas das `seeds 100–159` de treino): **60 choques graves** ($> 40\text{ min}$), **60 intermediários** ($15\text{–}40\text{ min}$) e **60 normais** ($\le 15\text{ min}$) na mesma topologia de **20 paradas**. As 4 condições (**C1 Persistência**, **C2 Tabular**, **C3 ST-GCN pura**, **C4 ST-GCN + Trava `[?]`**) recebem exatamente o mesmo corredor, horário, atraso cinemático GPS e gabarito independente.
4. **o caminho até o pitch:** malha GTFS (393 linhas), `ST-GCN` + script [`experimento_sem3_choques.py`](../code/grafoparada_tec/experimento_sem3_choques.py) já rodaram o teste pequeno (`--mode smoke`, 6 cenários) antes de 18/11; congelamento em **19/11**, execução oficial dos 180 cenários em **25/11**, conferência em **27/11** e tabela com ICs no pitch de **02/12**. **Plano B:** execução 100% offline sobre `test_set.csv` congelado localmente, sem depender de internet, navegador ou banco remoto.

---

## slide 1 · o competidor e o que ele consegue · ~65 s

- **aparece:** a falha real do `sem2` no Nó 10 da PE-60 (`45,0 min` real vs `14,3 min` previsto pela ST-GCN pura = `30,7 min` apagados sem aviso) ao lado dos competidores **C1 Persistência** (`7,13 min` MAE em 20 nós; `97%` FN no piloto de 5 nós), **C2 Tabular de Corredor** (`1,93 min` MAE em 20 nós; `2,46 min` em 5 nós) e **C3 ST-GCN pura** (`1,51 min` em regime normal).
- **a medida dele, e o número:**
  - Números próprios do piloto ([`avaliar_piloto.py`](../code/grafoparada_tec/avaliar_piloto.py) e [`motor_evolucao_prototipo.py`](../code/grafoparada_tec/motor_evolucao_prototipo.py)).
  - Fontes abertas verificadas sem inventar números: [Horn et al. (2025)](https://doi.org/10.1109/ITSC60802.2025.11423733) (3 anos AVL Holanda, sem benchmark de FN $> 40$ min), [Mansurova et al. (2025)](https://doi.org/10.3390/data10080119) (Astana, >19 mil viagens GPS 5s, sem benchmark de choque 45 min), [Niemann Tygesen et al. (2023)](https://doi.org/10.1145/3615899.3627934) (grafos + incidentes reduzem erro sob congestionamento não recorrente), [Wang et al. (2022)](https://doi.org/10.1016/j.trc.2022.103790) e [Kim, Yun & Kim (2026)](https://doi.org/10.1016/j.jpubtr.2026.100175).
- **pontos de apoio na sua fala (não ler):** explicar que apps comerciais fechados (Cittamobi/Moovit) não revelam modelos nem rodam nos mesmos cenários controlados; por isso a comparação científica justa usa C1, C2 e C3 sobre a mesma entrada.

## slide 2 · o que quero mostrar e como vou medir · ~75 s

- **aparece:** a frase-alvo + definição da métrica principal **TCGNS** ($\text{FN}_{\text{choques}} / N_{\text{choques}} \times 100$) + tabela visual de **PASSOU / CAIU / INCONCLUSIVO**.
- **o alvo:** evitar falhas silenciosas (choque $> 40\text{ min}$ sem alerta dentro da janela de decisão). **Por que não usabilidade/SUS:** uma nota SUS alta com `14,3 min` na tela enquanto o ônibus está a `45,0 min` continua enganando quem espera no ponto.
- **métricas secundárias:** Taxa de Falso Alarme (**FPR**), Sensibilidade, Precisão do alerta, **MAE geral** e **MAE nos choques graves** (comparando capacidade de detectar separada da de prever).
- **passou, caiu, inconclusivo:**
  - **Passou:** `TCGNS <= 5%` e `FPR <= 10%` (com **IC 95% Clopper–Pearson** dentro dos limites).
  - **Caiu:** `TCGNS > 15%` ou `FPR > 20%`.
  - **Inconclusivo:** valores intermediários (`5% < TCGNS <= 15%` ou `10% < FPR <= 20%`) ou **IC 95% cruzando o limiar**.
- **pontos de apoio na sua fala (não ler):** enfatizar que `|atraso_GPS_min - ST-GCN| > 15 min` compara duas grandezas na mesma unidade (atraso em minutos na parada) com limiar congelado antes de `25/11`, e que a regressão tabular pode até empatar ou vencer em MAE — e tudo bem, o teste pode reprovar ou dar inconclusivo.

## slide 3 · como será a comparação · ~80 s

- **aparece:** esquema em fluxo:
  `180 Cenários Pareados (20 nós · seeds 2000–2179)` $\rightarrow$ `C1 Persistência | C2 Tabular | C3 ST-GCN Pura | C4 ST-GCN + Trava [?]` $\rightarrow$ `Gabarito único independente` $\rightarrow$ `CSV + IC 95% (Clopper–Pearson & Bootstrap por cenário)`.
- **quem ou o que entra:** `180` cenários independentes (`60` graves $> 40\text{ min}$, `60` intermediários $15\text{–}40\text{ min}$, `60` normais $\le 15\text{ min}$), com choques distribuídos pelos nós internos do corredor de 20 paradas. Com `60` choques e `0` FN, o limite superior do IC 95% fica em `~4,87%`, sustentando a meta de `5%`.
- **as condições:** C1, C2, C3 e C4 (pesos de C2/C3 congelados nas `seeds 100–159`).
- **o que fica igual:** mesma topologia (20 nós), mesmo horário, mesmos lags de entrada, mesmo atraso cinemático GPS e mesmas `seeds 2000–2179`.
- **o gabarito:** atraso real injetado e rótulo `is_grave` (`> 40 min`) definidos de forma independente pelo gerador antes da inferência de qualquer modelo.

## slide 4 · como chegar ao pitch com resultado · ~60 s

- **aparece:** calendário visual `18/11 Plano` $\rightarrow$ `19/11 Congelamento` $\rightarrow$ `20–24/11 Validação` $\rightarrow$ `25/11 Execução oficial` $\rightarrow$ `27/11 Auditoria` $\rightarrow$ `02/12 Pitch` + caixa **Teste Pequeno (`--mode smoke`)** e **Plano B**.
- **já pronto:** malha GTFS 393 linhas, ST-GCN oficial (`stgcn_official.py`), protótipo de 20 nós e script [`experimento_sem3_choques.py`](../code/grafoparada_tec/experimento_sem3_choques.py).
- **o teste pequeno (rodado antes de 18/11):**
  - Na 1ª execução de `--mode smoke`, o script **quebrou** com `TypeError: STGCN.__init__() got an unexpected keyword argument 'num_features'` porque a rede oficial usa `(num_nodes, in_channels=1, out_horizon=1)` e janela fixa `HISTORY_LEN=12`.
  - Corrigido e re-executado (`6` cenários: `2` graves, `2` intermediários, `2` normais), gerou `results_raw_smoke.csv` e `evaluation_report_smoke.json` em ~7s: `C1 Persistência` (`100%` FN), `C3 ST-GCN pura` (`100%` FN nos 2 choques), `C4 Trava Híbrida` (`0%` FN, `0%` FP). Isso validou o pipeline antes de `25/11`.
- **plano B:** execução 100% local e offline usando `test_set.csv`, `results_raw.csv` e `evaluation_report.json` congelados, sem depender de internet, Vercel ou banco Neon remoto.

## slide 5 · fecho e limite honesto · ~35 s

- **aparece:** duas colunas objetivas: **O que o teste prova** vs **O que não prova ainda**.
- **pontos de apoio na sua fala (não ler):** demonstra robustez experimental controlada a choques fora da distribuição de treino em topologia de 20 paradas da PE-60; **não** substitui validação operacional em campo no Grande Recife, que depende de acesso contínuo ao streaming AVL/GPS do CTM e de comitê de ética para coleta humana.

**tempo total, cronometrado:** *[preencha após ensaiar 2x seguidas com cronômetro — meta: entre 5 e 7 minutos]*

---

## ensaio cético

> `<!-- guia-ia -->`: **Rode o ensaio cético (Passo 3) em uma conversa nova**, colando o prompt do enunciado com as suas 4 frases e o texto dos slides.

**a pergunta mais difícil:** *[preencha após rodar o ensaio cético na conversa nova]*

**o que eu mudei por causa dela:** *[preencha após rodar o ensaio cético na conversa nova]*
