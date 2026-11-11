# sem2 · exemplo excelente

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), feito a partir do
> [tec excelente](../tec/excelente.md), do [flx excelente](../flx/excelente.md), do [exp excelente](../exp/excelente.md)
> e do [sem1 excelente](../sem1/excelente.md). as anotações do professor estão no fim.

**link dos slides:** o roteiro abaixo descreve cada slide; o deck deste exemplo não foi montado.

**a versão que roda:** a tag `sem2` em [github.com/lsfcin/rastro-da-banca](https://github.com/lsfcin/rastro-da-banca)

**a máquina:** o meu Redmi Note 10 Pro, o mesmo do exp, em modo avião, espelhado no projetor pelo scrcpy, por cabo.

**a gravação de reserva:** [ensaio-sem2.mp4](https://github.com/lsfcin/rastro-da-banca/releases/download/sem2/ensaio-sem2.mp4), a segunda passada do ensaio, sem cortes, anexada à *release* `sem2`.

## as quatro frases, sem IA

1. **a demo:** a dona Cida recebe o áudio de verdade de uma cliente e compartilha com o app. a tela entrega o pedido com a hora, ela confere ouvindo o áudio, confirma, e o pedido entra na lista de separação de sábado.
2. **o custo:** no celular, um áudio de 18 s levou 56 s do compartilhar à tela, e a memória chegou a 1,0 GB. o flx dava uns 52 s e 2 GB. a diferença é a carga do modelo e o formato do whisper.cpp.
3. **a falha:** "dois pés de alface" vira "dois peixes", e o pedido sai só com o maracujá, sem "?". quem sofre é a cliente que chega às nove. e o erro mostra que ouvir o áudio é o centro da ideia, não um detalhe.
4. **o que mudou:** no sem1, os quase 3 vezes o áudio eram o problema, e eu ia trocar pelo base. ficou o small, transcrevendo em fila enquanto ela atende, porque ela não espera a tela e o base trocou produto.

## slide 1 · ponta a ponta · 85 s

- **aparece:** o celular espelhado: a conversa da banca no WhatsApp, com dois áudios. depois, a tela do pedido.
- **a entrada:** o áudio da dona Lúcia, 18 s, gravado na rua e encaminhado pela dona Cida, com a autorização da cliente. o da dona Neide, 14 s, fica para o slide 3.
- **eu falo:** [compartilho os dois áudios com o app e toco o primeiro para a sala] "esse é o meu celular, em modo avião, fazendo o papel do celular da dona Cida. esse áudio é de verdade: a dona Lúcia, cliente da banca, mandou no sábado passado e deixou usar aqui. [o áudio toca] enquanto vocês ouviam, o app já estava transcrevendo, no celular, sem internet. na banca é assim: o áudio chega enquanto a dona Cida pesa a macaxeira de outra cliente. ela não fica olhando a tela. [a tela abre] pronto: dois quilos de jerimum, um molho de coentro, seis ovos, buscar às dez, R$ 16,50. o jerimum, que no tec virou limão, saiu certo. ela toca o áudio, confere, escreve 'Lúcia' e confirma. a confirmação sai pelo WhatsApp quando a rede voltar, e o pedido entra na lista de sábado, na fila das dez."

## slide 2 · quanto custa · 50 s

- **aparece:** na tela do celular, a linha que o app escreve no fim de cada execução: "áudio 18 s · do compartilhar à tela 56 s · pico de memória 1,0 GB · small · tag sem2". no slide, ao lado: "flx: 2,89 × 18 s ≈ 52 s · ~2 GB, estimado".
- **medido:** no ensaio, nesta máquina, duas execuções seguidas: 56 s e 52 s, com pico de 1,0 GB nas duas. em sala, leio o que a tela mostrar. se der diferente do ensaio, eu digo.
- **estimado no flx:** ~52 s, pelos 2,89 vezes o áudio que medi no exp. ~2 GB, pela [tabela de modelos do whisper](https://github.com/openai/whisper#available-models-and-languages).
- **eu falo:** "esse número é da execução que vocês acabaram de ver. do compartilhar até a tela pronta: 56 segundos. a conta do flx dava 52. a diferença é a carga do modelo, uns 4 segundos, que a conta não tinha: no ensaio, a segunda execução seguida deu 52, com o modelo já carregado. a memória chegou a 1,0 GB, metade do que eu estimei. os 2 GB do flx vieram da tabela do whisper original, que mede a memória da placa de vídeo de um computador. o celular usa o whisper.cpp, com o mesmo modelo num formato mais enxuto. no flx, troquei a estimativa pelo número medido. e o dinheiro segue zero: nada saiu do celular."

## slide 3 · a falha · 60 s

- **aparece:** a tela do segundo pedido, como saiu, e o certo ao lado.
- **a entrada:** o áudio da dona Neide, 14 s, com um carro de som passando: "Cida, me separa dois pés de alface e um quilo de maracujá, passo às nove."
- **a saída, como saiu:** ouvido: "Cida, me separa dois peixes e um quilo de maracujá, passo às nove." pedido: 1 quilo de maracujá, buscar às 09:00. nenhum "?".
- **o certo:** 2 pés de alface, 1 quilo de maracujá, buscar às 09:00.
- **eu falo:** "esse eu escolhi porque erra. a dona Neide pediu dois pés de alface, com um carro de som passando. o whisper ouviu 'dois peixes'. e olhem a tela: um quilo de maracujá, nove horas, nenhum '?'. o pedido tem cara de certo. o 'limão' do tec a regra pegou, porque parece produto e não está na lista. 'dois peixes', não: o item some calado. quem sofre é a dona Neide, que chega às nove e não tem alface, e a dona Cida, que perde a venda e a cliente. [toco o áudio e corrijo na tela] então ouvir o áudio, no passo 7, não é um detalhe da tela: é o centro da ideia. não consertei para hoje, de propósito. é a medida do sem3: quantos desses ela pega conferindo, contra o caderno."

## slide 4 · o que mudou desde o sem1 · 45 s

- **aparece:** duas linhas. "sem1: quase 3 vezes o áudio. trocar pelo base." / "agora: fica o small, em fila, enquanto ela atende."
- **no sem1:** "no celular a transcrição ainda leva quase 3 vezes o áudio", dito como problema. das duas saídas que o tec deixava, eu ia pelo base.
- **agora:** ficou o small, e o app transcreve em fila, um áudio depois do outro, enquanto ela atende.
- **eu falo:** "no sem1, eu mostrei os quase 3 vezes como problema, e ia trocar o small pelo base, que é mais rápido. mudei: ficou o small. vocês viram por quê: compartilhei dois áudios, e enquanto eu falava, o app transcreveu os dois, em fila. na banca é igual: ninguém espera a tela. e testei o base nos três áudios do tec: com a mesma lista no contexto, ele trocou a macaxeira. produto trocado é o erro que deixa cliente sem compra. entre esperar um minuto e errar o produto, a dona Cida espera."

## slide 5 · o fecho · 20 s

- **aparece:** a lista de separação de sábado: 09:00, dona Neide · 10:00, dona Lúcia. embaixo: "o pedido fica na banca."
- **eu falo:** "roda no celular, sem internet, a um minuto por áudio. e erra calado num caso que só ela pega. a soma para a colheita, que eu prometi no sem1, ainda não roda: hoje a demo para na lista de separação. no dia 25, eu trago quantos erros ela pega."

**tempo total, cronometrado, com a demo rodando:** 4 min 15 s e 4 min 25 s, duas vezes seguidas, no mesmo Redmi. a segunda está gravada sem cortes: é a reserva.

## ensaio cético

**a pergunta mais difícil:** "no sem1, o diferencial era a colheita somada. cadê ela na demo?"

**o que eu mudei por causa dela:** eu ia deixar sem falar. pus no fecho: "a soma para a colheita ainda não roda". prefiro que a turma saiba por mim. e tirei do slide 4 o "economiza tempo", que eu não medi.

---

## anotações do professor

cada anotação cita uma frase do exemplo, marca o item (◼ passa, ◻ não passa) e explica por quê.

1. **slide 1, ponta a ponta ◼.** "faço o papel do celular da dona Cida": uma pessoa, um áudio de verdade de uma cliente, a tela, e o que ela faz com a tela: confere, confirma, e o pedido entra na lista. e o modo avião prova sozinho o "roda sem internet" do flx, sem o aluno precisar dizer.
2. **slide 1, a espera à vista.** "enquanto vocês ouviam, o app já estava transcrevendo": a demo não esconde o minuto de espera, usa ele. o vídeo de reserva é a segunda passada do ensaio, sem cortes, da mesma tag.
3. **slide 2, quanto custa ◼.** "do compartilhar até a tela pronta: 56 segundos": o número sai da execução que acabou de rodar, na tela, ao lado dos 52 s e dos 2 GB do flx. cada diferença tem causa: a carga do modelo, o formato do whisper.cpp. a estimativa errou a memória pela metade, e o aluno disse isso e corrigiu o flx.
4. **slide 3, a falha ◼.** "esse eu escolhi porque erra": a entrada, a saída sem "?", o certo. quem sofre tem nome e hora. e o erro diz algo sobre a ideia: a regra pega o que parece produto, e o que some calado só quem ouve pega. a falha vira a medida do sem3.
5. **slide 4, o que mudou ◼.** "entre esperar um minuto e errar o produto, a dona Cida espera": o que valia no sem1, o que vale agora, e o porquê, visto na própria demo (a fila) e medido (o base trocou a macaxeira). mudar de plano com motivo convence mais que cumprir o plano.
6. **o ensaio e o tempo.** "prefiro que a turma saiba por mim": a pergunta difícil mudou o fecho, não só a resposta. cinco slides, a demo rodando duas vezes seguidas no mesmo celular, 4 min 25 s.

