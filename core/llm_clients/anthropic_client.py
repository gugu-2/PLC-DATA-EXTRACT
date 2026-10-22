"""
Anthropic Claude LLM Client Implementation
Supports Claude 3.5 Sonnet, Claude 3 Opus with high token outputs.
"""

import os
import json
from typing import Optional
import httpx
from core.llm_clients.base import BaseLLMClient
from config import config


class AnthropicClient(BaseLLMClient):
    """Asynchronous client for Anthropic Claude Messages API."""

    def __init__(self, model_name: str = "claude-3-5-sonnet-20241022", api_key: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or config.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY")
        self.base_url = "https://api.anthropic.com/v1/messages"

    def get_provider_name(self) -> str:
        return "anthropic"

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 8192
    ) -> str:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set in environment or .env file.")

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        payload = {
            "model": self.model_name,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        if system_prompt:
            payload["system"] = system_prompt

        timeout = httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(self.base_url, headers=headers, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Anthropic API error ({resp.status_code}): {resp.text}")

            data = resp.json()
            try:
                content_blocks = data.get("content", [])
                text_blocks = [b.get("text", "") for b in content_blocks if b.get("type") == "text"]
                return "".join(text_blocks).strip()
            except Exception as e:
                raise RuntimeError(f"Failed to parse Anthropic response: {e}\nRaw: {data}")
