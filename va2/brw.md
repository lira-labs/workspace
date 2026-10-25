# brw · Cauã da Cunha Lira

> folha do artefato [brainwriting híbrido](https://www.google.com/search?q=../3-brainwriting-hibrido.md). siga o guia passo a passo
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
| [x] | outra: apagão da demanda reprimida e má distribuição de frota no transporte público urbano (o "paradoxo da catraca" e a censura estrutural da bilhetagem eletrônica) |

por que esta crise: na parada perto de casa vejo vizinho esperando ônibus por mais de 50 minutos até desistir e pagar corrida de moto ou van pirata. enquanto isso, a prefeitura olha para o relatório da catraca vazia, acha que a linha perdeu passageiros e corta mais horários da tabela. quero que o transporte público enxergue quem desiste no ponto antes de condenar a linha ao abandono.

**tecnologias de IA** (marque 3 e chame de A, B, C):

| | tecnologia de IA |
|:-:|:--|
| [x] A | grafos e RAG (redes neurais de grafos espaço-temporais) |
| [x] B | sistemas multiagente e agência (*tools*, MCP) |
| [x] C | modelos locais / no aparelho (*SLMs*, 1B–7B) |

**infraestruturas tradicionais** (marque 3 e chame de 1, 2, 3):

| | infraestrutura |
|:-:|:--|
| [x] 1 | geolocalização, GPS e mapas |
| [x] 2 | crowdsourcing e curadoria coletiva |
| [x] 3 | plataformas de dois lados (*matching*, como Uber) |

## 2 · clichês

| clichê | o que acerta | onde fica raso |
|:--|:--|:--|
| app de horário de ônibus (Cittamobi, Moovit) | mostra no mapa onde o veículo está e ajuda o passageiro a decidir se espera. | trata a consulta como leitura passiva; se a pessoa vê um atraso de 50 minutos e fecha o app para desistir, essa intenção de viagem evapora sem gerar registro de demanda no sistema. |
| planejamento de frota pela bilhetagem eletrônica (catraca) | contabiliza com precisão quem conseguiu embarcar e pagar a tarifa. | sofre de censura estrutural de demanda (*demand unconstraining*): mede capacidade consumida, não demanda real; ignora quem desistiu pelo intervalo ou não conseguiu subir porque o veículo passou lotado. |
| pesquisa Origem-Destino (OD) por formulário | levanta deslocamentos desejados fora do que a catraca registra. | custa milhões, leva anos para atualizar e tem baixa resolução temporal; nasce defasada e não detecta gargalos operacionais cotidianos. |
| ouvidoria e chatbot de reclamação de linhas | abre um canal formal para registrar queixas sobre atrasos e superlotação. | gera relatos textuais isolados e sem coordenadas; não constrói o tensor espaço-temporal necessário para recalcular e calibrar a tabela horária. |
| painel gerencial de GPS das operadoras | fiscaliza se a frota cumpriu as viagens programadas na tabela oficial. | audita apenas a conformidade do quadro vigente, sendo cego para saber se a própria tabela roda vazia em um bairro enquanto outro sofre escassez de veículos. |

## 3 · matriz 3 × 3 e a minha ideia

cada célula: **nome** · frase de até 20 palavras (quem usa, o que faz).

| | 1 · geolocalização, GPS e mapas | 2 · crowdsourcing e curadoria coletiva | 3 · plataformas de dois lados (*matching*) |
|:--|:--|:--|:--|
| **A · grafos e RAG** | **GrafoParada** · analistas de transporte cruzam GTFS, GPS aberto e buscas em grafo para estimar pressão e demanda reprimida. | **MapaLotação** · passageiros sinalizam paradas cheias; rede em grafo propaga estimativa de risco de pass-up para paradas seguintes. | **RotaElástica** · RAG cruza solicitações acumuladas na região e sugere variantes temporárias de trajeto para linhas paralelas. |
| **B · sistemas multiagente** | **DespachoVivo** · agentes monitoram headway entre ônibus no GPS e sugerem ajustes táticos de intervalo aos operadores. | **FiscalColetivo** · agentes cruzam relatos de espera com telemetria oficial e geram dossiês públicos de não atendimento. | **PonteModal** · plataforma conecta vans cadastradas como apoio emergencial em trechos onde a linha regular colapsou. |
| **C · modelos locais** | **SentinelaPonto** · modelo local no aparelho resume histórico de espera do usuário preservando privacidade antes do envio agregado. | **VozDaParada** · modelo no celular converte relatos curtos de atraso em atributos estruturados sem expor dados pessoais. | **CaronaBairro** · modelo local conecta passageiros retidos na mesma parada para organizar deslocamentos compartilhados locais. |

**as 9 no mapa impacto × viabilidade:**

| | viabilidade alta | viabilidade baixa |
|:--|:--|:--|
| **impacto alto** | **GrafoParada** — usa dados públicos existentes (GTFS/GPS) e consultas para apoiar redistribuição tática de viagens; cabe no semestre.<br>**DespachoVivo** — foca no equilíbrio de intervalos entre veículos em operação; viável com feeds de GPS abertos. | **RotaElástica** — esbarra em regulamentação rígida de concessões e na inviabilidade jurídica de mudar itinerários em tempo real.<br>**FiscalColetivo** — depende de massa crítica de relatos manuais auditados para ter validade jurídica.<br>**PonteModal** — exige articulação regulatória complexa e acordos com frotas de vans e cooperativas. |
| **impacto baixo** | **MapaLotação** — alerta pontos cheios, mas não entrega alvos matemáticos para recalcular a ordem de serviço; teste simples.<br>**SentinelaPonto** — protege privacidade localmente, mas não resolve o cálculo central da rede; teste pequeno. | **VozDaParada** — processamento de voz no ponto gera ruído de áudio, gasta bateria e não supera dados tabulares.<br>**CaronaBairro** — resolve viagens pontuais entre vizinhos, mas não ataca a escala do transporte coletivo. |

**as duas perguntas: o argumento do interesse próprio e a alternativa sem IA:**

| ideia | quem usa ganha, para si | o que custa a ele | o que resolve sem IA avançada | se sustenta? |
|:--|:--|:--|:--|:--|
| GrafoParada | o órgão gestor identifica linhas ociosas e gargalos para redistribuir viagens sem custo extra | auditar os dados públicos de GPS e GTFS já disponíveis | uma planilha com média histórica de atrasos, mas ela não propaga o efeito da rede nem mede a demanda latente | sim |
| MapaLotação | o passageiro vê se a parada à frente está lotada | apertar um botão no app toda vez que chegar ao ponto | um grupo de mensagens ou botão de aviso simples | **não**: o passageiro esquece de avisar se estiver correndo, e um botão simples resolve |
| RotaElástica | o passageiro ganha ônibus direto onde a rota habitual falhou | esperar o sistema formar quórum para desviar a linha | um mapa de linhas alternativas existentes | **não**: a concessão pública não permite desvio dinâmico de trajeto |
| DespachoVivo | o operador evita comboio de ônibus (*bunching*) e economiza combustível | monitorar o painel e avisar os motoristas | um cronômetro com regras de intervalo fixo | sim |
| FiscalColetivo | a comunidade ganha provas documentadas contra a concessionária | preencher formulário e anexar horário toda vez que o ônibus atrasa | o canal oficial da ouvidoria municipal | **não**: o passageiro cansado não preenche denúncia sem benefício imediato |
| PonteModal | o passageiro retido consegue transporte alternativo regulamentado | pagar a tarifa da van integrada | um grupo de transporte complementar local | **não**: depende de regulação municipal prévia que não cabe no semestre |
| SentinelaPonto | o usuário tem sua privacidade resguardada no aparelho | processar dados no próprio celular gastando bateria | anonimização determinística simples por hash e agregação por raio | **não**: agregação espacial na origem sem modelo de IA resolve a privacidade |
| VozDaParada | o passageiro reclama por áudio sem precisar digitar na rua | gravar áudios em paradas barulhentas | botões com opções fixas ("lotado", "não passou") | **não**: formulário de um toque resolve sem erro de transcrição |
| CaronaBairro | vizinhos dividem o custo de um carro por aplicativo na parada | combinar destino e esperar desconhecidos no ponto | grupos de WhatsApp do bairro | **não**: o grupo de mensagens do bairro já resolve sem IA |

onde discordei da IA, e por quê: a IA colocou o GrafoParada em viabilidade média por achar que dependia de integração com os sistemas fechados de bilhetagem das empresas. passei para alta: consigo testar a estimação de oferta e headways anômalos em um corredor real usando apenas dados públicos de GTFS e GPS aberto da cidade, comparando o modelo contra baselines simples em um notebook. isso não exige convênio formal com operadores para começar e cabe no semestre.

**minha ideia escolhida:** **GrafoParada** · analistas de transporte estimam pressão operacional e demanda reprimida cruzando telemetria aberta com volumes agregados de consulta.

**por que ela, sem IA, em até 3 linhas:**
porque o passageiro já abre o mapa para checar o ônibus, gerando o sinal de intenção sem precisar preencher nada;  
porque cruzar esse sinal com o GPS público mostra onde a linha roda no vazio e onde a demanda está represada;  
porque permite à prefeitura redistribuir viagens ociosas para horários críticos sem aumentar o gasto com subsídio.

## 4 · motores

| motor | o que foi [verbo] | nome | frase | o que mudou em relação à ideia | o que quem usa ganha para si | se sustenta nas duas perguntas? |
|:--|:--|:--|:--|:--|:--|:--|
| inverter | a direção da análise: em vez de buscar mais frota, expõe onde o ônibus roda vazio para transferir viagem | **frota no vazio** | mapa expõe trechos onde ônibus rodam vazios enquanto paradas vizinhas acumulam filas de espera. | a pergunta deixa de ser "onde falta ônibus" e passa a ser "de onde tirar ônibus ocioso para atender quem espera". | o gestor resolve a reclamação sem pedir mais orçamento. | sim |
| canalizar | a checagem rotineira de horários, que o passageiro já faz no celular para saber quando o ônibus chega | **clique de pressão** | o volume agregado de consultas por parada e linha funciona como sinal fraco de intenção de viagem. | o gesto passivo de olhar a tela vira o dado de entrada da pressão de demanda, sem formulário. | não precisa fazer nada além do que já faz. | sim |
| transplantar | o estimador de desbalanço entre oferta e demanda dos apps de carona para o transporte público coletivo | **pressão de corredor** | como nos mapas de demanda de corridas, o sistema calcula o risco de passageiros ficarem na parada. | traz a estimativa de desequilíbrio dinâmico para recalcular a ordem de serviço pública. | antecipa reclamações antes de a linha colapsar. | sim |
| reescalar | a unidade de análise: de paradas isoladas para a cadeia topológica de toda a extensão do corredor | **pulso do corredor** | em vez de olhar um ponto único, o modelo avalia como o atraso a montante estrangula o corredor a jusante. | a avaliação deixa de ser pontual e passa a modelar a propagação do fluxo na linha. | enxerga a causa do atraso e não apenas o sintoma. | sim |
| trocar a persona | saiu o passageiro na parada, entrou o técnico de planejamento do órgão público gestor | **lente do regulador** | técnicos da prefeitura usam o contraste entre frota ociosa e pressão de busca para auditar tabelas. | o foco passa de utilitário individual de mobilidade para ferramenta de auditoria contratual. | embasa cortes e remanejamentos com dados auditáveis. | sim |
| trocar o contexto | do horário de pico matutino para as janelas de entre-pico e finais de semana | **entre-pico invisível** | sistema prioriza faixas horárias de baixa frequência onde intervalos longos provocam mais desistências. | foca a medição exatamente onde a catraca é mais cega e onde o passageiro mais desiste. | recupera passageiros que já haviam desistido do ônibus. | sim |
| trocar a tecnologia | da rede neural de grafos para um modelo tabular com gradiente boosted (LightGBM) com lags | **tabela de atraso** | árvores de decisão usam histórico de atrasos e horários para prever o próximo headway da linha. | substitui o grafo por uma tabela simples de variáveis defasadas. | processamento rápido e fácil de auditar. | **não**: uma tabela isolada não propaga o impacto de uma parada sobre as paradas seguintes na rede |
| juntar | GrafoParada + frota no vazio | **grade viva** | contrasta a pressão de demanda latente com as viagens ociosas e gera proposta de remanejamento de viagens. | o sistema deixa de apenas diagnosticar o problema e sugere a nova tabela de horários de soma zero. | recebe a sugestão de tabela pronta para colocar em consulta. | sim |
| restringir | o hardware: operar sem servidores dedicados, apenas com scripts em planilhas eletrônicas | **matriz em planilha** | uma planilha cruza a tabela horária oficial com a média de embarques da catraca. | elimina o pipeline de IA e roda apenas operações em tabelas estáticas. | custo zero de infraestrutura de software. | **não**: a planilha não lê o feed contínuo de GPS nem enxerga quem não conseguiu embarcar |

## 5 · o que fica e o que sai

**o que eu gostei:** da **frota no vazio** (inverter), porque mostra de onde tirar viagem sem pedir mais dinheiro à prefeitura; e do **clique de pressão** (canalizar), que aproveita o hábito que o passageiro já tem de olhar o mapa sem pedir cadastro nem denúncia.

**o que achei interessante:** no **pulso do corredor**, o fato de que olhar a linha inteira como grafo explica por que uma parada no fim do trajeto está vazia: o ônibus já vem atrasado e lotado desde o início da rota, e quem está no fim já desistiu antes de ele passar.

**o que eu descarto, e por quê:** descarto o despacho de ônibus em tempo real e a criação de linhas dinâmicas (RotaElástica e PonteModal): a regulação das concessões é rígida e motoristas não mudam rota no susto. descarto também a matriz em planilha: ela continua cega para a demanda reprimida e repete o erro da catraca. neste semestre o foco é diagnóstico e redistribuição de tabela horária programada.

**minha ideia completa:** **GrafoParada · Frota no Vazio**

analistas de transporte usam o GTFS programado e o GPS aberto dos ônibus para reconstruir atrasos, intervalos e o tempo efetivo de parada (*dwell time*) em cada ponto.  
o volume de consultas aos mapas na parada com localização ativa entra como sinal de demanda reprimida, e uma rede neural de grafos espaço-temporal (ST-GNN) modela como o atraso se propaga ao longo do corredor.  
o modelo contrasta paradas com alta pressão de espera e trechos onde veículos passam direto no vazio, gerando propostas de remanejamento de horários sem exigir mais frota nem acesso ao banco fechado da catraca.  
a prefeitura reduz o intervalo onde a população mais desiste de esperar, o passageiro volta a confiar no horário e o sistema recupera receita de tarifa sem aumentar o subsídio público.

## 6 · refinamento

**a · e se todo mundo usasse?**

o tamanho da crise hoje:
- o transporte público por ônibus perdeu 19,1 milhões de passageiros pagantes por dia entre 2013 e 2023 no Brasil, uma queda de 40% da demanda histórica ([Anuário NTU 2023-2024](https://www.google.com/search?q=https://www.ntu.org.br/novo/upload/Publicacao/Pub638555239564619934.pdf)).
- os sistemas de ônibus urbanos custaram R$ 75,7 bilhões em 2023, exigindo mais de R$ 12,7 bilhões em subsídios públicos para cobrir déficits de linhas que rodam vazias ([NTU, Custos e Tarifas](https://www.ntu.org.br)).
- no Grande Recife, as viagens diárias caíram de 2 milhões para menos de 1,2 milhão na última década, empurrando a população para vans clandestinas e aplicativos ([Grande Recife Consórcio / Urbana-PE](https://www.granderecife.pe.gov.br)).
- quem ganha até 2 salários mínimos gasta em média 2 horas e 14 minutos por dia no deslocamento casa-trabalho nas capitais, esperando até 45 minutos na parada ([Ipea, Desigualdades de Acesso](https://www.ipea.gov.br/portal/images/stories/PDFs/TDs/td_2565.pdf)).

se todo mundo usasse por 5 anos (a minha aposta):
- se a redistribuição de frota ociosa recuperasse 10% dos passageiros que desistiram (1,9 milhão de viagens/dia no país), seriam cerca de R$ 3,1 bilhões ao ano em receita tarifária recuperada, aliviando a pressão por subsídio nas prefeituras.
- o tempo médio de espera no entre-pico em linhas periféricas cairia de 55 para 25 minutos, devolvendo até 30 minutos livres por dia para quem depende exclusivamente do ônibus.
- uma fatia de R$ 1,5 bilhão hoje gasta em transporte clandestino inseguro ou viagens individuais de emergência voltaria para a economia familiar dos bairros periféricos.

por que cada pessoa usaria: o gestor público, para cumprir metas contratuais e remanejar viagens sem pedir verba extra; o passageiro, porque o ônibus passa no horário e a espera diminui. ninguém precisa querer ajudar.

**b · a IA que não pode faltar.** técnica: rede neural de grafos espaço-temporal (ST-GNN, como STGCN — Yu, Yin & Zhu, IJCAI 2018)

por que sem ela não roda: regras determinísticas já filtram consultas repetidas e medem o tempo de parada física (*dwell time*) pelo GPS do veículo. porém, o transporte opera sobre uma malha onde o atraso na parada A causa comboio (*bunching*) e superlotação na parada B minutos depois. uma regressão tabular ou árvore trata cada parada como linha isolada e ignora essa propagação em cadeia; a ST-GNN usa a matriz de adjacência do itinerário para aprender como perturbações viajam pelo corredor no espaço e no tempo, distinguindo uma parada vazia de um ônibus que passou direto porque já vinha lotado. contudo, adoto o rigor de parcimônia: se no teste empírico temporal um modelo tabular com lags (LightGBM) ou uma GRU temporal sem grafo empatar em acurácia de headway dentro da margem de erro, eu retiro a rede de grafos e fico com o modelo simples.

**c · críticas de quem está de fora**

| crítica | saída 1 | saída 2 | minha decisão |
|:--|:--|:--|:--|
| consulta em app não é pessoa física na fila; o clique pode vir de quem está em casa ou de robôs. | treinar o modelo em variáveis observáveis de oferta (headway real e atraso no GPS) e tratar a busca apenas como peso probabilístico. | exigir biometria e cadastro prévio para validar que o passageiro está fisicamente no ponto. | **saída 1**, treinando o alvo em dados físicos de telemetria e tratando a consulta como proxy calibrado, sem burocracia para o usuário. |
| nas periferias e entre idosos menos pessoas usam o app, e o modelo pode achar que a parada vazia no mapa é falta de interesse. | incluir a capacidade nominal do ônibus e aplicar máscara de observabilidade que impeça o modelo de confundir ausência de dado com ausência de passageiro. | confiar que a amostra de jovens com celular representa toda a fila da parada. | **saída 1**: usar a máscara de observabilidade e auditar o modelo por setor censitário de renda (IBGE) para não cortar viagens de bairros vulneráveis. |
| o semestre letivo é curto para conseguir convênios de dados com prefeituras ou empresas de ônibus. | congelar na 2ª semana o uso de dados 100% abertos de GTFS e feeds públicos de GPS (como os da Cittamobi ou Grande Recife). | esperar a assinatura de um acordo formal com o órgão gestor da cidade. | **saída 1**, garantindo que o protótipo rode em um corredor real com dados públicos disponíveis na web, sem depender de autorização externa. |

## 7 · resumo, sem IA

as prefeituras cortam viagens de ônibus porque a catraca não registra quem desistiu de esperar intervalos de uma hora, condenando as linhas periféricas a rodarem cada vez mais vazias.  
o GrafoParada · Frota no Vazio cruza a posição dos ônibus pelo GPS público com o volume de consultas de rotas para estimar onde há passageiros esperando e onde os veículos rodam ociosos.  
uma rede neural de grafos mapeia como o atraso se propaga ao longo do corredor; se um modelo simples resolver, ele assume o lugar da rede.  
se todo mundo usasse, prefeituras transfeririam viagens que rodam no vazio para os horários de sufoco, devolvendo 30 minutos diários a quem trabalha e recuperando passageiros sem gastar mais com subsídio.  
o gestor usa para ajustar a tabela sem precisar de mais dinheiro; o passageiro, para não perder a viagem na parada.

## 8 · auditoria cega

**o veredito da conversa nova:**

| item | passa ou não passa | trecho que prova | o que já resolve sem IA avançada |
|:--|:--|:--|:--|
| 1 · brw completo | passa | todas as seções preenchidas, do § 1 ao § 8 | — |
| 2 · impacto claro | passa | "19,1 milhões de passageiros pagantes por dia perdidos"; "devolver até 30 minutos livres por dia" | — |
| 3 · ia avançada | passa | "a ST-GNN usa a matriz de adjacência do itinerário para aprender como perturbações viajam pelo corredor no espaço e no tempo... se o LightGBM empatar, retiro a rede" | uma média móvel de atrasos mostra o atraso passado, mas não prevê a propagação de comboios ao longo da cadeia de paradas |

**a minha resposta, sem IA:**
1. nada a mudar.
2. nada a mudar.
3. mantenho a ST-GNN como hipótese espacial porque atraso em linha de ônibus é problema clássico de propagação em rede dirigida (*bunching*), mas o teste de ablação ($A=I$) e a baseline tabular (LightGBM) estão programados para verificar se o ganho justifica o custo computacional.