"""
OpenAI & OpenAI-Compatible LLM Client
Supports OpenAI, Groq, OpenRouter, DeepSeek, and custom OpenAI-compatible endpoints.
"""

import os
import json
from typing import Optional, Dict, Any
import httpx
from core.llm_clients.base import BaseLLMClient
from config import config


class OpenAICompatibleClient(BaseLLMClient):
    """Universal asynchronous client for OpenAI-compatible Chat Completion APIs."""

    def __init__(
        self,
        model_name: str = "gpt-4o",
        api_key: Optional[str] = None,
        base_url: str = "https://api.openai.com/v1",
        provider_name: str = "openai"
    ):
        super().__init__(model_name)
        self.provider_name = provider_name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or self._resolve_api_key()

    def _resolve_api_key(self) -> Optional[str]:
        if self.provider_name == "openai":
            return config.openai_api_key or os.getenv("OPENAI_API_KEY")
        elif self.provider_name == "groq":
            return config.groq_api_key or os.getenv("GROQ_API_KEY")
        elif self.provider_name == "openrouter":
            return config.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
        return os.getenv("OPENAI_API_KEY")

    def get_provider_name(self) -> str:
        return self.provider_name

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16384
    ) -> str:
        if not self.api_key:
            raise ValueError(f"API key for provider '{self.provider_name}' is not set.")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload: Dict[str, Any] = {
            "model": self.model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        timeout = httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"{self.provider_name} API error ({resp.status_code}): {resp.text}")

            data = resp.json()
            try:
                choices = data.get("choices", [])
                if not choices:
                    raise RuntimeError(f"No choices returned from {self.provider_name} API.")
                return choices[0]["message"]["content"].strip()
            except Exception as e:
                raise RuntimeError(f"Failed to parse {self.provider_name} response: {e}\nRaw: {data}")
