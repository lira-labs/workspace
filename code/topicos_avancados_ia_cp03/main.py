"""CLI do experimento AI4Good (CP-03).

Uso:
  python main.py utopia                 # modo interativo: roda as 20 rodadas pedindo sua opinião a cada uma
  python main.py utopia --step          # roda só a próxima rodada e para (aguarda resposta)
  python main.py utopia --answer "..."  # grava sua resposta para a última rodada
"""
import argparse
import sys
from src.orchestrator import SimulationOrchestrator


def show(r):
    print(f"\n{'=' * 70}\nRODADA {r['round']} — {r['era']}\n{'=' * 70}")
    for k in ("agent_1", "agent_2", "auditor"):
        print(f"\n--- {r[k]['name']} [{r[k]['model']}] ---\n{r[k]['response']}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("experiment", choices=["utopia", "distopia"])
    ap.add_argument("--step", action="store_true")
    ap.add_argument("--answer")
    ap.add_argument("--verify", help="arquivo .md com a checagem de fatos do Claude (Antigravity)")
    ap.add_argument("--round", type=int, help="rodada alvo do --verify (padrão: última)")
    args = ap.parse_args()

    orch = SimulationOrchestrator(args.experiment)
    if args.verify:
        from pathlib import Path
        orch.record_verification(Path(args.verify).read_text(encoding="utf-8"), args.round)
        print(f"Verificação gravada na rodada {args.round or orch.history[-1]['round']}.")
        return
    if args.answer:
        orch.record_human_answer(args.answer)
        print(f"Resposta gravada na rodada {orch.history[-1]['round']}.")
        return
    if args.step:
        show(orch.run_round())
        return

    while orch.next_round_number() <= 20:
        if orch.pending_human_answer():
            orch.record_human_answer(input("\n👤 Sua opinião/decisão: ").strip())
        if orch.next_round_number() > 20:
            break
        show(orch.run_round())
    if orch.pending_human_answer():
        orch.record_human_answer(input("\n👤 Sua reflexão final: ").strip())


if __name__ == "__main__":
    main()
