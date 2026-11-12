#!/usr/bin/env python3
"""
==============================================================================
🤖 AUDITOR CÉTICO AUTOMATIZADO · DEEPSEEK REASONER (R1)
GrafoParada · Tópicos Avançados em IA (AI4Good) · UFRPE
Autor: Cauã da Cunha Lira (caua.lira@ufrpe.br)
==============================================================================
Este script automatiza a auditoria cética do projeto GrafoParada, gerando um
dossiê completo do estado do código, metodologia e slides, e acionando o modelo
de raciocínio profundo da DeepSeek (ou o DeepSeek Harness) para emitir parecer A1.
==============================================================================
"""

import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
PROMPT_FILE = Path(__file__).parent / "prompt_revisor_cetico.txt"
DOSSIE_OUT = Path(__file__).parent / "dossie_projeto_completo.md"
REPORT_OUT = WORKSPACE_ROOT / "va2" / "auditoria_cetica_deepseek.md"

def load_env_file(filepath):
    """Carrega variáveis de ambiente de arquivos .env ou segredos.env."""
    env_vars = {}
    if not filepath.exists():
        return env_vars
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip().strip('"').strip("'")
    except Exception as e:
        print(f"⚠️ Erro lendo {filepath}: {e}")
    return env_vars

def compile_project_dossier():
    """Varre os arquivos centrais do GrafoParada e compila um dossiê técnico conciso."""
    print("📦 [1/3] Compilando dossiê técnico do GrafoParada...")
    
    sections = []
    sections.append("# 📋 DOSSIÊ TÉCNICO OFICIAL · GRAFOPARADA (UFRPE 2026)\n")
    
    # 1. Metodologia A1 e Abandono
    ref_file = WORKSPACE_ROOT / "papers" / "referencial_teorico_a1_abandono.md"
    if ref_file.exists():
        sections.append("## 1. FUNDAMENTAÇÃO TEÓRICA & ESTADO DA ARTE A1")
        sections.append(ref_file.read_text(encoding="utf-8")[:3000] + "\n...\n")
        
    # 2. Defesa da Banca no Roteiro
    roteiro_file = WORKSPACE_ROOT / "code" / "grafoparada_web" / "roteiro.html"
    if roteiro_file.exists():
        sections.append("## 2. RESPOSTAS À BANCA NO ROTEIRO DE APRESENTAÇÃO")
        content = roteiro_file.read_text(encoding="utf-8")
        if "Banca Cética" in content or "qa-box" in content:
            idx = content.find("qa-box")
            sections.append(content[idx:idx+4000] + "\n...\n")
            
    # 3. Código ST-GCN e Métricas
    stgcn_file = WORKSPACE_ROOT / "code" / "grafoparada_tec" / "stgcn_grafoparada.py"
    if stgcn_file.exists():
        sections.append("## 3. ARQUITETURA ST-GCN (RESUMO)")
        lines = stgcn_file.read_text(encoding="utf-8").splitlines()
        code_summary = "\n".join([l for l in lines[:120] if not l.startswith("#") or "CLASS" in l or "DEF" in l])
        sections.append(f"```python\n{code_summary[:2500]}\n```\n")

    dossie_text = "\n\n".join(sections)
    DOSSIE_OUT.write_text(dossie_text, encoding="utf-8")
    print(f"  ✓ Dossiê gerado com sucesso: {DOSSIE_OUT.name} ({len(dossie_text)} caracteres)")
    return dossie_text

def run_deepseek_audit(dossie_text):
    """Executa a auditoria cética via API DeepSeek Reasoner (R1) ou prepara para dsh."""
    print("🧠 [2/3] Verificando credenciais e motor DeepSeek...")
    
    # Busca chave no ambiente ou em segredos.env / .env
    env_vars = {}
    env_vars.update(load_env_file(WORKSPACE_ROOT / ".env"))
    env_vars.update(load_env_file(WORKSPACE_ROOT / "segredos.env"))
    
    api_key = os.environ.get("DEEPSEEK_API_KEY") or env_vars.get("DEEPSEEK_API_KEY")
    system_prompt = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else "Atue como revisor cético A1."

    if not api_key:
        print("\n" + "="*70)
        print("💡 [AVISO: CHAVE DEEPSEEK NÃO DETECTADA EM segredos.env]")
        print("="*70)
        print("Para que a IA gere o relatório 100% de forma automática pelo script:")
        print("1. Obtenha sua chave em https://platform.deepseek.com")
        print("2. Adicione ao arquivo segredos.env a linha:")
        print("   DEEPSEEK_API_KEY=sk-sua-chave-aqui\n")
        print("OU execute o DeepSeek Harness localmente via terminal:")
        print("   npx @deepseek-ai/dsh web\n")
        print("OU copie o dossiê pronto e cole no DeepSeek Web (chat.deepseek.com):")
        print(f"   Arquivo gerado: {DOSSIE_OUT}")
        print("="*70 + "\n")
        return False

    print("🚀 [3/3] Enviando dossiê para a API DeepSeek Reasoner (DeepSeek-R1)...")
    url = "https://api.deepseek.com/chat/completions"
    payload = {
        "model": "deepseek-reasoner",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Aqui está o dossiê técnico completo do GrafoParada para sua auditoria implacável:\n\n{dossie_text}"}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            
        choice = res_data["choices"][0]["message"]
        reasoning = choice.get("reasoning_content", "")
        content = choice.get("content", "")
        
        final_report = f"""# 🛡️ PARECER CÉTICO OFICIAL · DEEPSEEK REASONER (R1)
> **Data de Auditoria:** 11/11/2026 · UFRPE / AI4Good  
> **Modelo:** DeepSeek-R1 (`deepseek-reasoner`) · Modo de Raciocínio Profundo  
> **Alvo:** GrafoParada (Cauã da Cunha Lira / Prof. Lucas Silva Figueiredo)

---

## 🧠 Cadeia de Raciocínio Crítico (Reasoning Trace)
{reasoning}

---

## 📋 Parecer da Banca Cética
{content}
"""
        REPORT_OUT.write_text(final_report, encoding="utf-8")
        print(f"✅ [SUCESSO] Auditoria concluída! Relatório salvo em:\n   {REPORT_OUT}")
        return True
        
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"❌ Erro na API DeepSeek ({e.code}): {err_msg}")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão com DeepSeek: {e}")
        return False

if __name__ == "__main__":
    dossie = compile_project_dossier()
    success = run_deepseek_audit(dossie)
    if not success:
        sys.exit(0)
