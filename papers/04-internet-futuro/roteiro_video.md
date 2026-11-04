# 🎬 Roteiro do Vídeo de Apresentação (2ª VA · Internet do Futuro)
> **Tema:** Telessaúde Segura no Interior: Criptografia Pós-Quântica com Satélites LEO, Computação de Borda e Zero Trust  
> **Aluno:** Cauã Lira  
> **Disciplina:** Internet do Futuro · Profa. Jeisa Pereira de Oliveira Domingues  
> **Duração Total Estimada:** **8 minutos e 30 segundos a 9 minutos** (com margem de segurança de 1 minuto para o teto de 10 min).

---

## 💡 Dicas Gerais para a Gravação
1. **Linguagem:** Fale com calma, em tom de conversa, como se estivesse explicando o projeto para um colega na sala de aula. Evite ler de forma robotizada; use os tópicos como guia natural.
2. **Visual dos Slides:** Use as próprias ilustrações e tabelas que já geramos no documento (estão todas em `papers/04-internet-futuro/figures/`). Elas dão um ar profissional e visualmente acolhedor.
3. **Câmera:** Se for gravar com câmera aberta no cantinho da tela (estilo OBS, Loom ou Google Meet gravando), olhe para a lente periodicamente para criar conexão com quem está assistindo.

---

## ⏱️ Cronograma Slide a Slide

```
[00:00 - 00:50] Slide 1: Capa e Boas-Vindas
[00:50 - 02:00] Slide 2: O Problema Real (Saúde no Interior e a Ameaça Quântica)
[02:00 - 03:15] Slide 3: A Nossa Tecnologia Base (Criptografia Pós-Quântica)
[03:15 - 04:30] Slide 4: As Tecnologias Parceiras (Satélites LEO, Edge e Zero Trust)
[04:30 - 06:00] Slide 5: A Arquitetura Proposta em Camadas
[06:00 - 07:15] Slide 6: Cenário Prático (O Atendimento do Seu José)
[07:15 - 08:30] Slide 7: Benefícios, Limitações e Como Avaliar na Prática
[08:30 - 09:15] Slide 8: Viabilidade Real e Próximos Passos
[09:15 - 09:40] Slide 9: Referências e Encerramento
```

---

### Slide 1: Capa e Boas-Vindas (00:00 - 00:50 · ~50 segundos)
- **Visual do Slide:**
  - Brasão da UFRPE no topo.
  - Título em destaque: *Telessaúde Segura no Interior: Criptografia Pós-Quântica com Satélites LEO, Computação de Borda e Zero Trust*.
  - Seu nome: Cauã Lira · Licenciatura em Computação · UFRPE.
  - Profa. Jeisa Pereira de Oliveira Domingues · Disciplina: Internet do Futuro.
- **O que falar:**
  > *"Olá, professora Jeisa, olá colegas! Meu nome é Cauã Lira e hoje eu venho apresentar a proposta de projeto teórico da nossa 2ª VA de Internet do Futuro.  
  > Na 1ª VA, o tema do meu seminário foi a **Criptografia Pós-Quântica**. Para este projeto, eu decidi tirar essa tecnologia do papel e da teoria de bancos e grandes empresas, trazendo-a para um desafio muito real e humano do nosso país: **como proteger os exames e prontuários médicos de pessoas atendidas por telessaúde no interior mais isolado do Brasil**."*

---

### Slide 2: O Problema que Estamos Investigando (00:50 - 02:00 · ~1 min 10 s)
- **Visual do Slide:**
  - Lado esquerdo: Imagem do posto de saúde no sertão com a antena no telhado (`figures/posto_sertao.jpg`).
  - Lado direito: Ilustração do ataque *colha agora, descriptografe depois* (`figures/colha_agora.jpg`).
  - Destaque em texto simples: *Dados de saúde duram décadas. A criptografia atual tem prazo de validade.*
- **O que falar:**
  > *"Desde 2022, a telessaúde é lei no Brasil. Ela é uma bênção para quem mora no sertão pernambucano ou em comunidades ribeirinhas da Amazônia, porque permite que uma pessoa num posto simples seja atendida por um médico especialista no Recife ou em São Paulo.  
  > Só que nesses lugares não chega fibra óptica nem 4G confiável. A única forma prática de conectar esses postos hoje é pela internet via satélite.  
  > E aí surge um perigo silencioso: um exame do coração, um pré-natal ou um prontuário médico são informações íntimas que precisam ficar em segredo pela vida inteira da pessoa — 30, 50, 70 anos.  
  > Hoje esses dados trafegam protegidos pela criptografia comum, como RSA. Mas quando os computadores quânticos ficarem fortes, eles vão quebrar essa proteção.  
  > E o pior: já existe o golpe chamado 'colha agora, abra depois'. Criminosos ou governos podem interceptar o sinal do satélite hoje, guardar esses dados num cofre digital e esperar o computador quântico do futuro para abrir tudo. Por isso, esperar o computador quântico chegar para só então agir é chegar atrasado."*

---

### Slide 3: A Tecnologia Base — Criptografia Pós-Quântica (02:00 - 03:15 · ~1 min 15 s)
- **Visual do Slide:**
  - Foto do computador quântico real (`figures/ibm_quantum.jpg`).
  - Tabela comparativa simplificada de tamanho de chaves (X25519 vs ML-KEM e Ed25519 vs ML-DSA).
  - Ponto-chave: *Funciona nos computadores de hoje, mas resiste aos computadores quânticos.*
- **O que falar:**
  > *"A nossa tecnologia do seminário é a **Criptografia Pós-Quântica**.  
  > Muita gente confunde com computador quântico, mas a beleza dela é que ela roda nos computadores, servidores e celulares normais de hoje. Ela usa uma matemática diferente — baseada em reticulados — que é impossível de ser quebrada tanto por supercomputadores clássicos quanto por computadores quânticos.  
  > Em 2024, o NIST oficializou os padrões mundiais: o **ML-KEM**, para combinar chaves secretas de conexão, e o **ML-DSA**, para fazer assinaturas digitais que comprovam que o exame não foi adulterado.  
  > Mas como eu apontei lá na 1ª VA, ela tem uma limitação: as chaves são bem maiores e mais pesadas. Uma chave clássica tem 32 bytes; a pós-quântica passa de mil bytes. Um aparelho fraquinho ou com pouca bateria não aguenta rodar isso sozinho. E é aqui que entram os nossos colegas e as tecnologias parceiras."*

---

### Slide 4: As Tecnologias Complementares (03:15 - 04:30 · ~1 min 15 s)
- **Visual do Slide:**
  - Tabela dos 4 papéis (`tab:papeis` do documento):
    - 🛰️ **Satélites LEO** (Tema 8 · Alexander): Camada de Transporte.
    - 🖥️ **Edge Computing** (Tema 2 · Daniel): Camada de Borda e Processamento Local.
    - 🛡️ **Zero Trust** (Tema 9 · João Victor V.): Camada Transversal de Acesso.
    - 🔐 **Criptografia Pós-Quântica** (Tema 17 · Cauã): Camada de Proteção.
- **O que falar:**
  > *"Nenhuma tecnologia resolve tudo sozinha. Para fechar o ciclo, trouxemos três temas apresentados pelos colegas na disciplina:  
  > Primeiro, os **Satélites de Órbita Baixa (LEO)**, do seminário do Alexander. Eles voam pertinho da Terra, entregando internet rápida e com pouco atraso para lugares onde não há estradas nem cabos.  
  > Segundo, a **Computação de Borda (Edge Computing)**, do seminário do Daniel. Colocamos um mini servidor dentro do posto de saúde. É esse servidor que faz o trabalho pesado de rodar a criptografia pós-quântica, tirando o peso das costas dos aparelhos mais simples.  
  > E terceiro, o **Zero Trust**, do seminário do João Victor Vasconcelos. No Zero Trust, ninguém tem confiança cega: o sistema confere quem é o aparelho, quem é a técnica de enfermagem e quem é o médico a cada clique.  
  > Reparem como uma cobre o ponto fraco da outra: a borda resolve o peso da criptografia; a criptografia impede que a dona do satélite leia os dados de saúde; e o Zero Trust impede que um invasor passeie livremente pelo sistema."*

---

### Slide 5: A Arquitetura Proposta em Camadas (04:30 - 06:00 · ~1 min 30 s)
- **Visual do Slide:**
  - O diagrama da arquitetura em 4 camadas horizontais + Zero Trust (`figures/arquitetura` em TikZ).
  - Fotos de apoio: Antena de satélite no telhado (`figures/starlink_antena.jpg`).
- **O que falar:**
  > *"Aqui está o desenho da nossa arquitetura. Ela foi dividida em quatro camadas lineares e uma transversal:  
  > **Camada 1 - Dispositivos:** É onde o atendimento começa. São aparelhos simples como um eletrocardiógrafo portátil ou um tablet. Eles se conectam pelo Wi-Fi local do posto e não precisam de nada pesado.  
  > **Camada 2 - Borda:** O coração do sistema. Um mini computador local recebe o exame, assina digitalmente com ML-DSA e abre um túnel seguro combinando a chave com ML-KEM. Se chover e a internet cair, ele guarda tudo numa fila local sem parar o atendimento.  
  > **Camada 3 - Transporte:** A antena no telhado e os satélites LEO. Eles são o carteiro da internet. Como o pacote já sai da borda 100% blindado pela criptografia pós-quântica, a empresa do satélite só enxerga bytes indecifráveis.  
  > **Camada 4 - Central e Nuvem:** Fica no hospital de referência ou na Secretaria de Saúde. O servidor central valida a assinatura do exame e armazena o prontuário com proteção pós-quântica definitiva para as próximas décadas.  
  > E por trás de tudo, a camada **Zero Trust** vigia cada etapa, garantindo privilégio mínimo para cada usuário."*

---

### Slide 6: Cenário Prático — O Atendimento do Seu José (06:00 - 07:15 · ~1 min 15 s)
- **Visual do Slide:**
  - Ilustração do Seu José no posto com a técnica e a teleconsulta (`figures/seu_jose_ecg.jpg`).
  - O infográfico dos 6 passos (`fig:caminho` do documento).
- **O que falar:**
  > *"Para ver como isso funciona na prática da vida real, imaginem o Seu José, de 67 anos, que mora num distrito rural e chega ao posto sentindo dor no peito.  
  > Em seis passos simples:  
  > 1. A técnica de enfermagem faz o eletrocardiograma portátil.  
  > 2. O Zero Trust valida que aquele aparelho e aquela técnica estão autorizados.  
  > 3. O servidor de borda assina o traçado do coração com ML-DSA e guarda uma cópia segura no posto.  
  > 4. O exame viaja pelo satélite LEO dentro do túnel pós-quântico híbrido.  
  > 5. No Recife, o servidor do hospital recebe o exame e confere que ninguém alterou uma linha sequer.  
  > 6. O cardiologista de plantão abre o laudo e entra em chamada de vídeo com o posto para orientar o socorro imediato do Seu José.  
  > Tudo rápido, com latência baixa e com a certeza de que o histórico cardíaco do Seu José nunca poderá ser exposto."*

---

### Slide 7: Benefícios, Limitações e Métricas de Avaliação (07:15 - 08:30 · ~1 min 15 s)
- **Visual do Slide:**
  - Tabela de Métricas Teóricas (`tab:metricas`).
  - Matriz FOFA / SWOT simplificada (`fig:fofa`).
- **O que falar:**
  > *"Como em qualquer projeto de engenharia honesto, precisamos falar dos benefícios e também das limitações:  
  > O grande benefício é a imunidade quântica imediata e o cumprimento rigoroso da LGPD para dados sensíveis.  
  > Por outro lado, as limitações existem: as chaves são maiores, os satélites sofrem atenuação em chuvas fortes e existe uma dependência de constelações privadas de satélites.  
  > Para saber se o projeto funciona na prática, propomos quatro métricas de teste num posto piloto:  
  > 1. **Tempo de Conexão:** medimos se o aperto de mão pós-quântico adiciona atraso perceptível na chamada de vídeo (estudos mostram que fica abaixo de 5%).  
  > 2. **Sobrecarga de Dados:** as chaves somam apenas cerca de 4,5 KB, o que num exame de ECG ou ultrassom representa menos de 0,1% de impacto na banda.  
  > 3. **Uso de CPU do Servidor:** comprovar que um mini computador comum de R$ 1.500 aguenta rodar os algoritmos com folga.  
  > 4. **Resiliência pós-falha:** desligar a antena por 1 hora e garantir que 100% dos exames em fila cheguem intactos ao hospital quando a conexão voltar."*

---

### Slide 8: Viabilidade e Conclusão (08:30 - 09:15 · ~45 segundos)
- **Visual do Slide:**
  - Foto conceitual de resiliência (`figures/chuva_borda.jpg`).
  - Tópicos-chave: *Tecnicamente viável hoje (NIST 2024 + Starlink comercial + mini PCs baratos). Próximo passo: projeto piloto com SUS e Universidades.*
- **O que falar:**
  > *"Em conclusão: o projeto é tecnicamente viável hoje. Não precisamos esperar 2035. Os algoritmos do NIST já estão prontos, os satélites LEO já cobrem o interior do Brasil e mini computadores de baixo custo existem em abundância.  
  > O desafio real é de gestão pública: levar energia solar estável aos postos, capacitar os profissionais de saúde e criar parcerias entre universidades e o SUS para projetos piloto.  
  > A criptografia pós-quântica não foi feita para ficar trancada em data centers de bancos ricos; ela pode e deve ser usada para salvar vidas e proteger a dignidade do cidadão mais humilde do nosso país."*

---

### Slide 9: Referências e Encerramento (09:15 - 09:40 · ~25 segundos)
- **Visual do Slide:**
  - Principais referências: NIST FIPS 203/204 (2024), Bernstein & Lange (Nature 2017), Del Portillo (Acta Astronautica 2019), Shi et al. (IEEE IoT 2016), Rose et al. (NIST ZTA 2020), Lei da Telessaúde e LGPD.
  - E-mail para contato: `caua.lira@ufrpe.br`.
  - Mensagem final: *Obrigado pela atenção!*
- **O que falar:**
  > *"Aqui estão as referências que fundamentam nosso trabalho, cobrindo cada uma das tecnologias apresentadas. Agradeço à professora Jeisa pela disciplina e aos colegas pelos seminários que enriqueceram esta arquitetura. Muito obrigado a todos e fico à disposição para dúvidas!"*

---
