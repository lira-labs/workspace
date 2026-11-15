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
STATUS_LOG = HOOKS_DIR / "last_lint_error.log"


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
                json.loads(p.read_text(encoding="utf-8"))
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


def handle_post_edit(payload: dict) -> dict:
    args = (payload.get("toolCall") or {}).get("args") or {}
    path_str = args.get("Path") or args.get("path") or ""
    if path_str:
        err = _validate_file(str(path_str))
        if err:
            STATUS_LOG.write_text(err, encoding="utf-8")
        else:
            STATUS_LOG.unlink(missing_ok=True)
    return {}


def handle_pre_invocation(_payload: dict) -> dict:
    if STATUS_LOG.exists():
        msg = STATUS_LOG.read_text(encoding="utf-8").strip()
        if msg:
            return {
                "injectSteps": [
                    {
                        "systemMessage": {
                            "systemMessage": f"[Hook PostToolUse Alert] Corrija antes de prosseguir: {msg}"
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
