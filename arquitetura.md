# GrafoParada · Fluxograma e Arquitetura

O caminho de ponta a ponta: do gesto do passageiro consultando o ponto no celular até a conferência do analista do consórcio e o remanejamento de horários que reduz a espera na parada. Artefato **fluxograma e arquitetura** da disciplina AI4Good ([guia](https://lucassf.pages.dev/ai4good/artefatos/3-fluxograma-e-arquitetura)).

Formas: **pessoa** `([ ])` · **IA** `{{ }}` · **regra** `[ ]`. Caixas: onde cada peça roda.

```mermaid
flowchart TD
    subgraph CEL_P["celular do passageiro (app de consulta de parada)"]
        A(["1 · passageiro abre o mapa da parada no celular para ver se o ônibus da linha vem"])
        J(["10 · passageiro na parada consulta o app e recebe o ônibus passando no intervalo reduzido"])
    end

    subgraph AVL_BUS["frota de ônibus / API pública de GPS e GTFS (CTM Grande Recife)"]
        BUS["sinal aberto de GPS do veículo a cada 30 s + tabela GTFS programada"]
    end

    subgraph SRV_CTM["computador/servidor local do analista no consórcio: tudo roda aqui em CPU"]
        B["2 · agrupar consultas por parada em janelas de 10 min e descartar cliques repetidos na RAM"]
        C["3 · cruzar o GPS aberto do ônibus com o raio da parada para medir o dwell time (parou >= 15 s = embarque; passou direto = parada queimada ou vazia)"]
        D["4 · comparar o horário do GPS com a tabela GTFS programada para calcular o atraso atual em minutos"]
        E["5 · normalizar os dados (z-score) das últimas 2 horas e montar a matriz do grafo viário das paradas (NetworkX)"]
        F{{"6 · prever a espera nas paradas para os próximos 10, 20 e 30 min propagando o atraso pelo corredor (STGCN)"}}
        G["7 · marcar alerta de desistência nas paradas onde a espera prevista passa de 40 min e apontar horários de veículos rodando no vazio"]
        H(["8 · a tela abre no alerta com o atraso real do GPS bruto ao lado; o analista do consórcio confere e aprova a troca de horário"])
        I["9 · gerar a nova tabela horária GTFS remanejando a viagem ociosa para o horário de sufoco"]
        DB[("histórico agregado da parada: contagem de consultas por 10 min, espera em min e dwell time (sem ID de celular)")]
    end

    A -- "consulta ao ponto (ID temporário + parada)" --> B
    BUS -- "coordenadas GPS e horários GTFS" --> C
    C --> D --> E
    B --> DB --> E
    E --> F --> G --> H --> I
    I -- "ordem de serviço atualizada" --> BUS
    I -- "nova tabela horária publicada no GTFS" --> J
```

## os dados

| dado pessoal | de quem é | onde fica | quem vê | por quanto tempo | quando é apagado |
|:--|:--|:--|:--|:--|:--|
| localização e IP/ID temporário da consulta ao ponto | passageiro | memória RAM do servidor local (passo 2) | ninguém (apenas a regra de filtro) | no máximo 10 minutos (duração da janela) | apagado da RAM ao fechar a janela de 10 min; no disco (`DB`) só entra o número inteiro total de consultas da parada |
| prefixo do veículo e coordenada GPS em tempo real | operação / motorista em turno | memória de cálculo (passos 3 e 4) no servidor local | analista de planejamento do consórcio (apenas no painel do passo 8) | durante o dia operacional | ao consolidar o histórico diário da parada; fica guardado apenas o atraso e o *dwell time* por parada e horário, sem vínculo com o motorista |
| registro de decisões do analista (alertas aceitos ou recusados) | analista do consórcio | banco local (`DB`) no computador do consórcio | o próprio analista e a auditoria técnica do projeto | até o fim do experimento | ao final da validação do experimento |

Do aparelho do passageiro sai apenas a requisição normal de consulta da parada que o aplicativo de ônibus já envia hoje; nenhum nome, telefone ou histórico individual de rotas é coletado ou salvo em disco.
