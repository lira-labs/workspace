# 🎙️ Roteiro Pronto para Leitura (Teleprompter) — 2ª VA · Internet do Futuro

> **Como usar:** Leia com calma, no seu ritmo normal de conversa. Os trechos entre colchetes `[PASSA O SLIDE]` são só para você saber a hora exata de mudar a tela.  
> **Tempo total:** cerca de **8 minutos e 30 segundos** (folga segura para o limite de 10 minutos).

---

### [SLIDE 1 — Capa: Telessaúde segura no interior] *(00:00 – 00:45)*

Olá, professora Jeisa. Olá, pessoal. Tudo bem? Meu nome é Cauã Lira, sou aluno aqui da Licenciatura em Computação da UFRPE, e hoje eu vim apresentar a minha proposta de projeto da segunda VA de Internet do Futuro.

Lá na primeira VA, o tema do meu seminário foi a Criptografia Pós-Quântica. Quando a gente começou a pensar nesse projeto agora, eu quis tirar esse assunto só da conversa de bancos e grandes empresas e trazer para um problema bem real do nosso país: como proteger os exames e os prontuários de pessoas que são atendidas por telessaúde lá no interior, bem longe das capitais.

---

### [PASSA PARA O SLIDE 2 — Dados de saúde duram décadas...] *(00:45 – 02:00)*

Desde 2022, a telessaúde é liberada por lei no Brasil inteiro. E isso faz uma diferença enorme para quem mora num sítio, num distrito do sertão ou numa comunidade ribeirinha lá na Amazônia. Com a telessaúde, a pessoa vai no posto de saúde perto de casa e consegue ser atendida por um médico especialista que está lá no Recife ou em outra capital.

Só que tem um detalhe. Nesses lugares mais afastados não chega fibra óptica e quase nunca tem sinal bom de celular. O jeito mais prático de levar internet até lá hoje é pelo satélite.

E aí entra o problema que pouca gente vê. Um exame do coração, um ultrassom ou um prontuário médico são dados super íntimos. A própria LGPD trata isso como dado sensível. E o mais importante: um dado de saúde precisa continuar em segredo pela vida inteira da pessoa. Daqui a vinte, trinta, cinquenta anos, aquele exame ainda diz respeito a ela.

Hoje, esses arquivos viajam pela internet protegidos pela criptografia comum. O problema é que, quando os computadores quânticos ficarem fortes de verdade, eles vão conseguir quebrar essa proteção atual. E não precisa nem esperar o futuro chegar para o risco começar. Já existe um golpe chamado "colha agora, abra depois". Funciona assim: alguém copia os dados que estão passando pelo satélite hoje, guarda tudo num cofre digital, e espera alguns anos até ter um computador quântico para abrir e ler tudo. É exatamente contra isso que a gente precisa agir agora.

---

### [PASSA PARA O SLIDE 3 — A criptografia pós-quântica roda nos computadores de hoje...] *(02:00 – 03:20)*

E é aí que entra o tema do meu seminário: a criptografia pós-quântica.

Muita gente acha que, pelo nome, ela precisa de um computador quântico para funcionar. Mas não precisa. A grande vantagem dela é que ela roda nos computadores e celulares comuns que a gente já usa hoje. A diferença é que ela usa um tipo novo de matemática, que nem os computadores normais e nem os computadores quânticos conseguem quebrar.

Em 2024, o NIST, que é o órgão que define esses padrões no mundo todo, lançou os primeiros algoritmos oficiais: o ML-KEM, que serve para combinar uma chave secreta entre dois computadores, e o ML-DSA, que serve para fazer uma assinatura digital e provar que ninguém mexeu no exame no meio do caminho.

Só que lá na primeira VA eu também mostrei uma limitação bem clara dessa tecnologia: o tamanho. Enquanto uma chave comum de hoje tem só 32 bytes, uma chave pós-quântica passa de mil bytes, e uma assinatura passa de três mil bytes. É muito mais pesada. Um aparelhinho simples do posto de saúde, com pouca memória, não aguenta rodar isso sozinho. E foi pensando nessa limitação que eu juntei o meu tema com o tema de outros três colegas da turma.

---

### [PASSA PARA O SLIDE 4 — Quatro tecnologias se unem...] *(03:20 – 04:40)*

Nenhuma dessas tecnologias resolve o problema sozinha, mas juntas uma cobre o ponto fraco da outra.

A primeira é a Criptografia Pós-Quântica, do meu seminário, que protege os dados hoje e pelos próximos trinta ou quarenta anos.

A segunda são os Satélites de Órbita Baixa, os satélites LEO, do seminário do Alexander. Como eles ficam bem mais perto da Terra do que os satélites antigos, eles levam internet rápida e sem aquele atraso chato para qualquer canto isolado do país.

A terceira é a Computação de Borda, o Edge Computing, do seminário do Daniel. A gente coloca um servidor pequenininho dentro do próprio posto de saúde para fazer o trabalho pesado da criptografia no lugar dos aparelhos simples.

E a quarta é o modelo Zero Trust, do seminário do João Victor Vasconcelos. No Zero Trust, ninguém é confiável só por estar dentro da rede. O sistema confere quem é o aparelho, quem é a técnica de enfermagem e quem é o médico toda vez que alguém pede para ver um exame.

Olha que encaixe bonito: a borda tira o peso da criptografia dos aparelhos fracos; a criptografia impede que a empresa dona do satélite leia os dados dos pacientes; e o Zero Trust impede que alguém invada o servidor do posto e veja o que não deve.

---

### [PASSA PARA O SLIDE 5 — Os dados saem protegidos do posto...] *(04:40 – 06:00)*

Aqui no slide a gente vê como essa arquitetura funciona em quatro camadas, mais uma camada de controle que atravessa tudo.

Na camada um ficam os aparelhos do posto, como um aparelho de eletrocardiograma portátil ou o tablet da equipe. Eles só mandam o exame pelo Wi-Fi interno do posto, sem precisar de nenhum processamento pesado.

Na camada dois fica o servidor de borda, que é o coração do projeto. É um mini computador comum lá dentro do posto. Ele recebe o exame, assina com o ML-DSA e abre um túnel seguro usando o ML-KEM junto com a criptografia atual. E se cair uma chuva forte e o sinal do satélite sumir, ele guarda tudo numa fila local e envia assim que a internet voltar.

Na camada três ficam a antena no telhado e os satélites LEO. Eles funcionam só como o caminhão que transporta a carga. Como os pacotes já saem trancados da borda, nem a empresa do satélite consegue enxergar o que tem dentro.

Na camada quatro fica o hospital de referência na capital. O servidor do hospital confere a assinatura do exame e guarda o prontuário já protegido para o médico abrir.

E por baixo de tudo isso corre o Zero Trust, conferindo cada pedido de acesso do começo ao fim.

---

### [PASSA PARA O SLIDE 6 — O exame do Seu José chega seguro...] *(06:00 – 07:10)*

Para ficar bem fácil de imaginar na vida real, vamos acompanhar o caso do Seu José, de 67 anos, que mora num distrito do sertão e chega ao posto sentindo uma dor no peito.

No passo um, a técnica de enfermagem faz o eletrocardiograma dele com um aparelho portátil.

No passo dois, o Zero Trust confere se aquele aparelho está cadastrado e se a técnica está autorizada a usar o sistema.

No passo três, o mini servidor lá do posto assina o exame com o ML-DSA e salva uma cópia de segurança no próprio posto.

No passo quatro, o exame sobe pela antena e viaja pelos satélites LEO dentro do túnel pós-quântico.

No passo cinco, o servidor do hospital lá no Recife recebe o arquivo, confere a assinatura e vê que ninguém alterou nada no caminho.

E no passo seis, o cardiologista abre o exame na hora e entra numa chamada de vídeo com o posto para orientar se o Seu José precisa ser levado de ambulância. Tudo isso rápido, sem travar, e com o histórico do Seu José protegido para o resto da vida.

---

### [PASSA PARA O SLIDE 7 — Quatro métricas testam o posto piloto...] *(07:10 – 08:15)*

Como este é um projeto teórico, também deixamos claro como a gente testaria se tudo isso funciona mesmo na prática, sem esconder os limites reais.

Para testar num posto piloto, a gente olharia para quatro coisas simples. Primeiro, se o aperto de mão pós-quântico na conexão causa algum atraso que atrapalhe a chamada de vídeo — pelos estudos, o aumento é bem pequeno, abaixo de cinco por cento. Segundo, quanto de internet extra essas chaves maiores gastam — dá menos de cinco kilobytes por exame, o que num arquivo de ECG ou ultrassom quase não faz diferença. Terceiro, se um mini computador comum aguenta o dia inteiro no calor do interior sem travar. E quarto, desligar a antena de propósito por uma hora para comprovar que cem por cento dos exames da fila chegam perfeitos quando o sinal volta.

E sendo bem sincero sobre as limitações: o sinal do satélite ainda sofre com tempestade, o posto precisa de energia estável para o servidor não desligar, e existe a dependência de empresas privadas donas dos satélites, que foi uma questão muito bem levantada no seminário do Alexander.

---

### [PASSA PARA O SLIDE 8 — A tecnologia já existe hoje...] *(08:15 – 08:50)*

O ponto principal que eu queria deixar é que a gente não precisa esperar dez anos para fazer isso. A tecnologia já está pronta hoje: os padrões do NIST saíram em 2024, os satélites LEO já cobrem o interior do Brasil e um mini computador de borda custa o preço de um computador simples.

O desafio maior não é técnico, é de gestão: colocar placa solar com bateria nos postos onde falta luz, treinar as equipes de saúde e começar pequeno, com um projeto piloto em parceria com o SUS e com a própria universidade.

---

### [PASSA PARA O SLIDE 9 — Segurança pós-quântica para proteger a dignidade...] *(08:50 – 09:20)*

Aqui estão as principais referências que eu usei no trabalho, cobrindo a criptografia pós-quântica, os satélites LEO, a computação de borda, o Zero Trust, a Lei da Telessaúde e a LGPD.

Quero agradecer à professora Jeisa pela disciplina e aos colegas pelos seminários, que deram toda a base para montar essa arquitetura junta. A criptografia pós-quântica não precisa ficar só nos grandes centros — ela também serve para proteger a dignidade de quem mora longe. Muito obrigado, e meu e-mail está aí na tela para qualquer dúvida!
