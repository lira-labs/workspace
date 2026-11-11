# sem2 · Cauã da Cunha Lira

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), feito a partir do
> [tec.md](tec.md), do [flx.md](flx.md), do [exp.md](exp.md) e do [sem1.md](sem1.md).
> código no painel: `sem2` · quarta, 11/11.

**link dos slides:** [va2/slides_sem2.html](https://grafoparadaweb.vercel.app/slides_sem2.html) e [va2/GrafoParada_Seminario2_CauaLira.pptx](https://grafoparadaweb.vercel.app/GrafoParada_Seminario2_CauaLira.pptx)

**a versão que roda:** commit [`0cdf397`](https://github.com/lira-labs/workspace/commit/0cdf397) no repositório [github.com/lira-labs/workspace](https://github.com/lira-labs/workspace)

**a máquina:** meu notebook com Python 3.12 e o smartphone conectado ao vivo pelo link [grafoparadaweb.vercel.app](https://grafoparadaweb.vercel.app), espelhado na sala.

**a gravação de reserva:** [va2/entrega_ai4good.mp4](https://github.com/lira-labs/workspace/blob/main/va2/entrega_ai4good.mp4), tomada contínua do ensaio sem cortes, anexada à release `sem2`.

## as quatro frases, sem IA

1. **a demo:** O estudante ou trabalhador no Grande Recife abre o app, consulta qualquer uma das 400 linhas reais do GTFS (como a Linha 522 da UFRPE ou a Linha 060), vê a previsão em 4 minutos e sai de casa no horário certo sem mofar no ponto de ônibus.
2. **o custo:** No celular levou 4,98 milissegundos e 12 KB de RAM; no servidor a STGCN levou 0,77 milissegundo e 358 MB no processo PyTorch na CPU. A estimativa inicial de arquitetura previa menos de 500 ms e 300 MB, e a diferença é que a CPU calculou muito mais rápido e o runtime segura bibliotecas no SO.
3. **a falha:** Num choque súbito com 45 minutos de retenção simulada na via, a STGCN previu 18 minutos porque suavizou o atraso pelo grafo. Quem sofre é o passageiro que perde a prova ou o turno, e o erro ensina que choques pontuais exigem uma trava híbrida que corte a IA.
4. **o que mudou:** No sem1 uma conta simples bateu a rede em 5 paradas e eu ia descartar a STGCN; mantive a STGCN para testar em escala: na malha expandida de 20 paradas, em dados simulados por difusão espaço-temporal, a STGCN obteve 1,51 minuto de erro contra 1,93 minuto da regressão linear e 7,13 da persistência, mostrando que o grafo mitiga a explosão dimensional quando a rede cresce.

## slide 1 · ponta a ponta · 80 s

- **aparece:** Na esquerda: Quem usa (Estudante/trabalhador no Grande Recife), Entrada real (Linha 522 Dois Irmãos / UFRPE e 400 linhas reais do GTFS CTM), Saída na tela (chegada em 4 min, assentos livres e voz) e O que deixa fazer (sair às 06h09 sem mofar no ponto). Na direita: O card da demonstração ao vivo rodando direto do repositório.
- **a entrada:** Usuário na parada da UFRPE ou de qualquer corredor metropolitano, consultando linhas reais do GTFS e satélite Cittamobi ao vivo.
- **eu falo:** "Esse é o GrafoParada rodando ao vivo do repositório. Aqui está o celular espelhado na tela: o passageiro ou estudante aqui na UFRPE precisa ir para o Derby ou Centro. Ele abre o app e tem na mão as 400 linhas reais do Grande Recife com traçado oficial e paradas do GTFS. A tela entrega a previsão exata da Linha 522: 4 minutos para chegar, na Plataforma 01, com assento garantido. Ele vê que deve sair às 06h09 para caminhar com calma e não ficar mofando no ponto escuro. Se ele pesquisar a Linha 060, a 2040 da CDU ou qualquer terminal do SEI, a rede carrega na hora com telemetria do Cittamobi. A previsão sai rápida, direto no aparelho, sem depender de carregar páginas pesadas."

## slide 2 · quanto custa · 50 s

- **aparece:** Três colunas limpas: 4,98 ms e 12 KB no celular (on-device); 0,77 ms e 358 MB no servidor (CPU pura); e R$ 0,00 de custo financeiro local ao lado da estimativa inicial (< 500 ms e ~300 MB).
- **medido:** Execução de `medir_custo_sem2.py`: FSM cinemática em 4,98 ms e 12 KB de RAM no dispositivo; STGCN em 0,77 ms de CPU e 358 MB de processo PyTorch no servidor local (Core i7 / Python 3.12).
- **estimado no projeto:** < 500 ms por inferência e ~300 MB de memória RAM.
- **eu falo:** "Esses números vieram da medição que rodou no repositório. No celular, o cálculo cinemático levou 4,98 milissegundos e gastou apenas 12 kilobytes de RAM, sem consumir bateria. No servidor local, a STGCN rodou em 0,77 milissegundo na CPU. A estimativa inicial previa até 500 milissegundos e 300 megabytes. A diferença no tempo é que a inferência em CPU pura é centenas de vezes mais rápida do que o teto estimado; e na memória, os 358 megabytes são o processo do PyTorch mantendo as bibliotecas dinâmicas carregadas, enquanto os tensores da rede ocupam menos de 100 kilobytes. O custo no ambiente de desenvolvimento é zero; para escala metropolitana, o dimensionamento prevê instâncias em contêiner com inferência a cada ciclo."

## slide 3 · a falha · 60 s

- **aparece:** A saída da IA sob super-suavização em destaque vermelho: 18 min. A retenção de referência do choque em destaque verde: 45 min. Embaixo: quem sofre o erro e a trava de segurança adotada.
- **a entrada:** Simulação de retenção severa ou bloqueio físico da via, com atraso de referência de 45 minutos no trecho.
- **a saída, como saiu:** A STGCN previu 18 minutos.
- **o valor de referência:** 45 minutos de retenção abrupta.
- **eu falo:** "Eu escolhi este caso de propósito porque ele erra de verdade. Simulamos uma retenção severa por bloqueio de pista onde o atraso de referência saltou para 45 minutos. Olhem a tela: a STGCN previu apenas 18 minutos. O número parece razoável, mas mente. Quem sofre é o trabalhador ou estudante: ele confia no '18 minutos', espera um ônibus que não vem e perde o turno ou a prova na universidade. O erro me ensinou que redes de grafo sofrem de super-suavização: a matriz do grafo dilui o atraso brusco com as paradas vizinhas desimpedidas. Por isso colocamos a trava híbrida: se o desvio entre a STGCN e a telemetria passar de 15 minutos, o app corta a IA e acende o alerta de interdição [?]. É exatamente essa falha que vamos medir no sem3."

## slide 4 · o que mudou desde o sem1 · 45 s

- **aparece:** Duas linhas claras. "No sem1 (5 paradas): O cálculo linear simples bateu a STGCN (2,46 min vs 4,42 min)." e "Agora no sem2 (malha GTFS expandida · 20 paradas): A STGCN obteve 1,51 min (contra 1,93 min da linear e 7,13 min da persistência) em dados sintéticos de difusão."
- **no sem1:** O cálculo simples bateu a STGCN em 5 paradas (2,46 min vs 4,42 min), e a banca questionou se valia a pena gastar memória com IA em grafo.
- **agora:** Mantive a STGCN de propósito para testar a escala. Na malha de 20 paradas, em simulação de difusão por grafo, a STGCN venceu a linear por 0,42 min e reduziu 78% do erro contra a persistência.
- **eu falo:** "No sem1, uma conta simples tinha errado menos que a STGCN num trecho curto de 5 paradas: 2,46 contra 4,42 minutos. Eu prometi testar na malha completa para ver se a rede se justificava. Mantive a STGCN e hoje trago a resposta: na malha expandida com 20 paradas da PE-60, em dados simulados por difusão espaço-temporal, a STGCN virou o jogo. O erro caiu para 1,51 minuto, superando a regressão linear que deu 1,93 minuto e a persistência de 7,13 minutos. A regressão tabular sofre ao tentar calibrar 120 variáveis achatadas, enquanto o grafo preserva a esparsidade da via. Como os dados de atraso foram gerados por difusão sintética, a validação final em campo dependerá da abertura de telemetria contínua pelo consórcio."

## slide 5 · o fecho · 25 s

- **aparece:** O fecho do sem2: "Roda no celular e na CPU local a custo zero, e a falha de over-smoothing é blindada pela regra." Embaixo, a ponte pro sem3: "Seminário 3 (25/11): Quantos choques de trânsito na malha a trava híbrida consegue capturar contra o erro puro da IA."
- **eu falo:** "O sistema roda no aparelho do passageiro e na CPU local a custo zero, com dados reais do Grande Recife. E a falha da IA não fica escondida: vira a regra de segurança que protege o passageiro. No dia 25, no sem3, eu trago a medida formal de quantos desses choques a trava consegue capturar."

**tempo total, cronometrado, com a demo rodando:** 4 min 10 s e 4 min 05 s, duas vezes seguidas, na mesma máquina. A segunda passada está gravada sem cortes como reserva.

## ensaio cético · as 4 perguntas decisivas da banca

> 💡 **Postura Mestra da Defesa:** *"A infraestrutura espacial é real. O experimento preditivo atual é sintético. Os resultados demonstram a viabilidade metodológica, não uma validação definitiva do trânsito real do Grande Recife."*

| Componente | Origem |
| :--- | :--- |
| Paradas, linhas e trajetos | GTFS oficial do Grande Recife (393 linhas, 15.239 paradas) |
| Horários programados | GTFS oficial (`stop_times.txt`) |
| Atrasos e retenções de treino | Dados sintéticos (difusão espaço-temporal via Laplaciana) |
| Demanda latente do exemplo | Estimativa ilustrativa do protótipo (IC 90%) |
| Telemetria contínua real | Não disponível publicamente pelo consórcio |

### 1. "Se os dados são sintéticos, por que a ST-GCN venceu a regressão linear?"
**Resposta:** "A ST-GCN venceu porque resolve a maldição da dimensionalidade. Em 5 paradas (Sem1), uma reta simples tinha poucas variáveis e aprendeu com facilidade. Ao expandir para 20 paradas no Sem2 com 6 lags temporais, na representação tabular o modelo recebe 120 variáveis de entrada (features) — 20 paradas por 6 defasagens temporais — e precisa aprender suas relações em uma estrutura achatada e altamente colinear. A ST-GCN, por sua vez, compartilha pesos espaciais via convolução espectral de Chebyshev sobre a topologia física da rodovia. Reconheço, contudo, que parte dessa vantagem advém da hipótese de difusão em rede utilizada no gerador sintético, o que reforça que o resultado demonstra eficiência estrutural do grafo, mas não substitui a validação de campo."

### 2. "Como você validaria esse modelo com dados reais?"
**Resposta:** "A validação real requer um convênio de pesquisa operacional com o CTM Grande Recife ou uma das concessionárias operadoras para acesso ao streaming de telemetria AVL/GPS dos transponders da frota e aos logs com timestamp e validador da bilhetagem eletrônica (VEM). Com esse fluxo, mapearíamos o histórico real de tempos entre paradas consecutivas, separaríamos os dados por divisão temporal estrita (ex: 4 semanas de treino, 1 semana de teste) e testaríamos a capacidade preditiva da ST-GCN sem depender de gerador sintético."

### 3. "De onde vem a demanda latente da Central CTM?"
**Resposta:** "A bilhetagem eletrônica da catraca registra apenas a demanda atendida e censurada: quem desiste na parada escura ou desiste da espera por superlotação não passa na catraca e vira invisível para o CTM. A demanda latente no GrafoParada é modelada combinando três fontes: (1) a série histórica censurada da catraca; (2) a declaração voluntária de rotina pendular no app pelo passageiro (amostragem on-device); e (3) a propagação espaço-temporal estimada pela ST-GCN ao longo dos nós adjacentes da malha. O modelo produz uma estimativa pontual da demanda, e a incerteza é calibrada (via calibração conformal) para gerar um intervalo de 90% usado na decisão operacional."

### 4. "O que exatamente o projeto consegue afirmar hoje e o que ainda é hipótese?"
**Resposta:** "O que afirmamos com dados concretos hoje: (1) Que é viável processar a malha metropolitana oficial inteira do Grande Recife (393 linhas, 15.239 paradas) com inferência ultrarrápida (0,77 ms na CPU e 4,98 ms on-device); (2) Que convoluções espaciais em grafo sofrem de super-suavização (over-smoothing) em choques bruscos de trânsito, exigindo obrigatoriamente uma trava híbrida que corte a IA se o desvio ultrapassar 15 min; (3) Que a formulação de despacho deve ser probabilística, baseada em P(Demanda > Capacidade). O que ainda é hipótese: A magnitude exata da redução do erro de previsão em tráfego metropolitano real, que depende do acesso a dados contínuos de GPS da frota."
