import httpx
from typing import Any, Dict, List, Optional

from app.config.settings import settings


class OllamaClient:
    def __init__(self, base_url: str = None):
        self.base_url = base_url or str(settings.OLLAMA_URL).rstrip("/")
        self.client = httpx.AsyncClient(base_url=self.base_url, timeout=60)

    async def generate(self, model: str, prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> str:
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        response = await self.client.post("/v1/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        # Ollama returns streams; for simplicity assume output in data["output"][0]["content"]
        if isinstance(data, dict):
            output = data.get("output")
            if isinstance(output, list) and output:
                first = output[0]
                return first.get("content", "").strip()
        return ""

    async def embed(self, model: str, input: str) -> List[float]:
        payload = {"model": model, "input": input}
        response = await self.client.post("/v1/embeddings", json=payload)
        response.raise_for_status()
        data = response.json()
        vectors = data.get("data")
        if not vectors or not isinstance(vectors, list):
            raise ValueError("Unexpected embedding response")
        return vectors[0].get("embedding", [])


ollama = OllamaClient()
