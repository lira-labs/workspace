# CLAIMS AND EVIDENCE · Compasso Cognitivo

> Regra inegociável: nenhuma afirmação da Seção 2 ou 3 entra na Seção 1/4/5 sem evidência correspondente.

## 1. Fatos Confirmados de Implementação (Verificados no Código)
- O sistema alvo atual é Windows desktop (`app.py` usa Win32 API; `tray.ps1` usa WPF).
- A telemetria de janelas e contadores de teclado/mouse roda localmente sem armazenar caracteres digitados.
- A percepção visual usa MediaPipe Holistic no navegador local (478 pontos faciais, 33 corporais), com calibração adaptativa.
- O alerta de "smartphone" na versão atual é uma heurística geométrica (`gaze_direction === 'down'` ou `head_pitch > 15°` por $\ge 5\text{ s}$), e não um detector YOLO.
- O copiloto zero-clique contínuo é um motor determinístico de regras e estatísticas locais (mediana de ciclos, detecção de travamento, silenciamento em jogos/hobbies, respiração 4-4-4).
- A revisão visual por IA usa Ollama local (`gemma3:4b` no backend, teste de fumaça registrado em `44,1 s` em `OLLAMA.md`) ou API externa OpenAI mediante chave e consentimento explícito do usuário.
- Suíte automatizada registrada em `VALIDACAO.md`: 23 testes Python aprovados + testes JS de visão, extensão e UI com câmera sintética.

## 2. Afirmações que Exigem Validação Experimental (Pendentes: Benchmark + Estudo $N=15$)
- Consumo real de CPU (%) e RAM (MB) do `Compasso.exe` atualizado (`compasso-aprovacao`).
- Latência real ponta a ponta do loop MediaPipe e ausência de tráfego externo por auditoria de rede.
- Acurácia e taxa de falsos positivos da heurística de olhar inferior (óculos, iluminação real, leitura em papel).
- Eficácia da fusão SO + webcam frente a modalidades isoladas para detectar fragmentação/travamento.
- Oportunidade e baixa intrusividade das intervenções JITAI e do gadget WPF ($N=15$).
- Acerto na diferenciação entre estudo, comunicação e hobby/jogos no cotidiano.
- Usabilidade (SUS) e percepção de suporte à autorregulação (Likert SRL) com $N=15$ participantes.

## 3. Afirmações Proibidas (Nunca Assumir Sem Ensaio Clínico/Longitudinal Dedicado)
- Precisão clínica ou diagnóstico médico/psicológico de TDAH, ansiedade ou fadiga cognitiva.
- Detecção validada de uso de smartphone por visão computacional de objetos (YOLO11n).
- Garantia comprovada de aumento de notas ou aprendizado em longo prazo.
- Inferência direta de "concentração" ou "mind wandering" com a mesma validade de estudos com probes cognitivos (e.g., Hutt et al., 2024) sem validação comparativa.
- Execução 100% offline quando o usuário escolhe explicitamente o provedor OpenAI.
