# 🤖 DeepSeek Harness (DSH) · Auditoria Cética Automatizada
> **Módulo Oficial de Crítica e Auditoria:** `core/harness/deepseek/`  
> **Projeto:** GrafoParada · UFRPE / AI4Good 2026  
> **Autor:** Cauã da Cunha Lira (`caua.lira@ufrpe.br`)  
> **Orientador:** Prof. Lucas Silva Figueiredo  

---

## 🎯 Objetivo
Fornecer um auditor automatizado independente baseado no **DeepSeek-R1 (DeepSeek Reasoner)** e no **DeepSeek Harness (`@deepseek-ai/dsh`)**, submetendo todo o código, metodologia e slides do GrafoParada a um crivo rigoroso antes da apresentação de terça-feira.

---

## 🛠️ O que foi Instalado e Configurado

1. **Core Runtime do DeepSeek Harness (`@deepseek-ai/dsh` v0.2.2-rc.1)**:
   - Baixado e compilado no cache local de pacotes Node.js (v24.19.0).
   - Compatível nativamente com Windows PowerShell (`pwsh-sandbox`).

2. **Arquivos do Módulo (`core/harness/deepseek/`)**:
   - [`prompt_revisor_cetico.txt`](prompt_revisor_cetico.txt): Prompt mestre calibrado para simular um revisor de periódicos A1 (*Transportation Research Part A*) e membro implacável da banca da UFRPE.
   - [`dsh.config.yaml`](dsh.config.yaml): Perfil configurado para inspecionar `code/`, `papers/` e `va2/`.
   - [`revisor_cetico.py`](revisor_cetico.py): Pipeline Python automatizado que compila o dossiê e consulta a API DeepSeek Reasoner.
   - [`dossie_projeto_completo.md`](dossie_projeto_completo.md): Dossiê compilado de 9.700 caracteres contendo toda a metodologia, código ST-GCN e respostas da banca.
   - [`iniciar_dsh.ps1`](iniciar_dsh.ps1): Atalho PowerShell para subir o painel web interativo.

---

## 🚀 Como Usar no Dia a Dia

### Modo 1: Auditoria 100% Automática via Python
Se você possui uma chave da API DeepSeek:
1. Adicione a chave no arquivo `segredos.env` (que nunca vai para o Git):
   ```env
   DEEPSEEK_API_KEY=sk-sua-chave-aqui
   ```
2. Execute o auditor no terminal:
   ```powershell
   uv run python core/harness/deepseek/revisor_cetico.py
   ```
3. O modelo **DeepSeek-R1** processará o dossiê com raciocínio profundo e salvará o parecer em:
   `va2/auditoria_cetica_deepseek.md`

---

### Modo 2: Interface Web Interativa do DeepSeek Harness
Para operar via navegador através do painel oficial do DeepSeek Harness:
```powershell
npx @deepseek-ai/dsh web
```
*(ou execute o script `core/harness/deepseek/iniciar_dsh.ps1`)*

O servidor local iniciará e abrirá automaticamente o navegador com a interface do agente, ferramentas de terminal, sistema de arquivos e suporte a plugins Cordis.

---

### Modo 3: Gratuito via DeepSeek Web (Sem necessidade de Chave API)
Caso não queira gastar créditos de API:
1. Abra o [chat.deepseek.com](https://chat.deepseek.com) no navegador ou app;
2. Ative a chave **DeepThink (R1)**;
3. Copie o conteúdo de [`prompt_revisor_cetico.txt`](prompt_revisor_cetico.txt) e [`dossie_projeto_completo.md`](dossie_projeto_completo.md);
4. O modelo gerará a auditoria completa instantaneamente na sua tela.
