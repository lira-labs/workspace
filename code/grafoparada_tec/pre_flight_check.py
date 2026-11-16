#!/usr/bin/env python3
"""
Pre-Flight Check & Deploy Gatekeeper para o GrafoParada
Executa validação sintática, verificação de dados, presença do deck oficial da banca e suíte de testes antes do merge/deploy na main.
"""

import sys
import os
import json
import py_compile
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TEC_DIR = ROOT / "code" / "grafoparada_tec"
WEB_DIR = ROOT / "code" / "grafoparada_web"
INDEX_HTML = WEB_DIR / "index.html"
ENGINE_JS = WEB_DIR / "real_transit_engine.js"
LAYA_VOICE_JS = WEB_DIR / "laya_voice_engine.js"
API_DIR = WEB_DIR / "api"
API_DB_JS = API_DIR / "_db.js"
API_REGISTER_JS = API_DIR / "register.js"
API_ROUTINE_JS = API_DIR / "routine.js"
API_TELEMETRY_JS = API_DIR / "telemetry.js"
API_TTS_JS = API_DIR / "tts.js"
GTFS_JSON = WEB_DIR / "data" / "gtfs_real_network.json"
GTFS_SCHEDULES_JSON = WEB_DIR / "data" / "gtfs_schedules.json"
MODEL_STATUS_JSON = WEB_DIR / "data" / "model_training_status.json"
LAYA_MANIFEST = WEB_DIR / "audio" / "laya" / "manifest.json"
TEST_SUITE = TEC_DIR / "teste_rotinas_e_realocacao.py"
OFFICIAL_DECK = WEB_DIR / "GrafoParada_Seminario2_CauaLira.pptx"
PY_BACKEND_FILES = [
    TEC_DIR / "db_manager.py",
    TEC_DIR / "compilar_horarios_gtfs.py",
    TEC_DIR / "treinar_modelo_continuo.py",
    TEC_DIR / "hook_continuous_train.py",
]

# Limiar mínimo de integridade física para o arquivo .pptx (1 MB)
MIN_DECK_BYTES = 1_000_000


def print_header(title):
    print(f"\n{'=' * 65}")
    print(f"🚀 [PRE-FLIGHT] {title}")
    print(f"{'=' * 65}")


def check_files():
    print("[1/6] Verificando integridade física dos arquivos essenciais...")
    required = [
        INDEX_HTML,
        ENGINE_JS,
        LAYA_VOICE_JS,
        API_DB_JS,
        API_REGISTER_JS,
        API_ROUTINE_JS,
        API_TELEMETRY_JS,
        API_TTS_JS,
        GTFS_JSON,
        GTFS_SCHEDULES_JSON,
        MODEL_STATUS_JSON,
        LAYA_MANIFEST,
        TEST_SUITE,
        OFFICIAL_DECK,
        *PY_BACKEND_FILES,
    ]
    for p in required:
        if not p.is_file():
            print(f"❌ Arquivo obrigatório não encontrado: {p}")
            return False
        size = p.stat().st_size
        print(f"  ✓ {p.name} ({size:,} bytes)")
    return True


def check_official_deck():
    print("\n[2/6] Validando integridade física da Apresentação Oficial da Banca (PPTX)...")
    if not OFFICIAL_DECK.is_file():
        print(f"❌ Deck oficial não encontrado em: {OFFICIAL_DECK}")
        return False
    
    size = OFFICIAL_DECK.stat().st_size
    if size < MIN_DECK_BYTES:
        print(f"❌ Deck oficial corrompido ou truncado: apenas {size:,} bytes (esperado >= {MIN_DECK_BYTES:,} bytes).")
        return False

    print(f"  ✓ Deck oficial da banca preservado: {OFFICIAL_DECK.name} ({size / (1024 * 1024):.2f} MB)")
    print("  ✓ Garantia de conformidade com a banca examinadora UFRPE AI4Good.")
    return True


def check_gtfs_json():
    print("\n[3/6] Validando JSONs do GTFS Metropolitano, Horários e Status ST-GCN...")
    try:
        with open(GTFS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            total = data.get("total_lines_ready", 0)
            pop = len(data.get("popular_lines", {}))
            if total != 393 or pop != 393:
                print(f"❌ gtfs_real_network.json inconsistente: total={total}, popular={pop} (esperado 393)")
                return False
            print(f"  ✓ gtfs_real_network.json válido! {total} linhas no catálogo, {pop} linhas populares ativas.")
    except Exception as e:
        print(f"❌ Erro ao validar gtfs_real_network.json: {e}")
        return False

    try:
        with open(GTFS_SCHEDULES_JSON, "r", encoding="utf-8") as f:
            sched = json.load(f)
            lines = sched.get("lines")
            rmr_places = sched.get("rmr_places")
            if not isinstance(lines, dict) or len(lines) != 393:
                got = len(lines) if isinstance(lines, dict) else type(lines).__name__
                print(f"❌ gtfs_schedules.json inválido: lines={got} (esperado 393)")
                return False
            if not isinstance(rmr_places, list) or len(rmr_places) == 0:
                print("❌ gtfs_schedules.json inválido: rmr_places vazio ou ausente")
                return False
            cities = sorted({str(p.get("city")).strip() for p in rmr_places if isinstance(p, dict) and p.get("city")})
            if len(cities) < 14:
                print(f"❌ gtfs_schedules.json inválido: apenas {len(cities)} cidades RMR encontradas (esperado >= 14)")
                return False
            print(
                f"  ✓ gtfs_schedules.json válido! {len(lines)} linhas indexadas, "
                f"{len(rmr_places)} rmr_places em {len(cities)} cidades da RMR."
            )
    except Exception as e:
        print(f"❌ Erro ao validar gtfs_schedules.json: {e}")
        return False

    try:
        with open(MODEL_STATUS_JSON, "r", encoding="utf-8") as f:
            status = json.load(f)
            if status.get("validation_393_passed") is not True:
                print(f"❌ model_training_status.json reprovado: validation_393_passed={status.get('validation_393_passed')!r}")
                return False
            print(
                f"  ✓ model_training_status.json válido! validation_393_passed=True, "
                f"lines_covered={status.get('lines_covered')}, stgcn_mae={status.get('stgcn_mae')}."
            )
    except Exception as e:
        print(f"❌ Erro ao validar model_training_status.json: {e}")
        return False

    return True


def check_js_syntax():
    print("\n[4/6] Validando sintaxe JavaScript via Node.js VM e node --check (api/*.js)...")
    node_script = """
const fs = require('fs');
const path = require('path');
const vm = require('vm');

let errors = 0;

// 1. Módulos JS externos (motor GTFS, motor de voz Laya e proxy serverless)
for (const filePath of [process.argv[1], process.argv[3], process.argv[4]]) {
    const label = path.basename(filePath);
    try {
        const code = fs.readFileSync(filePath, 'utf8');
        new vm.Script(code);
        console.log('  ✓ ' + label + ': Sintaxe 100% válida');
    } catch (e) {
        console.error('  ❌ ' + label + ' ERRO:', e.message);
        errors++;
    }
}

// 2. index.html inline scripts
try {
    const html = fs.readFileSync(process.argv[2], 'utf8');
    const scriptRegex = /<script(?![^>]*\\bsrc=)[^>]*>([\\s\\S]*?)<\\/script>/gi;
    let match;
    let count = 0;
    while ((match = scriptRegex.exec(html)) !== null) {
        count++;
        try {
            new vm.Script(match[1]);
            console.log('  ✓ index.html [script inline #' + count + ']: Sintaxe 100% válida');
        } catch (err) {
            console.error('  ❌ index.html [script inline #' + count + '] ERRO:', err.message);
            errors++;
        }
    }
} catch (e) {
    console.error('  ❌ Erro lendo index.html:', e.message);
    errors++;
}

process.exit(errors > 0 ? 1 : 0);
"""
    cmd = [
        "node",
        "-e",
        node_script,
        str(ENGINE_JS),
        str(INDEX_HTML),
        str(LAYA_VOICE_JS),
        str(API_TTS_JS),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout, end="")
    if res.returncode != 0:
        print(res.stderr, end="")
        print("❌ Falha na verificação de sintaxe JavaScript!")
        return False

    api_targets = [API_DB_JS, API_REGISTER_JS, API_ROUTINE_JS, API_TELEMETRY_JS]
    if API_TTS_JS.is_file():
        api_targets.append(API_TTS_JS)
    for api_file in sorted(API_DIR.glob("*.js")):
        if api_file not in api_targets:
            api_targets.append(api_file)

    for api_file in api_targets:
        chk = subprocess.run(["node", "--check", str(api_file)], capture_output=True, text=True)
        if chk.returncode != 0:
            print(chk.stdout, end="")
            print(chk.stderr, end="")
            print(f"❌ Falha em node --check para api/{api_file.name}")
            return False
        print(f"  ✓ api/{api_file.name}: node --check OK")
    return True


def check_python_compile():
    print("\n[5/6] Validando compilação Python dos módulos de dados e treino contínuo...")
    try:
        with tempfile.TemporaryDirectory(prefix="gp_pycompile_") as tmp_dir:
            for py_file in PY_BACKEND_FILES:
                cfile = Path(tmp_dir) / f"{py_file.name}c"
                py_compile.compile(str(py_file), cfile=str(cfile), doraise=True)
                print(f"  ✓ {py_file.name}: py_compile OK")
        return True
    except Exception as e:
        print(f"❌ Erro de compilação Python: {e}")
        return False


def run_test_suite():
    print("\n[6/6] Executando suíte de conformidade operacional, científica e pedagógica...")
    cmd = [sys.executable, str(TEST_SUITE)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    lines = res.stdout.strip().split("\n")
    summary_lines = [l for l in lines if "PASS" in l or "RESULTADO" in l or "STATUS" in l]
    for s in summary_lines[-10:]:
        print(f"  {s}")
    if res.returncode != 0:
        print(res.stdout)
        print(res.stderr)
        print("❌ Falha nos testes de conformidade!")
        return False
    return True


def main():
    print_header("AUDITORIA PRÉ-MERGE / DEPLOY · GRAFOPARADA")
    steps = [
        check_files,
        check_official_deck,
        check_gtfs_json,
        check_js_syntax,
        check_python_compile,
        run_test_suite,
    ]
    for step in steps:
        if not step():
            print("\n" + "=" * 65)
            print("🛑 [BLOQUEADO] Falha nos critérios de qualidade. NÃO faça merge para a main!")
            print("=" * 65)
            sys.exit(1)
    
    print("\n" + "=" * 65)
    print("✅ [APROVADO] Todos os critérios foram 100% atendidos!")
    print("Seguro para merge na branch main e deploy em produção.")
    print("=" * 65)
    sys.exit(0)


if __name__ == "__main__":
    main()
