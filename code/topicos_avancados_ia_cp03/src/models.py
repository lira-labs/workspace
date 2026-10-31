import os
import json
import urllib.parse
import urllib.request
from pathlib import Path
from typing import List, Dict, Optional
from google import genai
from google.genai import types
import ollama


def load_env_key():
    """Carrega GEMINI_API_KEY a partir de .env (raiz do workspace) se não estiver no os.environ."""
    if "GEMINI_API_KEY" in os.environ:
        return os.environ["GEMINI_API_KEY"]
    env_path = Path(__file__).resolve().parents[3] / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    os.environ["GEMINI_API_KEY"] = val
                    return val
    return None


def runtime_web_search(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    """Ferramenta de pesquisa na web em tempo de execução (Item 4 · arn·c).

    Consulta a API pública da Wikipedia/DuckDuckGo Instant Answer para recuperar fatos,
    datas e referências reais durante o debate dos agentes na arena.
    """
    results: List[Dict[str, str]] = []
    try:
        encoded = urllib.parse.quote(query[:120])
        url = f"https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded}&utf8=&format=json&srlimit={max_results}"
        req = urllib.request.Request(url, headers={"User-Agent": "AI4Good-ArenaMultiagente/1.0 (UFRPE)"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("query", {}).get("search", []):
                snippet = (
                    item.get("snippet", "")
                    .replace('<span class="searchmatch">', "")
                    .replace("</span>", "")
                )
                results.append(
                    {
                        "title": item.get("title", ""),
                        "snippet": snippet,
                        "url": f"https://pt.wikipedia.org/wiki/{urllib.parse.quote(item.get('title', '').replace(' ', '_'))}",
                    }
                )
    except Exception:
        pass
    return results


class ModelClient:
    def __init__(
        self,
        provider: str = "gemini",
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.7,
        max_output_tokens: Optional[int] = None,
        num_ctx: int = 8192,
        thinking_budget: int = 2048,
        web_search: bool = True,
        reasoning_mode: bool = True,
    ):
        self.provider = provider
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.num_ctx = num_ctx
        self.thinking_budget = thinking_budget
        self.web_search = web_search
        self.reasoning_mode = reasoning_mode
        self.last_thoughts: str = ""
        self.last_search_results: List[Dict[str, str]] = []

        if self.provider == "gemini":
            api_key = load_env_key()
            if not api_key:
                raise ValueError("GEMINI_API_KEY não encontrada no ambiente nem no arquivo .env")
            self.client = genai.Client(api_key=api_key)
        elif self.provider == "ollama":
            self.client = ollama
        else:
            raise ValueError(f"Provedor desconhecido: {self.provider}")

    @property
    def label(self) -> str:
         where = "remoto · Search+Thinking" if self.provider == "gemini" else "local · Ollama+Reasoning"
         return f"{getattr(self, 'last_model_used', self.model_name)} ({where})"

    # Modelos reserva caso o principal esteja sobrecarregado (erro 503)
    GEMINI_FALLBACKS = ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-flash-latest"]

    def generate(self, system_prompt: str, user_prompt: str, search_query: Optional[str] = None) -> str:
        """Gera resposta com busca na web em tempo de execução (Item 4) e cadeia de raciocínio (Item 5)."""
        web_context = ""
        if self.web_search:
            q = search_query or user_prompt.splitlines()[0][:100]
            self.last_search_results = runtime_web_search(q)
            if self.last_search_results:
                snippets = "\n".join(
                    f"- [{r['title']}]({r['url']}): {r['snippet']}" for r in self.last_search_results
                )
                web_context = f"\n\n[EVIDÊNCIAS DE BUSCA WEB EM TEMPO DE EXECUÇÃO]:\n{snippets}\n"

        enriched_prompt = f"{user_prompt}{web_context}"

        if self.provider == "gemini":
            import time
            from google.genai import errors

            tools = [types.Tool(google_search=types.GoogleSearch())] if self.web_search else None
            thinking_cfg = (
                types.ThinkingConfig(include_thoughts=True, thinking_budget=self.thinking_budget)
                if self.reasoning_mode and self.thinking_budget > 0
                else None
            )

            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
                tools=tools,
                thinking_config=thinking_cfg,
            )
            candidates = [self.model_name] + [m for m in self.GEMINI_FALLBACKS if m != self.model_name]
            last_err = None
            for model in candidates:
                for attempt in range(3):
                    try:
                        response = self.client.models.generate_content(
                            model=model, contents=enriched_prompt, config=config
                        )
                        self.last_model_used = model
                        # Extrai cadeia de raciocínio (thoughts) se retornada pelo modelo
                        thoughts = []
                        if response.candidates and response.candidates[0].content:
                            for part in response.candidates[0].content.parts or []:
                                if getattr(part, "thought", False) and part.text:
                                    thoughts.append(part.text.strip())
                        self.last_thoughts = "\n".join(thoughts)
                        return response.text.strip() if response.text else ""
                    except errors.ServerError as e:  # 503/500: sobrecarga temporária
                        last_err = e
                        wait = 10 * (attempt + 1)
                        print(f"[aviso] {model} indisponível ({e.code}); nova tentativa em {wait}s...")
                        time.sleep(wait)
                    except errors.ClientError as e:  # 404 etc.: tenta o próximo modelo
                        last_err = e
                        break
            raise RuntimeError(f"Todos os modelos Gemini falharam: {last_err}")

        # Execução local via Ollama com cadeia de raciocínio (<thinking>) e contexto controlado (num_ctx)
        reasoning_instruction = (
            "\nAntes da resposta final, elabore sua reflexão crítica passo a passo dentro de uma tag "
            "<thinking>...</thinking> analisando premissas, dados da busca web e contradições."
            if self.reasoning_mode
            else ""
        )
        messages = [
            {"role": "system", "content": f"{system_prompt}{reasoning_instruction}"},
            {"role": "user", "content": enriched_prompt},
        ]
        res = self.client.chat(
            model=self.model_name,
            messages=messages,
            options={"temperature": self.temperature, "num_ctx": self.num_ctx},
        )
        return res["message"]["content"].strip()
