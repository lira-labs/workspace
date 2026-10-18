# brw · Cauã da Cunha Lira

> folha do artefato [brainwriting híbrido](../3-brainwriting-hibrido.md). siga o guia passo a passo
> e preencha cada seção aqui. as decisões são suas, e decidir é saber explicar.

## 1 · onde atacar

**crise** (marque 1 com `x`):

| | crise |
|:-:|:--|
| [ ] | perda do raciocínio crítico e alienação (*slop*) |
| [ ] | a verdade sob mira e colapso epistêmico (*fakes*) |
| [ ] | manipulação política e democracia (*bots*) |
| [ ] | crise ecológica da IA (água e energia) |
| [ ] | alimentação com veneno e ultraprocessados (vs. feiras agroecológicas) |
| [ ] | endividamento e dreno das *bets* |
| [ ] | moradia e especulação (casas vazias) |
| [ ] | concentração de plataformas e trabalho |
| [x] | outra: apagão da demanda reprimida e má distribuição de frota no transporte público urbano (o "paradoxo da catraca" que condena linhas a intervalos de 1 em 1 hora) |

por que esta crise: onde o ônibus demora uma hora para passar, muita gente desiste na parada e busca transporte alternativo; como o sistema mede demanda quase só pelo giro da catraca, interpreta o ponto vazio como falta de passageiro e corta ainda mais horários, fazendo o Brasil perder 19,1 milhões de viagens pagantes por dia na última década (NTU) num setor que custa R$ 75,7 bilhões ao ano.

**tecnologias de IA** (marque 3 e chame de A, B, C):

| | tecnologia de IA |
|:-:|:--|
| [x] C | modelos locais / no aparelho (*SLMs*, 1B–7B) |
| [x] B | sistemas multiagente e agência (*tools*, MCP) |
| [ ] | visão computacional e OCR |
| [ ] | voz (fala ↔ texto) e interfaces sem tela |
| [x] A | grafos e RAG (redes de grafos, busca vetorial) |
| [ ] | modelos de difusão / geração visual |
| [ ] | outra: |

**infraestruturas tradicionais** (marque 3 e chame de 1, 2, 3):

| | infraestrutura |
|:-:|:--|
| [x] 3 | plataformas de dois lados (*matching*, como Uber) |
| [x] 1 | geolocalização, GPS e mapas |
| [ ] | e-commerce, marketplaces e catálogos |
| [ ] | mensageria leve e bots (WhatsApp, SMS) |
| [ ] | redes sociais, feeds e comunidades |
| [ ] | pagamento instantâneo (Pix, moeda local) |
| [x] 2 | crowdsourcing e curadoria coletiva |
| [ ] | outra: |

## 2 · clichês

| clichê | o que acerta | onde fica raso |
|:--|:--|:--|
| app de horário de ônibus (Cittamobi, Moovit) | mostra no mapa onde o veículo está e ajuda o passageiro a decidir se espera. | trata a consulta como leitura passiva; se o ônibus vai demorar 50 minutos e a pessoa fecha o app e desiste, essa demanda perdida desaparece sem gerar registro. |
| planejamento de frota pela bilhetagem eletrônica (catraca) | contabiliza com precisão quem conseguiu embarcar e pagar passagem. | confunde oferta com demanda total: ignora quem desistiu na parada por falta de ônibus ou porque o veículo passou lotado. |
| pesquisa Origem-Destino (OD) por formulário | levanta deslocamentos desejados fora do que a catraca registra. | custa caro, leva anos para atualizar e depende da boa vontade de responder questionários longos, nascendo defasada. |
| ouvidoria e chatbot de reclamação de linhas | abre um canal formal para registrar queixas sobre atrasos e superlotação. | exige trabalho extra de quem já perdeu o ônibus; reclamações textuais avulsas não formam uma matriz espaço-temporal para recalcular a tabela horária. |
| painel gerencial de GPS das empresas | fiscaliza se a frota cumpriu as viagens programadas na tabela oficial. | audita apenas se o quadro horário atual foi cumprido, sem enxergar se a própria tabela está subdimensionada naquele bairro ou rodando vazia em outro. |

## 3 · matriz 3 × 3 e a minha ideia

cada célula: **nome** · frase de até 20 palavras (quem usa, o que faz).

| | 1 · geolocalização, GPS e mapas | 2 · crowdsourcing e curadoria coletiva | 3 · plataformas de dois lados (*matching*) |
|:--|:--|:--|:--|
| **A · grafos e RAG** | **GrafoParada** · passageiros abrem paradas no mapa com GPS ativo; rede de grafos cruza buscas e frota para medir demanda reprimida. | **MapaLotação** · usuários sinalizam paradas cheias; rede de grafos propaga alertas de superlotação para paradas seguintes da mesma linha. | **RotaElástica** · grafo identifica corredores desassistidos no mapa e conecta grupos de passageiros a viagens extras sob demanda. |
| **B · sistemas multiagente** | **DespachoVivo** · agentes monitoram distância entre ônibus no GPS e buscas nas paradas, sugerindo ajustes de intervalo aos operadores. | **FiscalColetivo** · agentes cruzam relatos nas paradas com o GPS oficial das linhas e geram dossiês públicos de viagens fantasma. | **PonteModal** · agentes negociam integração automática entre passageiros esperando em paradas sem ônibus e motoristas de transporte complementar. |
| **C · modelos locais (*SLMs*)** | **SentinelaPonto** · modelo local no celular detecta pelo deslocamento se quem abriu a parada embarcou ou desistiu após longa espera. | **VozDaParada** · modelo no aparelho resume relatos rápidos de espera na fila sem expor a trajetória individual do passageiro. | **IntegraFácil** · assistente local calcula se vale esperar o ônibus ou dividir corrida curta até um terminal troncal próximo. |

**as 9 no mapa impacto × viabilidade:**

| | viabilidade alta | viabilidade baixa |
|:--|:--|:--|
| **impacto alto** | **GrafoParada** — ataca a cegueira da catraca usando o ato habitual de checar o ponto no mapa com localização ativa; é testável num recorte com dados públicos de GTFS/GPS.<br>**SentinelaPonto** — separa quem embarcou de quem desistiu na parada sem exigir relato manual; cabe num protótipo delimitável no semestre. | **DespachoVivo** — pode reduzir o intervalo real nas paradas críticas, mas alterar despacho ao vivo exige integração operacional com garagens e consórcios.<br>**RotaElástica** — pode atender bairros com intervalos de 1 hora, mas exige frota flexível e autorização regulatória para rotas dinâmicas.<br>**PonteModal** — pode suprir buracos de horário com vans e carros, mas exige reunir os dois lados e regras tarifárias integradas. |
| **impacto baixo** | **MapaLotação** — avisa que o ônibus vem cheio, mas sozinho não altera a oferta de horários da linha.<br>**FiscalColetivo** — comprova atrasos e viagens não cumpridas, mas foca em punição posterior sem redesenhar a malha.<br>**VozDaParada** — organiza queixas coletivas com privacidade, mas ainda depende de engajamento ativo do passageiro. | **IntegraFácil** — ajuda na decisão individual de abandonar o ponto, mas acelera a fuga do ônibus em vez de corrigir a distribuição da frota. |

onde discordei da IA, e por quê: a IA colocou o **GrafoParada** em viabilidade alta assumindo integração imediata com toda a base comercial de apps como Cittamobi ou Moovit numa metrópole inteira. mantive em viabilidade alta apenas porque reduzi o escopo do semestre: consigo testar o grafo sobre dados abertos de GTFS e GPS combinados com abertura de paradas com localização ativa num corredor delimitado. isso valida a estimação de demanda reprimida e ociosidade frente a regras simples, mas não comprova ainda a adoção por todos os consórcios da cidade.

**minha ideia escolhida:** **GrafoParada** · passageiros abrem paradas no mapa com GPS ativo; rede de grafos cruza buscas e frota para medir demanda reprimida.

**por que ela, sem IA, em até 3 linhas:**
escolho o GrafoParada porque o passageiro já abre o mapa da parada com a localização ligada para saber se o ônibus está perto ou se vai demorar uma hora.  
aproveitar esse gesto evita formulários de reclamação e registra quem esteve no ponto e desistiu antes de passar na catraca.  
com isso, é possível provar onde faltam horários e onde sobram ônibus vazios usando o próprio comportamento de consulta.

## 4 · motores

| motor | nome | frase | o que mudou em relação à ideia |
|:--|:--|:--|:--|
| inverter | **frota no vazio** | mapa expõe onde ônibus rodam vazios enquanto paradas de linhas vizinhas acumulam espera e desistência. | em vez de só apontar falta de ônibus num ponto, o grafo contrasta a parada estrangulada com os trechos de sobreoferta para propor realocação da frota existente. |
| canalizar | **clique que vota** | ao abrir a parada com localização ativa para ver o horário, o passageiro já alimenta a fila virtual da linha. | o interesse imediato de checar quanto falta para o ônibus chegar gera o sinal coletivo de demanda reprimida sem nenhum botão de denúncia ou cadastro extra. |
| transplantar | **pressão de ponto** | como o mapa de calor dinâmico de apps de corrida, paradas mudam de cor conforme o saldo entre espera e oferta. | traz o mecanismo de pressão dinâmica de plataformas de corrida para priorizar ajustes de tabela nos pontos onde a espera estoura. |
| reescalar | **pulso do corredor** | em vez de olhar uma parada isolada, o grafo soma a demanda reprimida de todas as paradas de um mesmo eixo viário. | muda a unidade de análise do ponto individual para o corredor inteiro, evitando que passageiros espalhados em paradas próximas pareçam baixa demanda. |
| trocar a persona | **lente do regulador** | consórcio público, Ministério Público e imprensa consultam o saldo entre demanda nas paradas e oferta cumprida por bairro. | quem consome o resultado deixa de ser só o planejador da empresa; o painel público permite cobrar redistribuição quando a operadora ignora a demanda. |
| trocar o contexto | **turno de 1 hora** | grafo opera focado em linhas distritais, periféricas e entre-picos onde os intervalos oficiais chegam a 60 minutos. | sai dos corredores centrais de alta frequência e foca nos territórios e faixas horárias onde errar o ponto custa uma hora perdida. |
| trocar a tecnologia | **desistência medida** | confirmação de presença por GPS e histórico local separam quem só consultou de longe de quem esperou na parada e desistiu. | acrescenta verificação espacial no aparelho antes de enviar o evento ao grafo, impedindo que consultas feitas em casa contem como fila real na parada. |
| juntar | **grade viva** | juntar o GrafoParada ao DespachoVivo transforma o mapa de demanda reprimida e frota ociosa em sugestão pronta de nova tabela horária. | o sistema deixa de apenas diagnosticar o desequilíbrio entre paradas e passa a sugerir quais viagens transferir das linhas ociosas para as estranguladas. |
| restringir | **trava de presença** | só entram no cálculo de demanda reprimida as aberturas de parada feitas com localização ligada dentro do raio físico do ponto. | impõe a proximidade física verificada por GPS como restrição de entrada, bloqueando cliques remotos ou tentativas de inflar artificialmente uma linha. |

## 5 · o que fica e o que sai

**o que eu gostei:** gostei muito de **canalizar** (**clique que vota**) e de **inverter** (**frota no vazio**). o passageiro não precisa preencher formulário: basta abrir a parada com a localização ligada para checar o ônibus, e essa presença no ponto vira o registro da demanda. ao mesmo tempo, inverter o olhar para mostrar onde há ônibus rodando vazios resolve a desculpa de que "não há frota disponível", apontando de onde remanejar horários.

**o que achei interessante:** a **trava de presença** (**restringir** / **trocar a tecnologia**) resolve de forma simples uma falha grave: pedir que a localização esteja ativa confirma que a pessoa está realmente próxima da parada e permite medir se ela foi embora antes de o ônibus passar. também achei útil o **pulso do corredor** (**reescalar**) para somar paradas vizinhas da mesma linha.

**o que eu descarto, e por quê:** descarto o despacho em tempo real de veículos extras durante a viagem e o *matching* com vans/carros (**PonteModal** e **RotaElástica**) porque exigiriam coordenação logística imediata com garagens e motoristas em campo. neste semestre, o foco é provar a demanda reprimida no grafo e sugerir o remanejamento da tabela horária com dados reais de GTFS/GPS.

**minha ideia completa:** **GrafoParada · Frota no Vazio**

passageiros abrem a parada no mapa com a localização ligada para ver onde está o ônibus e decidir se vale esperar.  
regras determinísticas confirmam pelo GPS do celular se a pessoa está no raio da parada (e se desistiu antes de o veículo passar) e pelo GPS público do ônibus se o veículo parou no ponto para embarque (*dwell time*) ou passou direto.  
uma rede neural de grafos espaço-temporal (ST-GNN) cruza esses eventos de espera, desistência e tempo de parada dos veículos ao longo dos corredores.  
o modelo contrasta paradas com demanda reprimida e trechos onde os ônibus passam direto sem ninguém no ponto, gerando propostas de redistribuição de horários sem exigir aumento total de frota nem acesso ao banco fechado da catraca.

## 6 · refinamento

**a · e se todo mundo usasse?** em cinco anos, integrado a apps de consulta de paradas e órgãos gestores no país (setor que custa R$ 75,7 bilhões/ano e perdeu 19,1 milhões de passageiros/dia na última década segundo a NTU), o sistema permitiria recuperar viagens perdidas e cortar o desperdício de diesel em trechos ociosos apenas reequilibrando quadros horários. cada passageiro usa por interesse próprio — ligar a localização e tocar na parada para saber se espera ou pega alternativa —, gerando a prova coletiva sem esforço extra.

**b · a IA que não pode faltar.** técnica: rede neural de grafos espaço-temporal (ST-GNN) · aula da disciplina: Aula 07 · arquiteturas de deep learning (1/4): redes de grafos

por que sem ela não roda: regras determinísticas resolvem a checagem de raio por GPS (confirmar se o usuário está na parada), a filtragem de cliques repetidos e a leitura do GPS do ônibus para saber se ele freou e ficou parado no ponto (*dwell time* de embarque) ou se passou direto. porém, uma regra simples (`if buscas > X`) falha porque um ônibus pode passar direto tanto porque a parada está vazia quanto porque já vem lotado das paradas anteriores, além de o atraso num nó inicial propagar desistências em cascata pelo corredor. a ST-GNN é necessária para modelar essa dependência espaço-temporal entre paradas e veículos, distinguindo parada realmente vazia de ônibus cheio que não parou, e pareando trechos ociosos com corredores estrangulados. se nos testes uma média histórica por parada empatar com a ST-GNN, retiro a alegação e volto aos motores.

**c · o cético e as saídas**

| crítica | saída 1 | saída 2 | minha decisão |
|:--|:--|:--|:--|
| pessoas podem abrir paradas no mapa deitadas em casa ou clicar repetidas vezes para tentar puxar mais ônibus para sua rua, inflando uma demanda que não estava no ponto. | exigir localização ativa e aplicar regra espacial que só contabiliza presença física no raio da parada acompanhada de tempo mínimo de espera sem embarque. | limitar um voto válido de espera por aparelho/janela horária e confirmar o embarque quando a trajetória do usuário passa a acompanhar o GPS do ônibus após a parada. | combino as duas saídas: ligar a localização já é natural para achar paradas próximas no mapa e garante a confirmação física no ponto, enquanto a trava por janela horária impede cliques repetidos. |
| nem todo passageiro usa app na parada (como idosos) e nós não temos acesso ao banco fechado da catraca da empresa; olhar só para o app pode achar que uma parada está vazia e cortar ônibus de quem não tem celular. | medir o embarque físico de quem não usa app pelo próprio GPS público do ônibus: se o veículo reduz a velocidade a zero na coordenada da parada e permanece parado de 15 a 60 segundos (*dwell time*), há embarque real no ponto. | proibir o algoritmo de sugerir cortes onde o GPS do ônibus registra paradas frequentes para embarque, restringindo o rótulo de "frota no vazio" aos trechos onde nem há presença no app nem o ônibus precisa parar nos pontos. | adoto as duas: nunca chamo busca no app de demanda total; o GPS público do ônibus protege quem não usa celular ao detectar as paradas reais de embarque sem precisar de acesso à catraca da empresa. |
| empresas de ônibus podem ignorar as sugestões de ajuste se preferirem rodar com intervalos de 1 hora para economizar óleo diesel, e apps comerciais fechados não abrem seus logs internos. | usar o mecanismo de inversão (**frota no vazio**) para propor remanejamentos de soma zero (transferir viagens de horários onde o ônibus passa direto sem parar para horários com desistência comprovada) e tornar o painel público. | construir no semestre um protótipo próprio sobre dados públicos de GTFS/GPS, combinando coleta controlada de abertura de paradas com localização ativa e cenários simulados de desistência. | escolho as duas: no protótipo da disciplina, rodo a ST-GNN sobre o grafo GTFS/GPS público com validação de presença na parada; na recomendação, priorizo realocação de frota ociosa com transparência aberta. |

## 7 · resumo, sem IA

o transporte público brasileiro perdeu 19,1 milhões de viagens diárias na última década porque planeja horários olhando quase só para a catraca, tratando quem desiste de esperar ônibus de 1 em 1 hora como inexistência de demanda.  
o **GrafoParada · Frota no Vazio** aproveita o ato de abrir a parada no mapa com a localização ligada para confirmar quem esteve no ponto e desistiu antes de o ônibus passar, sem depender do banco fechado da catraca.  
regras conferem a presença física do usuário e se o ônibus parou no ponto pelo GPS público, enquanto uma rede de grafos espaço-temporal (ST-GNN) propaga o fluxo pela malha para separar paradas vazias de linhas lotadas e medir a demanda reprimida.  
em escala, consórcios e prefeituras podem redistribuir viagens de trechos onde os ônibus passam direto no vazio para horários estrangulados, sem aumentar a frota.  
cada passageiro usa apenas para checar no mapa se o ônibus vem ou se vale buscar alternativa naquela hora.
