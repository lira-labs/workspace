# -*- coding: utf-8 -*-
"""
Gestor de Persistência Local (SQLite) para Treino Contínuo & Auditoria · GrafoParada.

Espelha o esquema relacional canônico de `contracts/data-model.md` e das rotas
serverless `/api/register`, `/api/routine` e `/api/telemetry` (Neon Postgres).
Banco padrão: `code/grafoparada_tec/data/grafoparada.db` (jamais versionado no Git).
"""
from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
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
        consent_at TEXT,
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
        legs_json TEXT,
        transfer_hub_name TEXT,
        return_origin_name TEXT,
        updated_at TEXT,
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
        delay_min REAL,
        wait_report_type TEXT,
        ti_hub_id TEXT,
        transfer_ok INTEGER,
        notes TEXT,
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
    """
    CREATE TABLE IF NOT EXISTS app_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        event_type TEXT NOT NULL,
        route_code TEXT,
        stop_id TEXT,
        payload_json TEXT,
        created_at TEXT NOT NULL
    )
    """,
)

_MIGRATION_COLUMNS: dict[str, tuple[tuple[str, str], ...]] = {
    "users": (
        ("consent_at", "TEXT"),
    ),
    "routines": (
        ("legs_json", "TEXT"),
        ("transfer_hub_name", "TEXT"),
        ("return_origin_name", "TEXT"),
        ("updated_at", "TEXT"),
    ),
    "demand_observations": (
        ("delay_min", "REAL"),
        ("wait_report_type", "TEXT"),
        ("ti_hub_id", "TEXT"),
        ("transfer_ok", "INTEGER"),
        ("notes", "TEXT"),
    ),
}

_INDEX_STATEMENTS = (
    "CREATE INDEX IF NOT EXISTS idx_users_contact_hint_lower ON users (contact_hint)",
    "CREATE INDEX IF NOT EXISTS idx_routines_user_id ON routines (user_id)",
    "CREATE INDEX IF NOT EXISTS idx_routines_created_at ON routines (created_at)",
    "CREATE INDEX IF NOT EXISTS idx_obs_route_code ON demand_observations (route_code)",
    "CREATE INDEX IF NOT EXISTS idx_obs_created_at ON demand_observations (created_at)",
    "CREATE INDEX IF NOT EXISTS idx_obs_stop_created ON demand_observations (stop_id, created_at)",
    "CREATE INDEX IF NOT EXISTS idx_app_events_type_created ON app_events (event_type, created_at)",
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


def _optional_bool_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, (int, float)):
        if value == 1:
            return 1
        if value == 0:
            return 0
        return None
    normalized = str(value).strip().lower()
    if normalized in ("true", "1", "sim"):
        return 1
    if normalized in ("false", "0", "nao", "não"):
        return 0
    return None


def init_db(db_path: str | Path | None = None) -> Path:
    """Inicializa o banco SQLite local e cria as tabelas canônicas de forma idempotente."""
    resolved = _resolve_db_path(db_path)
    with _connect(resolved) as conn:
        for stmt in _SCHEMA_STATEMENTS:
            conn.execute(stmt)
        for table, cols in _MIGRATION_COLUMNS.items():
            existing_cols = {
                str(row[1]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()
            }
            for col_name, col_type in cols:
                if col_name not in existing_cols:
                    conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")
        for idx_stmt in _INDEX_STATEMENTS:
            conn.execute(idx_stmt)
    return resolved


def register_user(
    name: str,
    contact_hint: str = "",
    user_id: str | None = None,
    db_path: str | Path | None = None,
    consent_at: str | None = None,
) -> dict[str, Any]:
    """Cadastra ou atualiza perfil leve LGPD (sem CPF) na tabela `users`."""
    clean_name = _require_str(name, "name", max_len=120)
    clean_hint = _optional_str(contact_hint, max_len=120)
    clean_id = _optional_str(user_id, max_len=80) or f"usr_{uuid.uuid4().hex[:12]}"
    clean_consent = _optional_str(consent_at, max_len=64)
    now = _utc_now_iso()

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        conn.execute(
            """
            INSERT INTO users (id, name, contact_hint, consent_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                contact_hint = excluded.contact_hint,
                consent_at = COALESCE(excluded.consent_at, users.consent_at),
                updated_at = excluded.updated_at
            """,
            (clean_id, clean_name, clean_hint, clean_consent, now, now),
        )
        row = conn.execute(
            "SELECT id, name, contact_hint, consent_at, created_at, updated_at FROM users WHERE id = ?",
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
    updated_at = _optional_str(routine_dict.get("updated_at"), max_len=64) or _utc_now_iso()
    raw_legs = routine_dict.get("legs_json")
    if isinstance(raw_legs, (list, dict)):
        legs_json = json.dumps(raw_legs, ensure_ascii=False)[:16000]
    elif isinstance(routine_dict.get("legs"), (list, dict)):
        legs_json = json.dumps(routine_dict["legs"], ensure_ascii=False)[:16000]
    else:
        legs_json = _optional_str(raw_legs, 16000)

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
        legs_json,
        _optional_str(routine_dict.get("transfer_hub_name"), 180),
        _optional_str(routine_dict.get("return_origin_name"), 180),
        updated_at,
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
                frequency, legs_json, transfer_hub_name, return_origin_name,
                updated_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                frequency = excluded.frequency,
                legs_json = excluded.legs_json,
                transfer_hub_name = excluded.transfer_hub_name,
                return_origin_name = excluded.return_origin_name,
                updated_at = excluded.updated_at
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
    raw_notes = obs_dict.get("notes") if obs_dict.get("notes") is not None else obs_dict.get("label")

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        cursor = conn.execute(
            """
            INSERT INTO demand_observations (
                user_id, stop_id, route_code, direction,
                observed_wait_min, predicted_wait_min, occupancy_est,
                delay_min, wait_report_type, ti_hub_id, transfer_ok, notes,
                source, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                _optional_str(obs_dict.get("user_id"), 80),
                _optional_str(obs_dict.get("stop_id"), 64),
                route_code,
                _optional_str(obs_dict.get("direction"), 24),
                _optional_float(obs_dict.get("observed_wait_min"), "observed_wait_min", min_value=0.0),
                _optional_float(obs_dict.get("predicted_wait_min"), "predicted_wait_min", min_value=0.0),
                _optional_int(obs_dict.get("occupancy_est"), "occupancy_est", min_value=0),
                _optional_float(obs_dict.get("delay_min"), "delay_min"),
                _optional_str(obs_dict.get("wait_report_type"), 64),
                _optional_str(obs_dict.get("ti_hub_id"), 64),
                _optional_bool_int(obs_dict.get("transfer_ok")),
                _optional_str(raw_notes, 500),
                source,
                now,
            ),
        )
        row = conn.execute(
            "SELECT * FROM demand_observations WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return dict(row)


def record_app_event(
    event_dict: dict[str, Any],
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """Registra um evento de telemetria de aplicação em `app_events`."""
    if not isinstance(event_dict, dict):
        raise ValueError("event_dict deve ser um dicionário.")

    event_type = _require_str(event_dict.get("event_type"), "event_type", max_len=80)
    raw_payload = event_dict.get("payload_json")
    if isinstance(raw_payload, (dict, list)):
        payload_json = json.dumps(raw_payload, ensure_ascii=False)[:8000]
    elif isinstance(event_dict.get("payload"), (dict, list)):
        payload_json = json.dumps(event_dict["payload"], ensure_ascii=False)[:8000]
    else:
        payload_json = _optional_str(raw_payload, 8000)
    now = _optional_str(event_dict.get("created_at"), max_len=64) or _utc_now_iso()

    resolved = init_db(db_path)
    with _connect(resolved) as conn:
        cursor = conn.execute(
            """
            INSERT INTO app_events (
                user_id, event_type, route_code, stop_id, payload_json, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                _optional_str(event_dict.get("user_id"), 80),
                event_type,
                _optional_str(event_dict.get("route_code"), 32),
                _optional_str(event_dict.get("stop_id"), 64),
                payload_json,
                now,
            ),
        )
        row = conn.execute(
            "SELECT * FROM app_events WHERE id = ?",
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


def _fetch_json(url: str, timeout: float) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "GrafoParada-Trainer/3.1"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    parsed = json.loads(raw)
    return parsed if isinstance(parsed, dict) else {}


def sync_cloud_observations(
    api_base: str | None = None,
    timeout: float = 5.0,
    db_path: str | Path | None = None,
) -> dict[str, Any]:
    """
    Sincroniza de forma segura rotinas e observações reais da API Vercel/Neon para o SQLite local.
    Nunca lança exceção quando `GRAFOPARADA_API_BASE` não está configurado ou a rede está offline.
    """
    raw_base = api_base if api_base is not None else os.environ.get("GRAFOPARADA_API_BASE", "")
    base_url = str(raw_base or "").strip().rstrip("/")
    if not base_url:
        return {
            "synced": False,
            "reason": "no_api_base_or_offline",
            "observations_added": 0,
            "routines_added": 0,
        }

    telemetry_payload: dict[str, Any] | None = None
    routine_payload: dict[str, Any] | None = None

    try:
        telemetry_payload = _fetch_json(f"{base_url}/api/telemetry?limit=500", timeout=timeout)
    except Exception:
        telemetry_payload = None

    try:
        routine_payload = _fetch_json(f"{base_url}/api/routine?limit=200", timeout=timeout)
    except Exception:
        routine_payload = None

    if telemetry_payload is None and routine_payload is None:
        return {
            "synced": False,
            "reason": "no_api_base_or_offline",
            "observations_added": 0,
            "routines_added": 0,
        }

    resolved = init_db(db_path)
    routines_added = 0
    observations_added = 0

    with _connect(resolved) as conn:
        existing_routine_ids = {
            str(r[0]) for r in conn.execute("SELECT id FROM routines").fetchall() if r[0]
        }
        existing_obs_keys = {
            (
                str(r[0] or ""),
                str(r[1] or ""),
                str(r[2] or ""),
                str(r[3] or ""),
            )
            for r in conn.execute(
                "SELECT route_code, stop_id, source, created_at FROM demand_observations"
            ).fetchall()
        }

    if isinstance(routine_payload, dict):
        for rtn in routine_payload.get("routines") or []:
            if not isinstance(rtn, dict):
                continue
            try:
                rtn_id = str(rtn.get("id") or "").strip()
                saved = save_routine(rtn, db_path=resolved)
                saved_id = str(saved.get("id") or rtn_id)
                if saved_id and saved_id not in existing_routine_ids:
                    existing_routine_ids.add(saved_id)
                    routines_added += 1
            except Exception:
                continue

    if isinstance(telemetry_payload, dict):
        for obs in telemetry_payload.get("recent_observations") or []:
            if not isinstance(obs, dict):
                continue
            key = (
                str(obs.get("route_code") or "").strip(),
                str(obs.get("stop_id") or "").strip(),
                str(obs.get("source") or "").strip(),
                str(obs.get("created_at") or "").strip(),
            )
            if key in existing_obs_keys:
                continue
            try:
                record_observation(obs, db_path=resolved)
                existing_obs_keys.add(key)
                observations_added += 1
            except Exception:
                continue

    return {
        "synced": True,
        "reason": "ok",
        "observations_added": observations_added,
        "routines_added": routines_added,
    }


def push_latest_training_run_to_cloud(
    cloud_url: str | None = None,
    timeout: float = 5.0,
    db_path: str | Path | None = None,
    sync_token: str | None = None,
) -> dict[str, Any]:
    """
    Envia o último registro local de `training_runs` para `POST /api/telemetry`
    (`kind="training_run"`) quando `cloud_url` ou `GRAFOPARADA_CLOUD_URL` estiver definido.
    Falha silenciosamente com retorno estruturado quando offline ou sem URL configurada.
    """
    raw_url = cloud_url if cloud_url is not None else os.environ.get("GRAFOPARADA_CLOUD_URL", "")
    base_url = str(raw_url or "").strip().rstrip("/")
    if not base_url:
        return {"pushed": False, "reason": "no_cloud_url"}

    try:
        resolved = init_db(db_path)
        with _connect(resolved) as conn:
            latest_row = conn.execute(
                "SELECT * FROM training_runs ORDER BY id DESC LIMIT 1"
            ).fetchone()
    except Exception:
        return {"pushed": False, "reason": "local_db_error"}

    if not latest_row:
        return {"pushed": False, "reason": "no_training_run"}

    run = dict(latest_row)
    endpoint = base_url if base_url.endswith("/api/telemetry") else f"{base_url}/api/telemetry"
    payload = {
        "kind": "training_run",
        "dataset_rows": run.get("dataset_rows"),
        "real_observations": run.get("real_observations"),
        "lines_covered": run.get("lines_covered"),
        "stgcn_mae": run.get("stgcn_mae"),
        "ols_mae": run.get("ols_mae"),
        "persistence_mae": run.get("persistence_mae"),
        "weights_hash": run.get("weights_hash"),
        "notes": run.get("notes"),
        "created_at": run.get("created_at"),
    }

    raw_token = sync_token if sync_token is not None else os.environ.get("GRAFOPARADA_SYNC_TOKEN", "")
    token = str(raw_token or "").strip()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "GrafoParada-Trainer/3.1",
    }
    if token:
        headers["x-sync-token"] = token

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = int(getattr(resp, "status", 200))
            raw_body = resp.read().decode("utf-8")
        parsed = json.loads(raw_body) if raw_body.strip() else {}
        return {
            "pushed": True,
            "reason": "ok",
            "status": status,
            "weights_hash": run.get("weights_hash"),
            "response": parsed if isinstance(parsed, dict) else {},
        }
    except Exception:
        return {"pushed": False, "reason": "offline_or_error"}
