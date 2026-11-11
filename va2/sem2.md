# sem2 · Cauã da Cunha Lira

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), feito a partir do
> [tec.md](tec.md), do [flx.md](flx.md), do [exp.md](exp.md) e do [sem1.md](sem1.md).
> código no painel: `sem2` · quarta, 11/11.

**link dos slides:** [va2/slides_sem2.html](https://github.com/lira-labs/workspace/blob/main/va2/slides_sem2.html) (versão web interativa) e [va2/GrafoParada_Seminario2_CauaLira.pptx](https://github.com/lira-labs/workspace/blob/main/va2/GrafoParada_Seminario2_CauaLira.pptx)

**a versão que roda:** commit [`565321f`](https://github.com/lira-labs/workspace/commit/565321f) (ou tag `sem2`) no repositório [github.com/lira-labs/workspace](https://github.com/lira-labs/workspace)

**a máquina:** o meu Desktop / Notebook Windows (Intel Core CPU com Python 3.12 + PyTorch) e o smartphone conectado ao vivo pelo link de produção [https://grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app)

**a gravação de reserva:** [va2/entrega_ai4good.mp4](https://github.com/lira-labs/workspace/blob/main/va2/entrega_ai4good.mp4) (e tomada contínua do ensaio sem cortes, anexada à release `sem2`)

---

## as quatro frases, sem IA

1. **a demo:** O trabalhador em Camela ou no TI Cabo — seja com a Janela Segura de Saída (06h08) baseada no seu turno, o Letreiro LED idêntico ao ônibus ou o Farol Noturno anti-queima de 76px — recebe a previsão da Linha 199 com folga no VEM e resgate contra alagamentos; e a agregação anônima de suas rotinas alimenta a Central CTM para realocar ônibus vazios da Linha 178 para a 199.
2. **o custo:** No celular, a máquina de estados cinemática levou 4,98 milissegundos e 12 KB de RAM; no servidor, a STGCN de 20 nós levou 0,77 milissegundos na CPU e 84 KB de tensores, dentro do processo PyTorch de 358 MB. O flx estimava menos de 500 ms e 300 MB, e a diferença é que a inferência pura na CPU é quase instantânea e o runtime completo segura os pesos em memória.
3. **a falha:** Num bloqueio súbito no Trevo de Ipojuca com 45 minutos de atraso real no GPS, a STGCN suavizou o salto pelo grafo e previu apenas 18 minutos; quem sofre é o trabalhador na parada da PE-60 que acha que o ônibus tá perto e perde o turno da fábrica; esse erro revela que redes de grafo sofrem de super-suavização espacial, e por isso o GrafoParada nunca esconde o dado bruto do GPS e acende o alerta de interdição [?] na tela.
4. **o que mudou:** No sem1, o cálculo simples tinha superado a STGCN no corredor curto de 5 paradas e eu prometi testar na malha completa; agora, com as 20 paradas da PE-60 e os dados reais de 400 linhas do GTFS, a STGCN virou o jogo e bateu a regressão com 1,51 minuto de erro contra 1,93 minuto, provando que quando a rede cresce a IA espacial se justifica; e o app deixou de ser um rastreador passivo para virar um sistema ativo de realocação da frota no vazio alimentado pela rotina das pessoas e adaptado para todas as idades.

---

## slide 1 · ponta a ponta, ao vivo · 80 s

- **aparece:** O smartphone com o GrafoParada rodando ao vivo ([grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app)). O mapa em Camela com a Linha 199. Na tela: o card 'Minha Rotina Pendular' com a Janela Segura de Saída (saia às 06h08), o Letreiro LED idêntico ao coletivo, o Guardião da Integração Temporal VEM (1h 14m restantes), o Farol Noturno anti-queima de 76px e o painel da Central CTM com a realocação da frota no vazio.
- **a entrada:** 1 toque no card `📅 Minha Rotina (Turno Suape 05h45)` para calcular a saída de casa sem mofar no ponto; ou o toque na `🏛️ Central CTM` para transferir um ônibus vazio da Linha 178 para a Linha 199.
- **eu falo:** [Com o app aberto e espelhado na tela] "Esse é o GrafoParada rodando ao vivo do nosso repositório. O passageiro não usa o transporte de forma aleatória: ele tem uma rotina de trabalho ou estudo. Com um único toque, o trabalhador de Suape ativa a sua rotina das 05h45. O app calcula a Janela Segura de Saída de casa: como a caminhada até a parada leva 6 minutos e o 199 chega às 06h14, ele avisa para sair exatamente às 06h08, evitando que o passageiro fique exposto no acostamento escuro da rodovia. E para a Dona Severina, de 68 anos, que tem medo de errar o ônibus, o app exibe na tela o Letreiro LED idêntico ao letreiro da frente do coletivo (199 CAMELA/CABO) e fala em voz alta: 'Dona Severina, o 199 chega em 4 minutos, tem 14 bancos vazios'. E vejam a nossa tese funcionando: 48 trabalhadores cadastraram essa rotina. A Central CTM detecta que o ônibus regular vai superlotar e que a Linha 178 de Suape está voltando com apenas 3 passageiros — quilometragem morta, o chamado deadheading, jogando fora 14 litros de diesel por hora. Com um clique do despachante, o veículo ocioso é remanejado para a Linha 199: a espera cai de 18 para 4 minutos e ninguém fica na chuva!"

---

## slide 2 · quanto custa, medido · 50 s

- **aparece:** Quadro comparativo direto entre o estimado no `flx.md` e o medido ao vivo em `medir_custo_sem2.py`:
  - *No Celular:* Estimado = 14,29 µs · 8,92 KB | Medido = **4,98 ms** (inferência completa) / **14,29 µs** (passo rotina) · **12,0 KB** de RAM.
  - *No Servidor (STGCN 20 Nós PE-60):* Estimado = < 500 ms · ~300 MB | Medido = **0,77 ms** por ciclo na CPU · **83,7 KB** de tensores ativos (**358,2 MB** total do processo PyTorch no SO).
  - *Custo em Reais:* R$ 0,00 (roda na CPU do consórcio sem placa de vídeo).
- **medido:** Execução real em `code/grafoparada_tec/medir_custo_sem2.py` (commit `565321f`), CPU Intel, Python 3.12 + PyTorch: 0,77 ms na CPU para as 20 paradas da PE-60; FSM cinemática v3 com Soft-Voting em 4,98 ms no aparelho.
- **estimado no flx:** < 500 ms de inferência e ~300 MB de RAM.
- **eu falo:** "Esse número não é estimativa: ele saiu da medição real que rodou agora no repositório com o script `medir_custo_sem2.py`. No celular do passageiro, a máquina de estados cinemática com Soft-Voting leva 4,98 milissegundos e gasta apenas 12 kilobytes de RAM, sem drenar bateria. No servidor local do consórcio, a nossa rede STGCN com 34 mil parâmetros rodou em apenas 0,77 milissegundo por ciclo na CPU — muito abaixo dos 500 milissegundos que eu tinha estimado no flx. E a memória: os tensores da rede ocupam só 84 kilobytes, enquanto o processo inteiro do PyTorch na máquina consome 358 megabytes, que foi o que medimos no experimento E1. A diferença para os 300 megabytes estimados no flx é que o runtime do PyTorch segura as bibliotecas dinâmicas em memória, mas o cálculo em si é levíssimo. O custo segue zero reais: roda num computador comum de escritório do CTM, sem gastar um centavo com nuvem paga."

---

## slide 3 · a falha mostrada de propósito · 65 s

- **aparece:** A demonstração da falha ao vivo no app (botão `🧪 Simular Interdição PE-60`): a previsão do primeiro ônibus muda de 4 min para um alerta amarelo: `[⚠️ ALERTA: STGCN suavizou para 18 min · GPS Real = 45 min]`. Ao lado, o gráfico de over-smoothing da STGCN.
- **a entrada:** Bloqueio súbito de trânsito no Trevo de Ipojuca (Nó 10 da PE-60). O GPS bruto do veículo registra que o ônibus parou e o atraso real salta de 5 min para **45 minutos**.
- **a saída, como saiu:** A rede neural STGCN difunde o atraso pela matriz Laplaciana para as paradas vizinhas e prevê apenas **18 minutos** no ponto.
- **o certo:** O app alertar **45 minutos de atraso** (ou exibir aviso de interdição na via).
- **eu falo:** "Eu fiz questão de trazer este caso porque ele erra de verdade. Imaginem que houve um acidente ou manifestação no Trevo de Ipojuca e a rodovia travou: o atraso real no GPS salta de 5 para 45 minutos. Olhem o que a STGCN faz na tela: como ela usa convolução em grafo com matriz Laplaciana, ela 'espalha' o atraso entre as paradas vizinhas e prevê apenas 18 minutos. O número parece razoável, mas é mentiroso. Quem sofre esse erro é o trabalhador na parada de Camela ou de Ipojuca: ele vê '18 minutos', fica esperando, o ônibus leva 45 minutos para chegar e ele toma advertência ou perde o emprego na fábrica de Suape. Esse erro me ensinou algo fundamental sobre a IA: redes de grafo sofrem de super-suavização espacial (*over-smoothing*) quando há choques bruscos isolados. E como nós resolvemos isso no GrafoParada? Nós nunca escondemos o dado bruto do GPS: se a divergência entre a STGCN e o GPS passar de 15 minutos, a tela acende o selo amarelo de interdição [?] avisando ao passageiro que a via travou. Essa falha é exatamente a nossa métrica para o experimento do Sem3: quantos desses choques a regra híbrida consegue blindar contra o erro puro da IA."

---

## slide 4 · o que mudou desde o sem1 · 50 s

- **aparece:** Quadro comparativo:
  - *No Sem1:* Corredor curto de 5 paradas: cálculo simples superou a STGCN (2,46 min vs 4,42 min). Promessa de validar se a IA se justificava na malha maior. Interface cheia de gráficos de desenvolvedor.
  - *Agora no Sem2:* Na malha real de 20 paradas da PE-60, a STGCN virou o jogo (**MAE = 1,51 min vs 1,93 min** da regressão linear e **7,13 min** da persistência). App evoluiu de um rastreador passivo para um sistema ativo de mitigação de frota no vazio alimentado pela rotina das pessoas, com acessibilidade universal (Modo Fácil para idosos, Modo Bolso para estudantes, Farol Noturno e proteção do VEM).
- **no sem1:** "No corredor curto de 5 paradas, o cálculo mais simples superou a STGCN (2,46 contra 4,42 min). Vamos testar na malha completa."
- **agora:** Confirmado com dados reais: em 20 paradas da PE-60, a STGCN venceu a regressão por 0,42 min e reduziu o erro em 78% contra a persistência. A tese central de entender a rotina para realocar ônibus ociosos foi implementada ponta a ponta.
- **eu falo:** "No sem1, eu fui honesto e mostrei que, no trecho curto de 5 paradas, uma conta simples de padaria tinha errado menos que a STGCN (2,46 contra 4,42 minutos). Prometi para a banca que ia testar na malha completa para ver se a IA realmente se pagava. Hoje eu trago a resposta com dados reais: nas 20 paradas da PE-60, a STGCN virou o jogo. Ela cravou um erro de 1,51 minuto, batendo a regressão linear que deu 1,93 minuto e a persistência que deu 7,13 minutos. Quando o corredor cresce e os atrasos se propagam entre as linhas, a IA espacial se justifica plenamente. Mas a maior mudança foi de conceito: o app deixou de ser um mero rastreador de ônibus passivo como o Cittamobi. Ele passou a entender a rotina das pessoas para balancear a frota no vazio do Grande Recife, acabando com ônibus rodando sem passageiro enquanto a população espera no escuro da PE-60."

---

## slide 5 · o fecho · 20 s

- **aparece:** O balanço da realocação: 14 L de diesel economizados por viagem ociosa evitada · R$ 4,10 de VEM protegido contra cobrança dupla · R$ 155,80 de receita preservada contra ligeirinhos · 166 bytes locais no celular.
- **eu falo:** "O GrafoParada roda no celular, roda na CPU do consórcio a custo zero e protege o trabalhador do assalto no escuro da parada. A desistência na parada financia o ônibus no pico. No dia 25, no sem3, eu trago a validação experimental com passageiros reais na PE-60 provando quantos desses gargalos nós conseguimos evitar antes da catraca."

---

**tempo total, cronometrado com a demo rodando:** 4 min 20 s (primeira passada) e 4 min 10 s (segunda passada).

---

## ensaio cético

**a pergunta mais difícil:** "Se a STGCN erra feio quando tem um acidente na PE-60 prevendo 18 minutos em vez de 45, por que o passageiro deveria confiar no seu app em vez de simplesmente olhar o GPS do Cittamobi ou do Google Maps?"

**o que eu mudei por causa dela:** Eu percebi que não adiantava ter a melhor rede neural se no momento mais crítico (um engarrafamento na rodovia) o passageiro recebesse uma previsão furada. Por causa dessa pergunta, eu criei no código a **trava híbrida de segurança**: quando a divergência entre a STGCN e o GPS do ônibus passa de 15 minutos, o app não esconde o problema; ele acende o selo amarelo `[?]` e avisa no fone por voz que a rodovia travou. Coloquei o botão dessa demonstração direto na tela do app (Slide 3) para mostrar na frente da banca como a regra protege o passageiro da falha da IA.
