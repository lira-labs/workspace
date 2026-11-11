#!/usr/bin/env python3
"""
Pre-Flight Check & Deploy Gatekeeper para o GrafoParada
Executa validação sintática, verificação de dados e suíte de testes antes do merge/deploy na main.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
WEB_DIR = ROOT / "code" / "grafoparada_web"
INDEX_HTML = WEB_DIR / "index.html"
ENGINE_JS = WEB_DIR / "real_transit_engine.js"
GTFS_JSON = WEB_DIR / "data" / "gtfs_real_network.json"
TEST_SUITE = ROOT / "code" / "grafoparada_tec" / "teste_rotinas_e_realocacao.py"

def print_header(title):
    print(f"\n{'=' * 65}")
    print(f"🚀 [PRE-FLIGHT] {title}")
    print(f"{'=' * 65}")

def check_files():
    print("[1/4] Verificando integridade física dos arquivos essenciais...")
    required = [INDEX_HTML, ENGINE_JS, GTFS_JSON, TEST_SUITE]
    for p in required:
        if not p.is_file():
            print(f"❌ Arquivo obrigatório não encontrado: {p}")
            return False
        size = p.stat().st_size
        print(f"  ✓ {p.name} ({size:,} bytes)")
    return True

def check_gtfs_json():
    print("\n[2/4] Validando JSON do GTFS Metropolitano...")
    try:
        with open(GTFS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            total = data.get("total_lines_ready", 0)
            pop = len(data.get("popular_lines", {}))
            print(f"  ✓ GTFS válido! {total} linhas no catálogo, {pop} linhas populares ativas.")
            return True
    except Exception as e:
        print(f"❌ Erro ao validar gtfs_real_network.json: {e}")
        return False

def check_js_syntax():
    print("\n[3/4] Validando sintaxe JavaScript via Node.js VM...")
    node_script = """
const fs = require('fs');
const vm = require('vm');

let errors = 0;

// 1. Engine
try {
    const engineCode = fs.readFileSync(process.argv[1], 'utf8');
    new vm.Script(engineCode);
    console.log('  ✓ real_transit_engine.js: Sintaxe 100% válida');
} catch (e) {
    console.error('  ❌ real_transit_engine.js ERRO:', e.message);
    errors++;
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
    cmd = ["node", "-e", node_script, str(ENGINE_JS), str(INDEX_HTML)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout, end="")
    if res.returncode != 0:
        print(res.stderr, end="")
        print("❌ Falha na verificação de sintaxe JavaScript!")
        return False
    return True

def run_test_suite():
    print("\n[4/4] Executando suíte de conformidade operacional e pedagógica...")
    cmd = [sys.executable, str(TEST_SUITE)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    lines = res.stdout.strip().split("\n")
    summary_lines = [l for l in lines if "PASS" in l or "RESULTADO" in l or "STATUS" in l]
    for s in summary_lines[-5:]:
        print(f"  {s}")
    if res.returncode != 0:
        print("❌ Falha nos testes de conformidade!")
        return False
    return True

def main():
    print_header("AUDITORIA PRÉ-MERGE / DEPLOY · GRAFOPARADA")
    steps = [
        check_files,
        check_gtfs_json,
        check_js_syntax,
        run_test_suite
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
