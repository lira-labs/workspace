import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from .models import ModelClient
from .agents import Agent

BASE_DIR = Path(__file__).resolve().parent.parent


class SimulationOrchestrator:
    """Loop multiagente com humano no circuito (human-in-the-loop).

    Fluxo de cada rodada N:
      1. Agente propositor (Gemini, remoto) apresenta o plano para a era N,
         obrigatoriamente incorporando a diretriz humana dada ao fim da rodada N-1.
      2. Agente crítico (Llama 3.2, local) contesta com restrições reais.
      3. Auditor (Qwen 2.5, local) lista Pontos Sensíveis e formula uma pergunta ao humano.
      4. O humano responde; a resposta é gravada na rodada N e vira diretriz da rodada N+1.
    O estado é persistido em outputs/<experimento>/rodada_NN.{json,md}, então cada
    rodada pode ser executada separadamente.
    """

    def __init__(self, experiment_type: str = "utopia"):
        self.experiment_type = experiment_type
        cfg = BASE_DIR / "config"
        self.output_dir = BASE_DIR / "outputs" / experiment_type
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.settings = yaml.safe_load((cfg / "settings.yaml").read_text(encoding="utf-8"))
        self.agent_configs = yaml.safe_load((cfg / f"agents_{experiment_type}.yaml").read_text(encoding="utf-8"))
        timeline_path = cfg / f"timeline_{experiment_type}.yaml"
        self.timeline = (
            yaml.safe_load(timeline_path.read_text(encoding="utf-8"))["rounds"] if timeline_path.exists() else {}
        )

        self.models: Dict[str, ModelClient] = {}
        for key, m in self.settings["models"].items():
            provider = "gemini" if m["provider"] == "google-genai" else "ollama"
            self.models[key] = ModelClient(
                provider=provider,
                model_name=m["model_name"],
                temperature=m.get("temperature", 0.7),
                max_output_tokens=m.get("max_output_tokens"),
            )

        self.agents: Dict[str, Agent] = {
            key: Agent(key, conf, self.models[conf.get("model", "gemini")])
            for key, conf in self.agent_configs["agents"].items()
        }
        self.history: List[Dict[str, Any]] = self._load_history()

    # ---------- persistência ----------
    def _load_history(self) -> List[Dict[str, Any]]:
        files = sorted(self.output_dir.glob("rodada_*.json"))
        return [json.loads(f.read_text(encoding="utf-8")) for f in files]

    def next_round_number(self) -> int:
        return len(self.history) + 1

    def pending_human_answer(self) -> bool:
        return bool(self.history) and not self.history[-1].get("human_answer")

    def record_human_answer(self, answer: str):
        """Grava a opinião/decisão humana na última rodada (vira diretriz da próxima)."""
        if not self.history:
            raise RuntimeError("Nenhuma rodada executada ainda.")
        self.history[-1]["human_answer"] = answer
        self.history[-1]["human_answered_at"] = datetime.now().isoformat(timespec="seconds")
        self._save_round(self.history[-1])

    VERIFIER_NAME = "Verificador de Fatos (Claude via Antigravity)"
    VERIFIER_MODEL = "Claude Opus 5.5 (Antigravity)"

    def record_verification(self, text: str, round_num: Optional[int] = None):
        """Grava a checagem de fatos feita pelo Claude (agente do Antigravity) numa rodada.

        Requisito: Antigravity aberto e cota diária do Claude. O texto é repassado como
        'correções' no contexto da rodada seguinte, para que erros não se propaguem.
        """
        r = self.history[-1] if round_num is None else self.history[round_num - 1]
        r["verificador"] = {
            "name": self.VERIFIER_NAME,
            "model": self.VERIFIER_MODEL,
            "response": text.strip(),
            "verified_at": datetime.now().isoformat(timespec="seconds"),
        }
        self._save_round(r)

    # ---------- execução ----------
    def _context(self, round_num: int) -> str:
        era = self.timeline.get(round_num, {})
        lines = [
            f"Experimento: {self.agent_configs.get('theme', self.experiment_type)}",
            f"Rodada {round_num}/20 — {era.get('era', '')}",
            f"Desafio histórico desta rodada: {era.get('desafio', '')}",
        ]
        if self.history:
            lines.append("\nDecisões humanas já tomadas (devem ser respeitadas e ter continuidade):")
            for r in self.history:
                if r.get("human_answer"):
                    lines.append(f"- Rodada {r['round']}: {r['human_answer']}")
            prev = self.history[-1]
            lines.append(f"\nSíntese do auditor na rodada anterior:\n{prev['auditor']['response'][:800]}")
            if prev.get("verificador"):
                lines.append(
                    "\nCORREÇÕES DO VERIFICADOR DE FATOS na rodada anterior (não repita os erros apontados):\n"
                    f"{prev['verificador']['response'][:1500]}"
                )
            if prev.get("human_answer"):
                lines.append(f"\nDIRETRIZ HUMANA PARA ESTA RODADA (obrigatória): {prev['human_answer']}")
        lines.append("\nNão repita argumentos de rodadas anteriores; avance a história.")
        return "\n".join(lines)

    def run_round(self) -> Dict[str, Any]:
        if self.pending_human_answer():
            raise RuntimeError("A rodada anterior ainda aguarda a resposta humana.")
        round_num = self.next_round_number()
        p_agent, c_agent, a_agent = list(self.agents.values())[:3]
        ctx = self._context(round_num)

        resp_1 = p_agent.act(
            f"{ctx}\n\nApresente sua proposta concreta para esta era (até 4 parágrafos), "
            "citando dados, instituições e especialistas reais quando possível."
        )
        resp_2 = c_agent.act(
            f"{ctx}\n\nProposta de {p_agent.name}:\n{resp_1}\n\n"
            "Responda em português, exatamente neste formato:\n"
            "PROBLEMAS NOVOS: (2 problemas que o Arquiteto NÃO mencionou, cada um com ator/dado concreto da época)\n"
            "CHECAGEM DE FATOS: (1 afirmação do Arquiteto que pode estar errada, exagerada ou inventada, e por quê; "
            "se não houver, escreva 'nenhuma identificada')\n"
            "CONTRAPROPOSTA: (1 alternativa mais realista, em 2 frases)"
        )
        prev_metrics = self.history[-1]["auditor"]["response"] if self.history else ""
        resp_3 = a_agent.act(
            f"{ctx}\n\nProposta de {p_agent.name}:\n{resp_1}\n\nCrítica de {c_agent.name}:\n{resp_2}\n\n"
            + (f"(Para comparação, sua avaliação anterior foi:\n{prev_metrics[:600]})\n\n" if prev_metrics else "")
            + "Responda em português, exatamente neste formato:\n"
            "RESUMO: (2 frases sobre o que foi proposto e criticado nesta rodada)\n"
            "PONTOS SENSÍVEIS: (até 3, cada um citando a medida específica)\n"
            "MÉTRICAS: Viabilidade X% | Equidade Social Y% — (1 frase justificando e dizendo se subiu ou caiu)\n"
            "PERGUNTA AO HUMANO: (1 pergunta aberta pedindo a opinião do humano sobre o dilema central da rodada)\n"
            "CAMINHOS POSSÍVEIS:\n"
            "  1) (caminho realista) — Ganho: ... | Custo: ...\n"
            "  2) (caminho realista diferente) — Ganho: ... | Custo: ...\n"
            "  3) (caminho realista diferente) — Ganho: ... | Custo: ..."
        )

        era = self.timeline.get(round_num, {})
        round_data = {
            "round": round_num,
            "experiment": self.experiment_type,
            "era": era.get("era", ""),
            "desafio": era.get("desafio", ""),
            "directive_in": self.history[-1].get("human_answer") if self.history else None,
            "agent_1": {"name": p_agent.name, "model": p_agent.client.label, "response": resp_1},
            "agent_2": {"name": c_agent.name, "model": c_agent.client.label, "response": resp_2},
            "auditor": {"name": a_agent.name, "model": a_agent.client.label, "response": resp_3},
            "human_answer": None,
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }
        self.history.append(round_data)
        self._save_round(round_data)
        return round_data

    def _save_round(self, r: Dict[str, Any]):
        n = str(r["round"]).zfill(2)
        (self.output_dir / f"rodada_{n}.json").write_text(
            json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md = f"""# Rodada {r['round']} — {r['era']}
**Experimento:** {self.experiment_type.upper()}  
**Desafio:** {r['desafio']}  
**Diretriz humana recebida:** {r.get('directive_in') or '— (rodada inicial)'}

## 🏛️ {r['agent_1']['name']} · `{r['agent_1']['model']}`
{r['agent_1']['response']}

---

## ⚡ {r['agent_2']['name']} · `{r['agent_2']['model']}`
{r['agent_2']['response']}

---

## ⚖️ {r['auditor']['name']} · `{r['auditor']['model']}`
{r['auditor']['response']}

---
{self._verifier_md(r)}
## 👤 Resposta humana (diretriz para a rodada {r['round'] + 1})
{r.get('human_answer') or '_Aguardando resposta._'}
"""
        (self.output_dir / f"rodada_{n}.md").write_text(md, encoding="utf-8")

    @staticmethod
    def _verifier_md(r: Dict[str, Any]) -> str:
        v = r.get("verificador")
        if not v:
            return "\n## 🔎 Verificador de Fatos\n_Aguardando verificação (requer Antigravity)._\n\n---\n\n"
        return f"\n## 🔎 {v['name']} · `{v['model']}`\n{v['response']}\n\n---\n\n"
