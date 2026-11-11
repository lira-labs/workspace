# sem2 · exemplo quase bom / sem alma

> roteiro do [seminário · iteração 2, demonstração](../4-seminario-demonstracao.md), do mesmo projeto do
> [excelente](excelente.md). parece pronto, mas não convence. as anotações do professor estão no fim.

**link dos slides:** no drive da turma.

**a versão que roda:** a última.

**a máquina:** o vídeo, no notebook.

**a gravação de reserva:** a demo já é o vídeo.

## as quatro frases, sem IA

1. **a demo:** mostro o rastro da banca funcionando num vídeo, do áudio até o pedido.
2. **o custo:** é de graça e leve: roda no celular, com uns 2 GB.
3. **a falha:** como toda IA, às vezes erra com barulho, mas a feirante pode corrigir.
4. **o que mudou:** trocamos o modelo small pelo base e melhoramos a tela.

## slide 1 · capa · 15 s

- **aparece:** "rastro da banca: IA de voz para a feira", nome, orientador.
- **eu falo:** "bom dia, vou mostrar a demo do rastro da banca."

## slide 2 · demo · 70 s

- **aparece:** um vídeo de 50 s, com cortes, em velocidade 2× e música de fundo: três áudios entram, três pedidos saem certos, a lista aparece. os áudios são os de voz sintética do tec.
- **eu falo:** "gravei ontem, porque a internet da sala pode falhar. aqui a feirante recebe o áudio, e o app gera o pedido automaticamente. como vocês podem ver, funciona muito bem."

## slide 3 · custo · 40 s

- **aparece:** "custo: R$ 0 · ~2 GB de RAM · rápido".
- **eu falo:** "o custo é zero, porque roda no celular. segundo a documentação do whisper, o modelo usa uns 2 GB, e no celular é rápido."

## slide 4 · limitações · 30 s

- **aparece:** "ruído · sotaque · a IA ainda pode errar".
- **eu falo:** "como toda IA, às vezes erra quando tem barulho, mas a feirante pode corrigir na tela. com modelos maiores, isso vai melhorar."

## slide 5 · evolução desde o sem1 · 40 s

- **aparece:** "small → base · nova tela · ícones novos · modo escuro".
- **eu falo:** "desde o sem1, trocamos o small pelo base, que é melhor, e melhoramos a interface."

## slide 6 · próximos passos · 20 s

- **aparece:** "colheita · pix · iOS · obrigado!"
- **eu falo:** "nos próximos passos, vamos adicionar a colheita e o pagamento. obrigado!"

**tempo total, cronometrado, com a demo rodando:** 3 min 35 s, uma vez, passando o vídeo.

## ensaio cético

**a pergunta mais difícil:** "por que a demo não é ao vivo?" respondi que a internet da sala pode cair.

**o que eu mudei por causa dela:** nada. a IA concordou que o vídeo é mais seguro.

---

## anotações do professor

cada anotação cita uma frase do exemplo, marca o item (◼ passa, ◻ não passa) e explica por quê.

1. **slide 2, a demo que não roda ◻.** "gravei ontem, porque a internet da sala pode falhar": o app não usa internet, e quem diz isso é o flx do próprio projeto. o vídeo editado, em 2×, com voz sintética, não prova que a versão roda do repositório nem que aguenta uma entrada real. e não tem ninguém nele: "a feirante" não é a dona Cida. o mínimo era ao vivo, e o vídeo só valia se a máquina falhasse, sem cortes. compare com o modo avião no [excelente](excelente.md).
2. **slide 3, o custo copiado ◻.** "segundo a documentação do whisper, uns 2 GB": é a estimativa do flx repetida, não medida. e nem é a do modelo que ele diz usar: o flx dá ~2 GB para o small e 1 GB para o base. "no celular é rápido" contradiz os 2,89 vezes do exp, e o vídeo em 2× esconde justamente esse número. o excelente mediu e achou metade da memória.
3. **slide 4, a falha genérica ◻.** "às vezes erra quando tem barulho": não tem entrada, saída errada, o certo, nem quem sofre. o "dois peixes" estava no flx do próprio projeto, pronto para ser mostrado. e "a feirante pode corrigir" só vale se ela ouvir o áudio: o erro que some calado é exatamente o que o sem3 precisa medir.
4. **slide 5, a mudança sem porquê ◻.** "trocamos o small pelo base, que é melhor": melhor em quê, e para quem? o base é mais rápido e erra mais produto, e a escolha entre os dois é a decisão que importa. "nova tela, ícones novos, modo escuro" é lista, não decisão. compare com "entre esperar um minuto e errar o produto, a dona Cida espera".
5. **o ensaio e o tempo.** "a IA concordou que o vídeo é mais seguro" e "uma vez, passando o vídeo": a pergunta certa apareceu, mas a resposta não fechava com o flx, e nada mudou. a demo de verdade nunca foi ensaiada na máquina da sala. e a colheita, que era o diferencial no sem1, virou um próximo passo sem uma palavra sobre isso.
