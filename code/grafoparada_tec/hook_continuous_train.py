# -*- coding: utf-8 -*-
"""
Hook / Executor de Treino Contínuo & Integridade · GrafoParada
==============================================================
Modo rápido (`--quick`, padrão em hooks síncronos de lifecycle):
  - Valida o banco SQLite (`db_manager.init_db()` + `get_db_summary()`),
  - Confirma presença e cobertura 393/393 em `gtfs_schedules.json` e `model_training_status.json`,
  - Garante resposta em < 1s sem bloquear o ciclo do agente.

Modo treino (`--retrain`, para `/schedule`, cron ou gatilho manual):
  - Garante `gtfs_schedules.json` atualizado (compila via `compilar_horarios_gtfs.py` se ausente),
  - Executa `treinar_modelo_continuo.run_continuous_training()` (ST-GCN + OLS + Persistência),
  - Registra execução em `training_runs` e atualiza `code/grafoparada_web/data/model_training_status.json`.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
WEB_DATA_DIR = BASE_DIR.parent / "grafoparada_web" / "data"
SCHEDULES_JSON = WEB_DATA_DIR / "gtfs_schedules.json"
STATUS_JSON = WEB_DATA_DIR / "model_training_status.json"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from db_manager import get_db_summary, init_db  # noqa: E402


def _parse_iso_age_hours(iso_str: str | None) -> float | None:
    if not iso_str:
        return None
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        delta = datetime.now(timezone.utc) - dt
        return max(0.0, delta.total_seconds() / 3600.0)
    except Exception:
        return None


def verify_artifacts_and_db() -> dict[str, object]:
    """Valida banco SQLite e integridade dos artefatos de horários e treino."""
    init_db()
    summary = get_db_summary()

    if not SCHEDULES_JSON.exists():
        raise FileNotFoundError(f"Arquivo ausente: {SCHEDULES_JSON}")
    with open(SCHEDULES_JSON, "r", encoding="utf-8") as f:
        sched = json.load(f)
    lines_count = len(sched.get("lines", {}))
    if lines_count != 393:
        raise RuntimeError(f"gtfs_schedules.json possui {lines_count} linhas; esperado 393.")

    status_data: dict[str, object] = {}
    if STATUS_JSON.exists():
        with open(STATUS_JSON, "r", encoding="utf-8") as f:
            status_data = json.load(f)

    age_h = _parse_iso_age_hours(str(status_data.get("trained_at_utc") or ""))
    return {
        "db_counts": summary.get("counts", {}),
        "schedules_lines": lines_count,
        "rmr_places": len(sched.get("rmr_places", [])),
        "status_exists": STATUS_JSON.exists(),
        "validation_393_passed": bool(status_data.get("validation_393_passed")),
        "stgcn_mae": status_data.get("stgcn_mae"),
        "trained_at_utc": status_data.get("trained_at_utc"),
        "status_age_hours": round(age_h, 2) if age_h is not None else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Hook de treino contínuo e verificação DB/GTFS.")
    parser.add_argument("--quick", action="store_true", help="Apenas valida DB, GTFS e status de treino (<1s).")
    parser.add_argument("--retrain", action="store_true", help="Executa o treino contínuo ST-GCN completo.")
    parser.add_argument(
        "--max-age-hours",
        type=float,
        default=12.0,
        help="Idade máxima do model_training_status.json antes de recomendar/rodar novo treino.",
    )
    args = parser.parse_args()

    t0 = time.time()
    try:
        info = verify_artifacts_and_db()
    except Exception as exc:
        if args.quick and not args.retrain:
            print(f"[hook_continuous_train] Falha na verificação: {exc}", file=sys.stderr)
            return 1
        info = {"status_exists": False, "validation_393_passed": False, "error": str(exc)}

    needs_train = args.retrain or not info.get("status_exists") or not info.get("validation_393_passed")
    age_h = info.get("status_age_hours")
    if isinstance(age_h, (int, float)) and age_h > args.max_age_hours and not args.quick:
        needs_train = True

    if needs_train and not args.quick:
        if not SCHEDULES_JSON.exists():
            import compilar_horarios_gtfs

            compilar_horarios_gtfs.main()
        import treinar_modelo_continuo

        result = treinar_modelo_continuo.run_continuous_training()
        info["retrained"] = True
        info["stgcn_mae"] = result.get("stgcn_mae")
        info["trained_at_utc"] = result.get("trained_at_utc")
        info["validation_393_passed"] = result.get("validation_393_passed")
        flag_file = BASE_DIR.parent.parent / ".agents" / "hooks" / "retrain_recommended.flag"
        flag_file.unlink(missing_ok=True)
    else:
        info["retrained"] = False

    info["elapsed_ms"] = round((time.time() - t0) * 1000, 1)
    print(json.dumps(info, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
