# -*- coding: utf-8 -*-
"""
Gestor de Persistência Local (SQLite) para Treino Contínuo & Auditoria · GrafoParada.

Espelha o esquema relacional canônico de `contracts/data-model.md` e das rotas
serverless `/api/register`, `/api/routine` e `/api/telemetry` (Neon Postgres).
Banco padrão: `code/grafoparada_tec/data/grafoparada.db` (jamais versionado no Git).
"""
from __future__ import annotations

import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DEFAULT_DB_PATH = Path(__file__).resolve().parent / "data" / "grafoparada.db"

_SCHEMA_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        contact_hint TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS routines (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        origin_city TEXT NOT NULL,
        origin_neighborhood TEXT,
        origin_stop_id TEXT,
        origin_stop_name TEXT NOT NULL,
        origin_lat REAL,
        origin_lon REAL,
        dest_city TEXT NOT NULL,
        dest_neighborhood TEXT,
        dest_stop_id TEXT,
        dest_stop_name TEXT NOT NULL,
        dest_lat REAL,
        dest_lon REAL,
        departure_time TEXT,
        return_time TEXT,
        preferred_line TEXT,
        frequency TEXT,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS demand_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        stop_id TEXT,
        route_code TEXT NOT NULL,
        direction TEXT,
        observed_wait_min REAL,
        predicted_wait_min REAL,
        occupancy_est INTEGER,
        source TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS training_runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dataset_rows INTEGER NOT NULL,
        real_observations INTEGER NOT NULL,
        lines_covered INTEGER NOT NULL,
        stgcn_mae REAL NOT NULL,
        ols_mae REAL NOT NULL,
        persistence_mae REAL NOT NULL,
        weights_hash TEXT NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_routines_user_id ON routines (user_id)",
    "CREATE INDEX IF NOT EXISTS idx_obs_route_code ON demand_observations (route_code)",
    "CREATE INDEX IF NOT EXISTS idx_obs_created_at ON demand_observations (created_at)",
)


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_db_path(db_path: str | Path | None = None) -> Path:
    if db_path is not None:
        return Path(db_path)
    env_override = os.environ.get("GRAFOPARADA_SQLITE_PATH", "").strip()
    return Path(env_override) if env_override else DEFAULT_DB_PATH


@contextmanager
def _connect(db_path: str | Path | None = None) -> Iterator[sqlite3.Connection]:
    resolved = _resolve_db_path(db_path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(resolved), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _require_str(value: Any, field_name: str, max_len: int = 240) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Campo '{field_name}' deve ser texto não vazio.")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"Campo '{field_name}' é obrigatório e não pode estar vazio.")
    if len(cleaned) > max_len:
        raise ValueError(f"Campo '{field_name}' excede o limite de {max_len} caracteres.")
    return cleaned


def _optional_str(value: Any, max_len: int = 240) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip()
    if not cleaned:
        return None
    return cleaned[:max_len]


def _optional_float(value: Any, field_name: str, min_value: float | None = None) -> float | None:
    if value is None or value == "":
        return None
    num = float(value)
    if min_value is not None and num < min_value:
        raise ValueError(f"Campo '{field_name}' deve ser >= {min_value}.")
    return num


def _optional_int(value: Any, field_name: str, min_value: int | None = None) -> int | None:
    if value is None or value == "":
        return None
    num = int(value)
    if min_value is not None and num < min_value:
        raise ValueError(f"Campo '{field_name}' deve ser >= {min_value}.")
    return num


def init_db(db_path: str | Path | None = None) -> Path:
    """Inicializa o banco SQLite local e cria as 4 tabelas canônicas de forma idempotente."""
    resolved = _resolve_db_path(db_path)
    with _connect(resolved) as conn:
        for stmt in _SCHEMA_STATEMENTS:
            conn.execute(stmt)
    return resolved


def register_user(
    name: str,
    contact_hint: str = "",
    user_id: str | None = None,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Cadastra ou atualiza perfil leve LGPD (sem CPF) na tabela `users`."""
    clean_name = _require_str(name, "name", max_len=120)
    clean_hint = _optional_str(contact_hint, max_len=120)
    clean_id = _optional_str(user_id, max_len=80) or f"usr_{uuid.uuid4().hex[:12]}"
    now = _utc_now_iso()

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        conn.execute(
            """
            INSERT INTO users (id, name, contact_hint, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                contact_hint = excluded.contact_hint,
                updated_at = excluded.updated_at
            """,
            (clean_id, clean_name, clean_hint, now, now),
        )
        row = conn.execute(
            "SELECT id, name, contact_hint, created_at, updated_at FROM users WHERE id = ?",
            (clean_id,),
        ).fetchone()
    return dict(row)


def save_routine(
    routine_dict: dict[str, Any],
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Persiste uma rotina diária de origem e destino na tabela `routines`."""
    if not isinstance(routine_dict, dict):
        raise ValueError("routine_dict deve ser um dicionário.")

    routine_id = _optional_str(routine_dict.get("id"), max_len=80) or f"rtn_{uuid.uuid4().hex[:12]}"
    user_id = _require_str(routine_dict.get("user_id"), "user_id", max_len=80)
    origin_city = _require_str(routine_dict.get("origin_city"), "origin_city", max_len=120)
    origin_stop_name = _require_str(
        routine_dict.get("origin_stop_name"), "origin_stop_name", max_len=180
    )
    dest_city = _require_str(routine_dict.get("dest_city"), "dest_city", max_len=120)
    dest_stop_name = _require_str(
        routine_dict.get("dest_stop_name"), "dest_stop_name", max_len=180
    )
    now = _optional_str(routine_dict.get("created_at"), max_len=64) or _utc_now_iso()

    payload = (
        routine_id,
        user_id,
        origin_city,
        _optional_str(routine_dict.get("origin_neighborhood"), 120),
        _optional_str(routine_dict.get("origin_stop_id"), 64),
        origin_stop_name,
        _optional_float(routine_dict.get("origin_lat"), "origin_lat"),
        _optional_float(routine_dict.get("origin_lon"), "origin_lon"),
        dest_city,
        _optional_str(routine_dict.get("dest_neighborhood"), 120),
        _optional_str(routine_dict.get("dest_stop_id"), 64),
        dest_stop_name,
        _optional_float(routine_dict.get("dest_lat"), "dest_lat"),
        _optional_float(routine_dict.get("dest_lon"), "dest_lon"),
        _optional_str(routine_dict.get("departure_time"), 16),
        _optional_str(routine_dict.get("return_time"), 16),
        _optional_str(routine_dict.get("preferred_line"), 32),
        _optional_str(routine_dict.get("frequency"), 32),
        now,
    )

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        conn.execute(
            """
            INSERT INTO routines (
                id, user_id, origin_city, origin_neighborhood, origin_stop_id,
                origin_stop_name, origin_lat, origin_lon, dest_city,
                dest_neighborhood, dest_stop_id, dest_stop_name, dest_lat,
                dest_lon, departure_time, return_time, preferred_line,
                frequency, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                user_id = excluded.user_id,
                origin_city = excluded.origin_city,
                origin_neighborhood = excluded.origin_neighborhood,
                origin_stop_id = excluded.origin_stop_id,
                origin_stop_name = excluded.origin_stop_name,
                origin_lat = excluded.origin_lat,
                origin_lon = excluded.origin_lon,
                dest_city = excluded.dest_city,
                dest_neighborhood = excluded.dest_neighborhood,
                dest_stop_id = excluded.dest_stop_id,
                dest_stop_name = excluded.dest_stop_name,
                dest_lat = excluded.dest_lat,
                dest_lon = excluded.dest_lon,
                departure_time = excluded.departure_time,
                return_time = excluded.return_time,
                preferred_line = excluded.preferred_line,
                frequency = excluded.frequency
            """,
            payload,
        )
        row = conn.execute("SELECT * FROM routines WHERE id = ?", (routine_id,)).fetchone()
    return dict(row)


def record_observation(
    obs_dict: dict[str, Any],
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Registra observação de espera e demanda real em `demand_observations`."""
    if not isinstance(obs_dict, dict):
        raise ValueError("obs_dict deve ser um dicionário.")

    route_code = _require_str(obs_dict.get("route_code"), "route_code", max_len=32)
    source = _require_str(obs_dict.get("source"), "source", max_len=80)
    now = _optional_str(obs_dict.get("created_at"), max_len=64) or _utc_now_iso()

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        cursor = conn.execute(
            """
            INSERT INTO demand_observations (
                user_id, stop_id, route_code, direction,
                observed_wait_min, predicted_wait_min, occupancy_est,
                source, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _optional_str(obs_dict.get("user_id"), 80),
                _optional_str(obs_dict.get("stop_id"), 64),
                route_code,
                _optional_str(obs_dict.get("direction"), 24),
                _optional_float(obs_dict.get("observed_wait_min"), "observed_wait_min", min_value=0.0),
                _optional_float(obs_dict.get("predicted_wait_min"), "predicted_wait_min", min_value=0.0),
                _optional_int(obs_dict.get("occupancy_est"), "occupancy_est", min_value=0),
                source,
                now,
            ),
        )
        row = conn.execute(
            "SELECT * FROM demand_observations WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


def log_training_run(
    run_dict: dict[str, Any],
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Registra uma execução de treino/avaliação contínua na tabela `training_runs`."""
    if not isinstance(run_dict, dict):
        raise ValueError("run_dict deve ser um dicionário.")

    required_ints = ("dataset_rows", "real_observations", "lines_covered")
    required_floats = ("stgcn_mae", "ols_mae", "persistence_mae")
    for field in (*required_ints, *required_floats):
        if run_dict.get(field) is None:
            raise ValueError(f"Campo obrigatório '{field}' ausente em run_dict.")

    dataset_rows = int(run_dict["dataset_rows"])
    real_observations = int(run_dict["real_observations"])
    lines_covered = int(run_dict["lines_covered"])
    stgcn_mae = float(run_dict["stgcn_mae"])
    ols_mae = float(run_dict["ols_mae"])
    persistence_mae = float(run_dict["persistence_mae"])
    weights_hash = _require_str(run_dict.get("weights_hash"), "weights_hash", max_len=128)
    notes = _optional_str(run_dict.get("notes"), max_len=500)
    now = _optional_str(run_dict.get("created_at"), max_len=64) or _utc_now_iso()

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        cursor = conn.execute(
            """
            INSERT INTO training_runs (
                dataset_rows, real_observations, lines_covered,
                stgcn_mae, ols_mae, persistence_mae,
                weights_hash, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dataset_rows,
                real_observations,
                lines_covered,
                stgcn_mae,
                ols_mae,
                persistence_mae,
                weights_hash,
                notes,
                now,
            ),
        )
        row = conn.execute(
            "SELECT * FROM training_runs WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


def get_training_dataset(db_path: str | Path | None = None) -> dict[str, Any]:
    """Retorna observações e rotinas consolidadas para alimentação contínua do `transit-trainer`."""
    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        observations = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM demand_observations ORDER BY created_at DESC, id DESC"
            ).fetchall()
        ]
        routines = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM routines ORDER BY created_at DESC"
            ).fetchall()
        ]
        latest_run_row = conn.execute(
            "SELECT * FROM training_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()

    lines_covered = sorted(
        {
            str(obs["route_code"]).strip()
            for obs in observations
            if obs.get("route_code")
        }
        | {
            str(rtn["preferred_line"]).strip()
            for rtn in routines
            if rtn.get("preferred_line")
        }
    )

    return {
        "db_path": str(resolved),
        "observations": observations,
        "routines": routines,
        "total_observations": len(observations),
        "total_routines": len(routines),
        "lines_covered": lines_covered,
        "latest_training_run": dict(latest_run_row) if latest_run_row else None,
    }


def get_db_summary(db_path: str | Path | None = None) -> dict[str, Any]:
    """Retorna sumário de contagens das 4 tabelas, últimas observações e último ciclo de treino."""
    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        counts = {
            table: int(conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in ("users", "routines", "demand_observations", "training_runs")
        }
        latest_run_row = conn.execute(
            "SELECT * FROM training_runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
        recent_obs = [
            dict(r)
            for r in conn.execute(
                "SELECT * FROM demand_observations ORDER BY id DESC LIMIT 20"
            ).fetchall()
        ]
        distinct_lines = [
            r[0]
            for r in conn.execute(
                "SELECT DISTINCT route_code FROM demand_observations WHERE route_code IS NOT NULL ORDER BY route_code"
            ).fetchall()
        ]

    return {
        "db_path": str(resolved),
        "counts": counts,
        "lines_covered": distinct_lines,
        "latest_training_run": dict(latest_run_row) if latest_run_row else None,
        "recent_observations": recent_obs,
    }
