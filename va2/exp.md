# exp · Cauã da Cunha Lira

> folha do artefato [desenho dos experimentos](../3-desenho-dos-experimentos.md). siga o guia passo
> a passo e preencha cada seção aqui. as decisões são suas, e decidir é saber explicar.

## 0 · a minha ideia, e o que ficou para medir

**GrafoParada · Frota no Vazio**

analistas de transporte usam o GTFS programado e o GPS aberto dos ônibus para reconstruir atrasos, intervalos e o tempo efetivo de parada (*dwell time*) em cada ponto.  
o volume de consultas aos mapas na parada com localização ativa entra como sinal de demanda reprimida, e uma rede neural de grafos espaço-temporal (ST-GNN) modela como o atraso se propaga ao longo do corredor.  
o modelo contrasta paradas com alta pressão de espera e trechos onde veículos passam direto no vazio, gerando propostas de remanejamento de horários sem exigir mais frota nem acesso ao banco fechado da catraca.  
a prefeitura reduz o intervalo onde a população mais desiste de esperar, o passageiro volta a confiar no horário e o sistema recupera receita de tarifa sem aumentar o subsídio público.

**o que eu medi no tec:** no meu computador, em CPU (sem exigir GPU), a rede STGCN (PyTorch 2.14 + NetworkX, 34.627 parâmetros) levou menos de 10 segundos para construir o grafo das 5 paradas da linha distrital (Camela, PE-60, Ipojuca, Suape e Gaibu), rodar o ciclo de treino de 25 épocas e prever a espera para $t+10$, $t+20$ e $t+30$ minutos. a rede acertou a propagação espacial do gargalo de P1 (43,2 min) para P2 (40,6 min), mas errou na escala dos picos extremos de atraso, suavizando valores súbitos em direção à média do lote por falta de padronização estatística (*z-score*).

**o que o flx deixou para o experimento:** a normalização por *z-score* e o pareamento da viagem ociosa viraram regras fixas nos passos 5 e 7, e o passo 8 ganhou o atraso real do GPS bruto ao lado da previsão da STGCN para o analista cobrir o erro de suavização de picos. ficou para o experimento medir: (1) o gasto real de memória RAM em CPU; (2) se o *z-score* e o sinal de consultas na parada reduzem o erro silencioso (quando a espera real passa de 40 min e a STGCN suaviza o pico e não avisa); e (3) quantas paradas críticas o analista consegue corrigir no passo 8 olhando o GPS bruto ao lado do alerta.

## 1 · os experimentos e a comunidade de cada um

| exp. | a pergunta que ele responde | o que é testado: a técnica, uma pessoa usando, ou o nicho | a comunidade e os veículos | o experimento publicado que eu sigo (com link) |
|:--|:--|:--|:--|:--|
| E1 | a STGCN com *z-score* e consultas na parada prevê a espera em $t+30\text{ min}$ com menos erro silencioso ($> 40\text{ min}$ sem aviso) e menor MAE do que regras e árvores sem grafo? | a técnica (previsão espaço-temporal e detecção de gargalo de desistência) | Sistemas Inteligentes de Transporte e Aprendizado de Máquina: *Transportation Research Part C*, *IEEE TITS*, *IJCAI* | [Wang et al. (2022)](https://doi.org/10.1016/j.trc.2022.103790) (*Transportation Research Part C*, Qualis A1): avalia previsão de curto prazo em paradas de ônibus integrando buscas de app contra baselines autorregressivos; e [Yu, Yin & Zhu (2018)](https://doi.org/10.24963/ijcai.2018/505) (*IJCAI*): avalia a STGCN em horizontes múltiplos por MAE e RMSE |
| E2 | conferindo a tela do Passo 8 (alerta da STGCN + atraso bruto do GPS), o analista identifica mais gargalos reais e remaneja melhor as viagens ociosas do que olhando só a planilha de catraca e GTFS? | uma pessoa usando, num nicho (tomada de decisão operacional com IA e verificação de viés de automação) | IHC e Apoio à Decisão: *CHI*, *CSCW*, *Human Factors* | [Patel et al. (2009)](https://doi.org/10.1145/1518701.1518709) (*CHI 2009*): compara duas condições de interface com os mesmos participantes em quadrado latino medindo tarefa completada e tempo; e [Parasuraman & Manzey (2010)](https://doi.org/10.1177/0018720810376055) (*Human Factors*): mede erro por omissão/complacência quando a IA suaviza um alerta |

## 2 · E1 · a STGCN prevê o gargalo de espera sem calar nos picos

### 2.1 · hipótese, linhas de base e o número que derruba

**a hipótese:** nos 4 corredores críticos do SEI (20 paradas), em janelas com formação de comboio (*bunching*) e pico de espera ($> 40\text{ min}$), a STGCN alimentada com *z-score* e contagem de consultas na parada deixa passar **no máximo 10% dos gargalos sem aviso** (falso negativo em $t+30\text{ min}$), reduz o MAE em pelo menos **1,5 minuto** frente ao baseline tabular sem grafo, e roda em CPU gastando menos de **500 MB de RAM**.

**o jeito de hoje:** persistência temporal / média móvel da própria parada (assumir que a espera em $t+30\text{ min}$ será igual à espera atual observada no ponto ou à tabela estática GTFS, sem enxergar o atraso vindo das paradas anteriores).

**o competidor mais forte:** no `cmp`, o artigo mais próximo é [Wang et al. (2022)](https://doi.org/10.1016/j.trc.2022.103790) (regressão com buscas no app treinada sobre a catraca, sem grafo) e, pelo critério estrito de parcimônia do `brw`, um modelo tabular **LightGBM / Regressão com Lags Temporais** nos mesmos casos (usando o histórico da própria parada e as consultas no app, mas sem a matriz Laplaciana do grafo viário da STGCN).

**o número que derruba a hipótese:** gargalo $> 40\text{ min}$ **errado sem aviso** (falso negativo) acima de **10%**, **OU** vantagem de MAE da STGCN sobre o modelo tabular sem grafo menor que **1,5 minuto** (caso em que o critério de parcimônia derruba a STGCN em favor do modelo simples), **OU** consumo medido acima de **500 MB de RAM**, avaliado em 40 cenários de teste de corredor.

**escrito antes de rodar:** commit de pré-registro anterior à execução do piloto.

## 3 · E2 · o analista corrige o pico suavizado e remaneja a viagem certa

### 3.1 · hipótese, linhas de base e o número que derruba

**a hipótese:** usando a tela do Passo 8 (que exibe o alerta da STGCN junto com o atraso real do GPS bruto e o *dwell time*), o analista termina com **menos gargalos críticos sem cobertura** do que usando a planilha tradicional de catraca + GTFS, e precisa intervir manualmente para corrigir a sugestão do sistema em **no máximo 1 a cada 3 casos**.

**o jeito de hoje:** olhar a planilha estática de cumprimento de viagens (GTFS programado + contagem de catraca física), onde paradas queimadas ou abandonadas por espera de 1 hora aparecem como "baixa demanda".

**o competidor mais forte:** o Moovit Analytics e o Optibus são softwares proprietários fechados que não rodam no piloto local. no lugar, testamos como competidor a condição de **IA sem a coluna de conferência do GPS bruto** (apenas o alerta da STGCN e catraca, como num painel caixa-preta), para medir quantos picos suavizados enganam o analista quando falta a transparência do Passo 8.

**o número que derruba a hipótese:** taxa de remanejamentos errados no fim (gargalo real deixado sem viagem ou viagem tirada de horário cheio) na condição com o painel completo (Condição B) igual ou maior que na planilha de hoje (Condição A), **OU** necessidade de correção manual pelo analista acima de **33% (1 em cada 3 casos)**, em 30 casos operacionais.

**escrito antes de rodar:** o mesmo commit de pré-registro do E1.
