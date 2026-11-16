"""GrafoParada Workspace Safety & Lint Hook Handler (.agents/hooks.json).

Executa verificações leves de sintaxe e segurança no ciclo de vida do agente
Antigravity (PreInvocation, PreToolUse, PostToolUse) sem bloquear fluxos normais.
"""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HOOKS_DIR = Path(__file__).resolve().parent
AGENTS_DIR = HOOKS_DIR.parent
WORKSPACE_DIR = AGENTS_DIR.parent
STATUS_LOG = HOOKS_DIR / "last_lint_error.log"
UNSLOP_LOG = HOOKS_DIR / "last_unslop_warning.log"
RETRAIN_FLAG = HOOKS_DIR / "retrain_recommended.flag"
UNSLOP_SCRIPT = AGENTS_DIR / "skills" / "unslop" / "scripts" / "banned_phrase_scan.py"
CONTINUOUS_HOOK_SCRIPT = WORKSPACE_DIR / "code" / "grafoparada_tec" / "hook_continuous_train.py"


def _read_payload() -> dict:
    try:
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def _validate_file(path_str: str) -> str | None:
    p = Path(path_str)
    if not p.exists() or not p.is_file():
        return None
    suffix = p.suffix.lower()
    try:
        if suffix == ".py":
            py_compile.compile(str(p), doraise=True)
        elif suffix == ".json":
            if p.stat().st_size < 10_000_000:
                parsed = json.loads(p.read_text(encoding="utf-8"))
                if p.name == "gtfs_schedules.json":
                    if len(parsed.get("lines", {})) != 393 or "rmr_places" not in parsed:
                        return "gtfs_schedules.json invalido: esperado 393 linhas e chave rmr_places."
        elif suffix == ".js":
            res = subprocess.run(
                ["node", "--check", str(p)],
                capture_output=True,
                text=True,
                timeout=6,
            )
            if res.returncode != 0:
                return f"JS syntax error in {p.name}: {(res.stderr or res.stdout).strip()[:400]}"
        elif suffix == ".html":
            text = p.read_text(encoding="utf-8", errors="ignore")
            ids = re.findall(r'\bid=["\']([^"\']+)["\']', text)
            dups = sorted({i for i in ids if ids.count(i) > 1})
            if dups:
                return f"Duplicate HTML id(s) in {p.name}: {', '.join(dups[:8])}"
            body_part = text.split("<body", 1)[1] if "<body" in text else text
            body_part = re.sub(r"<script\b[\s\S]*?</script>", "", body_part, flags=re.I)
            depth = 0
            for idx, line in enumerate(body_part.splitlines(), 1):
                depth += len(re.findall(r"<div\b", line, re.I)) - len(re.findall(r"</div>", line, re.I))
                if depth < 0:
                    return f"Unbalanced </div> (negative depth {depth}) around body line {idx} in {p.name}"
            if depth != 0:
                return f"Unbalanced <div> count in {p.name}: net balance {depth}"
            scripts = re.findall(r"<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)</script>", text, re.I)
            if scripts:
                joined = "\n;\n".join(scripts)
                with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as tf:
                    tf.write(joined)
                    tmp_path = tf.name
                try:
                    res = subprocess.run(
                        ["node", "--check", tmp_path],
                        capture_output=True,
                        text=True,
                        timeout=6,
                    )
                    if res.returncode != 0:
                        return f"Inline <script> syntax error in {p.name}: {(res.stderr or res.stdout).strip()[:400]}"
                finally:
                    Path(tmp_path).unlink(missing_ok=True)
    except Exception as exc:
        return f"Validation error in {p.name}: {exc}"
    return None


def _check_unslop(p: Path) -> None:
    """Roda scanner anti-AI-slop leve em textos/documentos do app ou apresentacao."""
    if not UNSLOP_SCRIPT.exists() or p.suffix.lower() not in {".md", ".txt"}:
        return
    if p.name in {"HANDOFF.md", "AGENTS.md", "CONTEXT.md"} or "node_modules" in p.parts:
        return
    try:
        res = subprocess.run(
            [sys.executable, str(UNSLOP_SCRIPT), str(p)],
            capture_output=True,
            text=True,
            timeout=5,
        )
        out = (res.stdout or "").strip()
        if res.returncode != 0 or ("match" in out.lower() and "0 matches" not in out.lower()):
            UNSLOP_LOG.write_text(f"{p.name}: {out[:300]}", encoding="utf-8")
        else:
            UNSLOP_LOG.unlink(missing_ok=True)
    except Exception:
        pass


def _maybe_check_continuous_train(p: Path) -> str | None:
    """Verifica DB + GTFS rapidamente e sinaliza quando treino continuo e recomendado."""
    triggers = {
        "treinar_modelo_continuo.py",
        "compilar_horarios_gtfs.py",
        "compilar_rede_real_gtfs.py",
        "db_manager.py",
        "gtfs_schedules.json",
        "gtfs_real_network.json",
        "model_training_status.json",
    }
    if p.name not in triggers:
        return None
    if p.name in {"treinar_modelo_continuo.py", "compilar_horarios_gtfs.py", "gtfs_schedules.json"}:
        RETRAIN_FLAG.write_text(p.name, encoding="utf-8")
    elif p.name == "model_training_status.json":
        RETRAIN_FLAG.unlink(missing_ok=True)
    if CONTINUOUS_HOOK_SCRIPT.exists():
        res = subprocess.run(
            [sys.executable, str(CONTINUOUS_HOOK_SCRIPT), "--quick"],
            capture_output=True,
            text=True,
            timeout=8,
        )
        if res.returncode != 0:
            return f"Continuous train/DB check falhou apos editar {p.name}: {(res.stderr or res.stdout).strip()[:300]}"
    return None


def handle_post_edit(payload: dict) -> dict:
    args = (payload.get("toolCall") or {}).get("args") or {}
    path_str = args.get("Path") or args.get("path") or ""
    if path_str:
        p = Path(str(path_str))
        err = _validate_file(str(path_str))
        if not err and p.exists() and p.is_file():
            err = _maybe_check_continuous_train(p)
            _check_unslop(p)
        if err:
            STATUS_LOG.write_text(err, encoding="utf-8")
        else:
            STATUS_LOG.unlink(missing_ok=True)
    return {}


def handle_pre_invocation(_payload: dict) -> dict:
    alerts: list[str] = []
    if STATUS_LOG.exists():
        msg = STATUS_LOG.read_text(encoding="utf-8").strip()
        if msg:
            alerts.append(f"[Hook PostToolUse Alert] Corrija antes de prosseguir: {msg}")
    if RETRAIN_FLAG.exists():
        src = RETRAIN_FLAG.read_text(encoding="utf-8").strip()
        alerts.append(
            f"[Hook Continuous Train] '{src}' foi alterado; rode "
            "`uv run --project code/grafoparada_tec python code/grafoparada_tec/hook_continuous_train.py --retrain`."
        )
    if UNSLOP_LOG.exists():
        u = UNSLOP_LOG.read_text(encoding="utf-8").strip()
        if u:
            alerts.append(f"[Hook Unslop] Padrao de prose AI detectado em {u}")
    if alerts:
        return {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": " | ".join(alerts)
                    }
                }
            ]
        }
    return {}


def handle_pre_tool(payload: dict) -> dict:
    args = (payload.get("toolCall") or {}).get("args") or {}
    cmd = str(args.get("CommandLine") or "")
    lowered = cmd.lower()
    if re.search(r"git\s+(push\s+.*(--force|-f)|reset\s+--hard)", lowered):
        return {
            "decision": "ask",
            "reason": "Hook de segurança detectou comando destrutivo no Git (--force ou reset --hard).",
        }
    if re.search(r"git\s+(push|merge)\b.*\bmain\b", lowered) and STATUS_LOG.exists():
        msg = STATUS_LOG.read_text(encoding="utf-8").strip()
        if msg:
            return {
                "decision": "deny",
                "reason": f"Hook bloqueou envio para main devido a erro pendente: {msg}",
            }
    return {"decision": "allow"}


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    payload = _read_payload()
    if mode == "post_edit":
        out = handle_post_edit(payload)
    elif mode == "pre_invocation":
        out = handle_pre_invocation(payload)
    elif mode == "pre_tool":
        out = handle_pre_tool(payload)
    else:
        out = {}
    sys.stdout.write(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
