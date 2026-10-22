"""
Local Ollama & vLLM Client Implementation
Provides 100% offline synthetic data generation for high-spec local GPUs.
"""

import os
import json
from typing import Optional
import httpx
from core.llm_clients.base import BaseLLMClient
from config import config


class OllamaClient(BaseLLMClient):
    """Asynchronous client for local Ollama instances."""

    def __init__(self, model_name: str = "qwen2.5-coder:14b", base_url: Optional[str] = None):
        super().__init__(model_name)
        self.base_url = (base_url or config.ollama_base_url or "http://localhost:11434").rstrip("/")

    def get_provider_name(self) -> str:
        return "ollama"

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16384
    ) -> str:
        url = f"{self.base_url}/api/chat"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
                "num_ctx": 32768
            }
        }

        timeout = httpx.Timeout(connect=20.0, read=600.0, write=20.0, pool=20.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
                resp = await client.post(url, json=payload)
            except httpx.ConnectError:
                raise ConnectionError(
                    f"Could not connect to Ollama at {self.base_url}. "
                    "Ensure Ollama is running (`ollama serve`) or check OLLAMA_BASE_URL."
                )

            if resp.status_code != 200:
                raise RuntimeError(f"Ollama API error ({resp.status_code}): {resp.text}")

            data = resp.json()
            message = data.get("message", {})
            return message.get("content", "").strip()
