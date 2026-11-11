# sem2 · Cauã da Cunha Lira

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), feito a partir do
> [tec.md](tec.md), do [flx.md](flx.md), do [exp.md](exp.md) e do [sem1.md](sem1.md).
> código no painel: `sem2` · quarta, 11/11.

**link dos slides:** [va2/slides_sem2.html](https://grafoparadaweb.vercel.app/slides_sem2.html) e [va2/GrafoParada_Seminario2_CauaLira.pptx](https://grafoparadaweb.vercel.app/GrafoParada_Seminario2_CauaLira.pptx)

**a versão que roda:** commit [`0cdf397`](https://github.com/lira-labs/workspace/commit/0cdf397) no repositório [github.com/lira-labs/workspace](https://github.com/lira-labs/workspace)

**a máquina:** meu notebook com Python 3.12 e o smartphone conectado ao vivo pelo link [grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app), espelhado na sala.

**a gravação de reserva:** [va2/entrega_ai4good.mp4](https://github.com/lira-labs/workspace/blob/main/va2/entrega_ai4good.mp4), tomada contínua do ensaio sem cortes, anexada à release `sem2`.

## as quatro frases, sem IA

1. **a demo:** O passageiro em Camela abre o app às 06h10, vê a previsão da Linha 199 chegando em 4 minutos e a indicação de sair às 06h08 para não mofar no acostamento escuro da PE-60.
2. **o custo:** No celular levou 4,98 milissegundos e 12 KB de RAM; no servidor a STGCN levou 0,77 milissegundo e 358 MB no processo PyTorch. O flx estimava menos de 500 ms e 300 MB, e a diferença é que a CPU calculou muito mais rápido e o runtime segura bibliotecas no SO.
3. **a falha:** No bloqueio do Trevo de Ipojuca com 45 minutos de atraso real no GPS, a STGCN previu 18 minutos porque suavizou o atraso pelo grafo. Quem sofre é o passageiro que perde o turno na fábrica, e o erro ensina que choques pontuais exigem uma trava que corte a IA.
4. **o que mudou:** No sem1 uma conta simples bateu a rede em 5 paradas e eu ia descartar a STGCN; mantive a STGCN porque na malha real de 20 paradas da PE-60 ela virou o jogo com 1,51 minuto de erro contra 1,93 minuto, provando que malha grande exige grafo.

## slide 1 · ponta a ponta · 80 s

- **aparece:** Na esquerda: Quem usa (passageiro em Camela), Entrada real (Linha 199 às 06h10), Saída na tela (chegada em 4 min) e O que deixa fazer (sair no horário certo sem mofar no ponto escuro). Na direita: O card da demonstração ao vivo rodando direto do repositório.
- **a entrada:** Passageiro na parada de Camela na rodovia PE-60, às 06h10, aguardando a Linha 199 sentido TI Cabo.
- **eu falo:** "Esse é o GrafoParada rodando ao vivo do repositório. Aqui está o celular espelhado na tela: o passageiro em Camela precisa ir trabalhar em Suape. Às 06h10 ele abre o app. A tela entrega a previsão exata da Linha 199: 4 minutos para chegar, na Plataforma 04. Ele vê que deve sair de casa às 06h08 para caminhar com calma e não ficar mofando no acostamento escuro e perigoso da rodovia. A previsão sai rápida, direto no celular, sem depender de carregar páginas pesadas."

## slide 2 · quanto custa · 50 s

- **aparece:** Medido nesta máquina: 4,98 ms e 12 KB no celular; 0,77 ms e 358 MB no servidor. Ao lado, o estimado no flx: < 500 ms e ~300 MB. Embaixo: a explicação da diferença.
- **medido:** Execução de `medir_custo_sem2.py` no commit `0cdf397`: FSM cinemática em 4,98 ms e 12 KB de RAM no celular; STGCN em 0,77 ms de CPU e 358 MB de processo PyTorch no servidor.
- **estimado no flx:** < 500 ms por inferência e ~300 MB de memória RAM.
- **eu falo:** "Esses números vieram da medição de verdade que rodou no repositório. No celular, o cálculo cinemático levou 4,98 milissegundos e gastou apenas 12 kilobytes de RAM. No servidor, a STGCN rodou em 0,77 milissegundo na CPU. O flx estimava até 500 milissegundos e 300 megabytes. A diferença no tempo é que a inferência em CPU pura é quase instantânea; e na memória, os 358 megabytes são o processo do PyTorch mantendo as bibliotecas dinâmicas em memória, enquanto os pesos da rede ocupam menos de 100 kilobytes. O custo em reais é zero: roda num computador comum de escritório do consórcio."

## slide 3 · a falha · 60 s

- **aparece:** A saída errada da IA em destaque vermelho: 18 minutos. O certo pelo GPS em destaque verde: 45 minutos. Embaixo: quem sofre o erro e a trava de proteção adotada.
- **a entrada:** Ônibus da Linha 199 travado no bloqueio do Trevo de Ipojuca (Nó 10 da PE-60), com atraso real de 45 minutos no satélite GPS.
- **a saída, como saiu:** A STGCN previu 18 minutos.
- **o certo:** 45 minutos de atraso (ou alerta de interdição total da rodovia).
- **eu falo:** "Eu escolhi este caso de propósito porque ele erra de verdade. Teve um acidente no Trevo de Ipojuca e a rodovia travou: o atraso real no GPS pulou para 45 minutos. Olhem a tela: a STGCN previu 18 minutos. O número parece razoável, mas mente. Quem sofre é o trabalhador na parada: ele confia no '18 minutos', espera um ônibus que não vem e perde o turno na fábrica. O erro me ensinou que redes de grafo sofrem de super-suavização: a matriz do grafo dilui o atraso brusco com as paradas vizinhas. Por isso colocamos a trava híbrida: se o desvio entre STGCN e GPS passar de 15 minutos, o app corta a IA e acende o alerta de interdição [?]. É exatamente essa falha que vamos medir no sem3."

## slide 4 · o que mudou desde o sem1 · 45 s

- **aparece:** Duas linhas claras. "No sem1 (5 paradas): O cálculo linear simples bateu a STGCN (2,46 min vs 4,42 min)." e "Agora no sem2 (20 paradas PE-60): A STGCN virou o jogo e reduziu o erro para 1,51 min (contra 1,93 min da linear e 7,13 min da persistência)."
- **no sem1:** O cálculo simples bateu a STGCN em 5 paradas (2,46 min vs 4,42 min), e a banca questionou se valia a pena usar IA em grafo.
- **agora:** Mantive a STGCN de propósito. Na malha de 20 paradas da PE-60, a STGCN venceu a linear por 0,42 min e reduziu 78% do erro contra a persistência.
- **eu falo:** "No sem1, uma conta simples de padaria tinha errado menos que a STGCN num trecho curto de 5 paradas: 2,46 contra 4,42 minutos. Eu prometi testar na malha completa para ver se a rede se justificava. Mantive a STGCN e hoje trago a resposta: nas 20 paradas da rodovia PE-60, a STGCN virou o jogo. O erro caiu para 1,51 minuto, superando a regressão linear que deu 1,93 minuto e a persistência de 7,13 minutos. Quando o corredor cresce e os atrasos se propagam entre as paradas, a IA espacial se paga."

## slide 5 · o fecho · 25 s

- **aparece:** O fecho do sem2: "Roda no celular e na CPU local a custo zero, e a falha de over-smoothing é blindada pela regra." Embaixo, a ponte pro sem3: "Seminário 3 (25/11): Quantos choques de trânsito na PE-60 a trava híbrida consegue capturar contra o erro puro da IA."
- **eu falo:** "O sistema roda no aparelho do passageiro e na CPU local a custo zero. E a falha da IA não fica escondida: vira a regra de segurança que protege o trabalhador. No dia 25, no sem3, eu trago a medida de campo de quantos desses choques a trava consegue capturar."

**tempo total, cronometrado, com a demo rodando:** 4 min 10 s e 4 min 05 s, duas vezes seguidas, na mesma máquina. A segunda passada está gravada sem cortes como reserva.

## ensaio cético

**a pergunta mais difícil:** "Se a STGCN erra feio num acidente prevendo 18 minutos em vez de 45, por que o passageiro deveria confiar no seu app?"

**o que eu mudei por causa dela:** Eu ia tentar defender que a IA aprende com o tempo. Mudei: assumi que o over-smoothing é intrínseco à convolução em grafo e criei a trava híbrida de segurança no código. Se a diferença entre IA e GPS passa de 15 minutos, a tela corta a previsão e acende o selo [?] de interdição.
