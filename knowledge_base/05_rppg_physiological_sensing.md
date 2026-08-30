# 05. Fotopletismografia Remota (rPPG) & Biomarcadores Fisiológicos Sem Contato
> Monitoramento de Frequência Cardíaca (BPM) e Variabilidade da Frequência Cardíaca (HRV) através de vídeo facial para detecção precoce de estresse autônomo em TEA.

---

## 1. O que é a rPPG (Remote Photoplethysmography)?

A **rPPG** é uma técnica óptica de visão computacional capaz de extrair a onda de pulso de volume sanguíneo (**BVP - Blood Volume Pulse**) diretamente de vídeos faciais capturados por câmeras RGB comuns (webcams ou smartphones), sem qualquer contato físico.

### Princípio Físico e Biológico:
A cada sístole cardíaca, o volume de sangue oxigenado que irriga os capilares sanguíneos da derme facial aumenta momentaneamente. A hemoglobina absorve seletivamente a luz verde ($\approx 520 - 580\text{ nm}$), gerando uma **micro-variação imperceptível ao olho humano na intensidade do canal Verde (G) da pele da face**.

$$\text{Sinal rPPG}(t) = \frac{1}{|ROI|} \sum_{(x,y) \in ROI} I_G(x, y, t) - \mu_G(t)$$

---

## 2. Por que a rPPG é Revolucionária no Autismo (TEA)?

| Monitoramento Tradicional (Wearables / Smartwatches) | Monitoramento por Visão Computacional (rPPG) |
| :--- | :--- |
| ❌ Exige contato físico colado à pele (smartwatches, cintas cardíacas). | ✅ **100% Livre de Contato:** Câmera posicionada a 1–2 metros de distância. |
| ❌ Causa **aversão sensorial e desconforto tátil extremo** em crianças com TEA. | ✅ Não interfere na rotina, não distrai e não gera ansiedade. |
| ❌ O aluno frequentemente arranca ou recusa o equipamento. | ✅ Processamento transparente em segundo plano na sala de aula. |

---

## 3. Biomarcadores Autônomos de Sobrecarga e Crise

A rPPG permite extrair dois indicadores neurovegetativos fundamentais do sistema nervoso autônomo (SNA):

1. **Taquicardia Reativa (Elevação Súbita de BPM):**
   * Em repouso/calma: 70 a 90 BPM.
   * Início de sobrecarga sensorial ou frustração: Salto rápido para **110 a 140+ BPM** antes de qualquer movimento corporal visível.
2. **Queda da Variabilidade da Frequência Cardíaca (HRV / RMSSD):**
   * A supressão do tônus vagal (parassimpático) gera uma queda abrupta na variabilidade entre os batimentos, sinalizando ativação da resposta de **"Luta ou Fuga" (*Fight-or-Flight*)**.

---

## 4. Repositórios e Datasets de Referência no GitHub

* 🔗 **`open-rppg`:** *A comprehensive Python toolbox for real-time and offline rPPG inference.*
* 🔗 **`advanced-rPPG`:** *Cross-platform live webcam application with MediaPipe face ROI tracking and HRV stress analysis.*
* 📊 **`UBFC-Phys` & `MCD-rPPG`:** *Bancos de dados mundiais com vídeo facial sincronizado com ECG/PPG clínico sob estresse social.*
