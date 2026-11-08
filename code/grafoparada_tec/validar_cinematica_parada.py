"""
Validação Experimental On-Device (v4.0): Cinemática de Parada, Desembarque vs Desistência, Rotina e LGPD
Projeto: GrafoParada · Frota no Vazio (VA2 - AI4Good / UFRPE)
Autor: Cauã da Cunha Lira

Executa a avaliação completa com dados reais:
1. Malha Oficial do Grande Recife (CTM/PE): 20 paradas da Linha 178/191 (TI Cabo / Porto de Suape / PE-60)
2. Sensores Físicos de Smartphone: dataset TMD (4.714 leituras reais de Acelerômetro, Giroscópio e Som)
3. Evolução de Modelos (v1.0 -> v2.0 -> v3.0 -> v4.0):
   - Classificador Neural Residual On-Device (26 atributos físicos) + Soft-Voting Temporal
   - Máquina de Estados Cinemática (FSM v3.0) com fusão de velocidade geodésica e sincronia GTFS
   - Motor On-Device de Aprendizado de Rotina (Clusterização Deslizante EWMA em 30 dias)
   - Escalabilidade Espaço-Temporal: 5 paradas (Regressão vence) vs 20 paradas da PE-60 (STGCN vence)
"""

from motor_evolucao_prototipo import main

if __name__ == "__main__":
    main()
