# -*- coding: utf-8 -*-
"""
Módulo de Domínio Científico e Algoritmos Preditivos · GrafoParada
Fundamentação Teórica Qualis A1:
- Modelagem de Abandono (Passenger Reneging): Kim, Yun & Kim (2026) · Journal of Public Transportation
- Penalidade Psicológica de Espera (Denied Boarding 1.68x): Yap & Cats (2021) · TR Part A
- Demanda Latente Não-Censurada: Tan & Ramli (2024) · Transportation
- Mecanismo Anti-Oversmoothing (Trava Híbrida Defensiva de 15 min): GrafoParada SICOE/CTM

Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)
Projeto GrafoParada · AI4Good / UFRPE
"""

from __future__ import annotations

import math
from typing import Dict, Any, List, Optional


# -----------------------------------------------------------------------------
# CONSTANTES TEÓRICAS E EMPÍRICAS CANÔNICAS
# -----------------------------------------------------------------------------
# Fator de penalidade psicológica de espera forçada por superlotação ou recusa de embarque
# Calibrado empiricamente por Yap & Cats (2021) em sistemas de transporte de alta demanda.
PENALIDADE_DENIED_BOARDING_YAP_CATS: float = 1.68

# Parâmetros da curva logística de abandono de passageiros (Kim et al., 2026)
# tau: tempo mediano de tolerância de espera na parada antes do abandono (em minutos)
# k: sensibilidade de desistência marginal (em min^-1)
RENEGING_TAU_MINUTOS_PADRAO: float = 15.0
RENEGING_K_SENSIBILIDADE: float = 0.25

# Limiar de discrepância para corte de over-smoothing da ST-GCN (em minutos)
LIMIAR_TRAVA_HIBRIDA_MINUTOS: float = 15.0

# Limiar de risco de reneging para disparo do despacho de emergência operacional CTM
LIMIAR_RENEGING_DESPACHO_EMERGENCIA: float = 0.80

# Limiar de ociosidade da frota concorrente no contra-fluxo para remanejamento
LIMIAR_OCUPACAO_LINHA_OCIOSA_PCT: float = 15.0


def calcular_tempo_percebido(
    tempo_espera_min: float,
    denied_boarding: bool = False,
    crowd_critical: bool = False
) -> float:
    """
    Calcula o tempo de espera percebido psicologicamente pelo passageiro.

    Fundamentação:
    Yap & Cats (2021) demonstram que em situações de superlotação ou recusa de embarque
    (denied boarding / queima de parada), a desutilidade psicológica da espera
    aumenta em 68% em relação à espera em condições normais de conforto.

    Args:
        tempo_espera_min: Tempo cronológico de espera medido ou projetado (minutos).
        denied_boarding: Se houve queima de parada ou recusa de embarque por lotação.
        crowd_critical: Se o veículo chegou no estado crítico (sem assentos e corredor cheio).

    Returns:
        Tempo percebido ponderado (minutos).
    """
    if tempo_espera_min < 0:
        raise ValueError("tempo_espera_min não pode ser negativo.")

    if denied_boarding or crowd_critical:
        return round(tempo_espera_min * PENALIDADE_DENIED_BOARDING_YAP_CATS, 2)
    return round(float(tempo_espera_min), 2)


def calcular_probabilidade_reneging(
    tempo_min: float,
    usar_tempo_percebido: bool = False,
    denied_boarding: bool = False,
    tau: float = RENEGING_TAU_MINUTOS_PADRAO,
    k: float = RENEGING_K_SENSIBILIDADE
) -> float:
    """
    Calcula a probabilidade de abandono da espera (Passenger Reneging).

    Fundamentação:
    Kim, Yun & Kim (2026) formalizam que a demanda latente não captada pelos validadores
    (smart card data) é censurada à direita devido ao abandono por tempo excessivo.
    A função de desistência segue distribuição sigmoide/logística centrada no limiar
    de tolerância comunitária tau:
        P(Reneging | t) = 1 / (1 + exp(-k * (t - tau)))

    Args:
        tempo_min: Tempo de espera decorrido ou previsto na parada (minutos).
        usar_tempo_percebido: Se True, aplica a penalidade de 1.68x de Yap & Cats (2021)
                              antes de avaliar a probabilidade de reneging.
        denied_boarding: Se True, sinaliza recusa de embarque para o cálculo percebido.
        tau: Mediana de tolerância de espera (default: 15.0 min).
        k: Taxa de sensibilidade de abandono (default: 0.25).

    Returns:
        Probabilidade de abandono entre 0.0 e 1.0 (arredondada em 4 casas).
    """
    if tempo_min < 0:
        raise ValueError("tempo_min não pode ser negativo.")

    t_efetivo = tempo_min
    if usar_tempo_percebido:
        t_efetivo = calcular_tempo_percebido(tempo_min, denied_boarding=denied_boarding)

    # Função logística padrão
    expoente = -k * (t_efetivo - tau)
    # Proteção numérica contra overflow
    if expoente > 60.0:
        prob = 0.0
    elif expoente < -60.0:
        prob = 1.0
    else:
        prob = 1.0 / (1.0 + math.exp(expoente))

    return round(float(prob), 4)


def avaliar_trava_hibrida_defensiva(
    tempo_gps_min: float,
    tempo_stgcn_min: float,
    threshold_min: float = LIMIAR_TRAVA_HIBRIDA_MINUTOS
) -> Dict[str, Any]:
    """
    Mecanismo anti-oversmoothing para modelos GNN espaço-temporais (ST-GCN).

    Problema Científico:
    Convoluções espaciais em grafos viários tendem a suavizar picos bruscos de atraso
    (como interdições por acidentes ou quebras de frota), espalhando ativações
    artificialmente para nós adjacentes e subestimando o atraso no nó crítico.

    Solução Operacional do GrafoParada:
    Se a discrepância absoluta entre o dado físico comprovado (GPS bruto) e a estimativa
    da GNN ultrapassar 15 minutos, o sistema aciona a trava híbrida de proteção,
    força fallback para o dado comprovado e exibe o alerta amarelo de anomalia [?].

    Args:
        tempo_gps_min: Tempo de espera bruto medido via telemetria AVL/GPS (min).
        tempo_stgcn_min: Tempo de espera inferido pelo bloco ST-GCN (min).
        threshold_min: Limiar de tolerância de discrepância (default: 15 min).

    Returns:
        Dicionário com o veredito da trava, delta absoluto e tempo a ser exibido.
    """
    delta = abs(tempo_stgcn_min - tempo_gps_min)
    trava_acionada = delta > threshold_min

    tempo_exibido = tempo_gps_min if trava_acionada else tempo_stgcn_min
    status = "ALERTA_AMARELO_OVER_SMOOTHING" if trava_acionada else "NOMINAL_STGCN"

    return {
        "trava_acionada": trava_acionada,
        "discrepancy_delta": round(delta, 2),
        "threshold_min": threshold_min,
        "tempo_gps_min": round(tempo_gps_min, 2),
        "tempo_stgcn_min": round(tempo_stgcn_min, 2),
        "tempo_exibido_min": round(tempo_exibido, 2),
        "status": status,
        "mensagem": (
            "Anomalia detectada na PE-60: ST-GCN em over-smoothing. Telemetria GPS direta forçada."
            if trava_acionada
            else "Previsão ST-GCN dentro da janela segura de convergência com telemetria GPS."
        )
    }


def avaliar_gatilho_despacho_emergencial(
    tempo_espera_min: float,
    ocupacao_concorrente_pct: float,
    denied_boarding: bool = False,
    capacidade_assentos_padrao: int = 36
) -> Dict[str, Any]:
    """
    Avalia a regra de disparo da Central de Controle Operacional CTM para inserção
    de frota no vazio (deadheading mitigation).

    Regra:
    Se P(Reneging | Yap&Cats) >= 80% E ocupação da linha concorrente ociosa <= 15%:
    Autoriza remanejamento imediato de veículo no contra-fluxo para resgate da parada,
    evitando a perda da demanda e economizando o combustível de viagens vazias.

    Args:
        tempo_espera_min: Tempo cronológico de espera na parada.
        ocupacao_concorrente_pct: Taxa percentual de ocupação da linha ociosa no contra-fluxo (0-100).
        denied_boarding: Se houve recusa prévia de embarque.
        capacidade_assentos_padrao: Capacidade nominal de assentos (default: 36).

    Returns:
        Dicionário com decisão operacional e justificativa técnica.
    """
    t_percebido = calcular_tempo_percebido(tempo_espera_min, denied_boarding=denied_boarding)
    prob_reneging = calcular_probabilidade_reneging(
        tempo_espera_min,
        usar_tempo_percebido=True,
        denied_boarding=denied_boarding
    )

    gatilho_reneging = prob_reneging >= LIMIAR_RENEGING_DESPACHO_EMERGENCIA
    gatilho_ociosidade = ocupacao_concorrente_pct <= LIMIAR_OCUPACAO_LINHA_OCIOSA_PCT

    despacho_autorizado = gatilho_reneging and gatilho_ociosidade

    return {
        "despacho_autorizado": despacho_autorizado,
        "tempo_cronologico_min": tempo_espera_min,
        "tempo_percebido_min": t_percebido,
        "probabilidade_reneging": prob_reneging,
        "probabilidade_reneging_pct": round(prob_reneging * 100.0, 1),
        "ocupacao_concorrente_pct": ocupacao_concorrente_pct,
        "capacidade_assentos": capacidade_assentos_padrao,
        "motivo": (
            "Despacho preventivo CTM aprovado: Risco de reneging crítico sob Yap & Cats (2021) "
            "com disponibilidade de frota ociosa no contra-fluxo (mitigação de deadheading)."
            if despacho_autorizado
            else "Operação nominal: Limiares de reneging e ociosidade não atendem aos critérios de quebra de escala."
        )
    }
