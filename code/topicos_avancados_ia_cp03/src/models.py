import os
from pathlib import Path
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


class ModelClient:
    def __init__(self, provider="gemini", model_name="gemini-3.5-flash", temperature=0.7, max_output_tokens=None):
        self.provider = provider
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

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
        where = "remoto" if self.provider == "gemini" else "local · Ollama"
        return f"{getattr(self, 'last_model_used', self.model_name)} ({where})"

    # Modelos reserva caso o principal esteja sobrecarregado (erro 503)
    GEMINI_FALLBACKS = ["gemini-3.8-flash", "gemini-flash-latest", "gemini-3.1-flash-lite"]

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Gera resposta com o modelo configurado."""
        if self.provider == "gemini":
            import time
            from google.genai import errors

            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            )
            candidates = [self.model_name] + [m for m in self.GEMINI_FALLBACKS if m != self.model_name]
            last_err = None
            for model in candidates:
                for attempt in range(3):
                    try:
                        response = self.client.models.generate_content(
                            model=model, contents=user_prompt, config=config
                        )
                        self.last_model_used = model
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

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        res = self.client.chat(
            model=self.model_name, messages=messages, options={"temperature": self.temperature}
        )
        return res["message"]["content"].strip()
