from typing import Dict, Any
from .models import ModelClient

class Agent:
    def __init__(self, key: str, config: Dict[str, Any], model_client: ModelClient):
        self.key = key
        self.name = config.get("name", key)
        self.role = config.get("role", "")
        self.system_prompt = config.get("system_prompt", "").strip()
        self.client = model_client

    def act(self, prompt: str) -> str:
        """Executa um turno de raciocínio e fala do agente."""
        return self.client.generate(self.system_prompt, prompt)
