# sem1 · Cauã da Cunha Lira

> roteiro do [seminário · preliminares](../4-seminario-preliminares.md). de 4 a 6 slides, de 3 a 5
> minutos. em cada slide: o que aparece, o que você fala, e quanto tempo leva.

**link dos slides:** [va2/slides_sem1.html](https://github.com/lira-labs/workspace/blob/main/va2/slides_sem1.html) (apresentação HTML interativa no repositório)

## as quatro frases, sem IA

1. **a ideia:** A demora faz o trabalhador acordar muito mais cedo e continuar chegando tarde, porque muitas opções de ônibus só passam de uma em uma hora e, quando atrasam, transportes alternativos como kombis, ligeirinhos, moto-táxis e Uber levam os passageiros; o GrafoParada quer mostrar para as empresas de ônibus que elas não ficaram sem passageiros, elas negligenciaram o trabalhador.
2. **o produto mais próximo:** No Cittamobi e outros apps, a gente tem todo aquele lance de puxar o celular no meio da rua com chance de ser assaltado, procurar a parada e às vezes a linha ou o rastreador nem aparecerem: ele só mede o tempo do ônibus, em nada ajuda o passageiro quando ele desiste.
3. **o artigo mais próximo:** A pesquisa de Wang et al. (2022), na *Transportation Research Part C*, é o máximo por usar buscas no celular para prever passageiros de ônibus, mas estamos no Brasil: a catraca mente, porque ela não conta a negligência das empresas que acham normal o ônibus das 6h chegar às 6h30 e esconde quem desistiu na parada.
4. **o que só a minha faz:** O GrafoParada é diferente porque aprende a sua rotina diária de trabalho para avisar por voz no fone quantos minutos faltam sem precisar puxar o celular na rua e mostra quais horários vazios podem ser redistribuídos para a população; e responde à pergunta científica: cruzar os dados do celular com as paradas anteriores consegue alertar atrasos críticos a tempo, e uma rede neural complexa (STGCN) supera um modelo simples nisso? (No nosso piloto, o alerta zerou os atrasos não avisados de 28% para 0%, mas, no corredor curto de 5 paradas, o cálculo mais simples superou a rede neural complexa).

## slide 1 · a ideia · 50 s

- **aparece:** `"A catraca mente." Quem desiste na parada vira invisível.` Três cartões visuais: `50+ min` (ônibus atrasa na PE-60 → kombi, ligeirinho, moto-táxi) → `0 na catraca` (empresa acha que a parada estava vazia e corta horários) → `GrafoParada` (aprende a rotina no aparelho + cruza desistência com GPS aberto da frota vazia).
- **eu falo:** "A demora faz o trabalhador acordar muito mais cedo e continuar chegando tarde. Aqui no Grande Recife, como lá em Ipojuca e na PE-60, muitas opções de ônibus só passam de uma em uma hora. Quando a pessoa vê que o ônibus vai demorar 50 minutos, ela pega os transportes alternativos: kombi, ligeirinho, moto-táxi ou até um Uber quando a grana não tá curta. Como esse trabalhador não passou na catraca, a empresa olha o relatório vazio e corta ainda mais horários. O GrafoParada mostra para as empresas que elas não ficaram sem passageiros — elas negligenciaram o trabalhador — e aponta de qual linha rodando vazia dá para puxar um ônibus para cobrir esse horário de pico."

## slide 2 · o produto mais próximo · 50 s

- **aparece:** `Cittamobi mostra o atraso, mas esquece quem desistiu.` Quadro comparativo direto entre o app oficial usado no Grande Recife ([cittamobi.com.br](https://www.cittamobi.com.br)) e o GrafoParada nos 4 critérios de rua (GPS do ônibus, risco de puxar o celular na parada, registro de desistência para ligeirinho/moto-táxi e remanejamento de frota vazia).
- **eu falo:** "O produto que chega mais perto hoje aqui no Grande Recife é o Cittamobi, junto com o modo GO do Transit lá fora. Ele é bom porque já está em mais de 330 cidades mostrando o GPS do ônibus. Mas no Cittamobi a gente tem todo aquele lance de puxar o celular no meio da rua, procurar a parada, às vezes o rastreador nem aparece, correndo risco de ser assaltado distraído olhando a tela. Pior: ele só mede o tempo do ônibus. Se o trabalhador vê que vai demorar uma hora, fecha o app e pega um moto-táxi, o Cittamobi esquece que aquela pessoa existiu e não avisa nada para reorganizar a frota."

## slide 3 · o artigo mais próximo · 50 s

- **aparece:** `"Short-term bus passenger flow prediction using trip planner request data"` · Z. Wang et al. · *Transportation Research Part C: Emerging Technologies* (2022, Qualis A1) · [doi.org/10.1016/j.trc.2022.103790](https://doi.org/10.1016/j.trc.2022.103790), destacando `-21,7% de erro` com buscas de app vs. o limite de treinar apenas na catraca física.
- **eu falo:** "Na ciência, quem chegou mais perto foi o grupo de Wang et al., em 2022, na *Transportation Research Part C*. Eles usaram as buscas que os passageiros fazem no aplicativo de rota para prever quantos passageiros iam embarcar, e provaram que isso reduz o erro em até 21,7%. Essa pesquisa é o máximo, mas estamos no Brasil, onde o transporte não é de qualidade. Eles treinaram o modelo deles olhando só para a catraca física. E aqui a catraca mente: ela não conta a negligência das empresas que acham tudo bem o ônibus das 6h chegar às 6h30, deixando de fora todo mundo que desistiu no ponto."

## slide 4 · o que só a minha faz · 65 s

- **aparece:** `O sinal do celular zerou gargalos sem aviso, e na linha reta a conta simples bateu a GNN.` Três números medidos no piloto (`exp.md`): `28% → 0%` de gargalos sem aviso com o *z-score* do celular; `2,46 min vs. 4,42 min` (cálculo simples no corredor de 5 paradas vs. STGCN); e `20% → 97%` de decisões certas na tela com aviso `[?]` e GPS bruto.
- **eu falo:** "O diferencial do GrafoParada é que ele aprende a sua rotina diária direto no seu aparelho — sem mandar seu histórico pessoal para banco de dados, apagando o IP da janela de 10 minutos na memória RAM — e te avisa por voz no fone quantos minutos faltam sem você puxar o celular na rua. Se você sai da parada em velocidade de veículo antes do GPS do ônibus chegar, ele conta a desistência e mostra ao consórcio qual horário ocioso remanejar. A nossa pergunta científica foi: cruzar os dados do celular com as paradas anteriores consegue alertar atrasos críticos a tempo, e uma rede neural complexa (STGCN) supera um modelo simples nisso? No piloto, o alerta do celular funcionou perfeitamente, derrubando os atrasos não avisados de 28% para 0%. Mas tivemos um achado honesto: num corredor curto em linha reta de 5 paradas, o cálculo mais simples (olhando P1, P2 e P3) errou menos que a STGCN — 2,46 contra 4,42 minutos. Por isso usamos a conta simples na linha reta e deixamos a STGCN para os Terminais Integrados onde várias linhas se cruzam."

## slide 5 (opcional) · fecho · 20 s

- **aparece:** `Não falta passageiro na parada. Falta enxergar quem desistiu antes da catraca.` Dois blocos finais: `No Bolso` (rotina no aparelho + voz no fone) e `Na Rede` (conta simples na linha reta · STGCN nos Terminais · parada do ônibus no GPS $\ge 15\text{ s}$ protege quem não tem celular).
- **eu falo:** "E mesmo onde a população é mais humilde ou idosa e não usa aplicativo, o sistema nunca tira ônibus no escuro: se o GPS público do ônibus mostrar que ele parou 15 segundos na parada, o sistema sabe que tem gente subindo. A nossa luta é fazer com que os dados enxerguem o trabalhador antes da catraca."

**tempo total, cronometrado:** 3 min 55 s (primeira tomada em voz alta) e 3 min 45 s (segunda tomada).

## ensaio cético

**a pergunta mais difícil:** "No seu piloto você viu que, num corredor curto de 5 paradas, um cálculo simples errou menos que a sua rede neural de grafos (STGCN): 2,46 minutos contra 4,42 minutos. Então por que você não joga a STGCN fora de vez?"

**o que eu mudei por causa dela:** na primeira vez eu travei e não soube responder por que manter a STGCN se a conta simples tinha ganhado no piloto. por causa dessa pergunta, mudei o Slide 4 e o Slide 5 para mostrar abertamente o `2,46 min vs. 4,42 min` e explicar a diferença prática: em uma linha reta curta de 5 paradas (uma fila indiana P1 → P2 → P3), a conta simples olhando as paradas anteriores resolve melhor; já a rede em grafo (STGCN) fica reservada para os Terminais Integrados (como TI Cabo e TI Barro), onde várias linhas diferentes se cruzam como uma teia e o atraso de uma linha trava as outras.
