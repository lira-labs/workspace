# GrafoParada · Fluxograma e Arquitetura

O caminho de ponta a ponta: do gesto do passageiro consultando o ponto no celular até a conferência do analista do consórcio e o remanejamento de horários que reduz a espera na parada. Artefato **fluxograma e arquitetura** da disciplina AI4Good ([guia](https://lucassf.pages.dev/ai4good/artefatos/3-fluxograma-e-arquitetura)).

Formas: **pessoa** `([ ])` · **IA** `{{ }}` · **regra** `[ ]`.

```mermaid
flowchart TD
    A(["1 · passageiro abre o mapa da parada no celular para ver se o ônibus da linha vem"])
    B["2 · agrupar consultas por parada em janelas de 10 min e descartar cliques repetidos do mesmo aparelho"]
    C["3 · cruzar o GPS aberto do ônibus com o raio da parada para medir o dwell time (parou >= 15 s = embarque; passou direto = parada queimada ou vazia)"]
    D["4 · comparar o horário do GPS com a tabela GTFS programada para calcular o atraso atual em minutos"]
    E["5 · normalizar os dados (z-score) das últimas 2 horas e montar a matriz do grafo viário das paradas (NetworkX)"]
    F{{"6 · prever a espera nas paradas para os próximos 10, 20 e 30 min propagando o atraso pelo corredor (STGCN)"}}
    G["7 · marcar alerta de desistência nas paradas onde a espera prevista passa de 40 min e apontar horários de veículos rodando no vazio"]
    H(["8 · a tela abre no alerta com o atraso real do GPS bruto ao lado; o analista do consórcio confere e aprova a troca de horário"])
    I["9 · gerar a nova tabela horária GTFS remanejando a viagem ociosa para o horário de sufoco"]
    J(["10 · passageiro na parada consulta o app e recebe o ônibus passando no intervalo reduzido"])

    A --> B
    B --> E
    C --> D --> E
    E --> F --> G --> H --> I --> J
```
