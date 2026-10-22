"""
Google Gemini LLM Client Implementation
Supports Gemini 2.5 Pro, 2.0 Flash, 1.5 Pro with large context and token limits.
"""

import os
import json
from typing import Optional
import httpx
from core.llm_clients.base import BaseLLMClient
from config import config


class GeminiClient(BaseLLMClient):
    """Asynchronous client for Google Gemini API."""

    def __init__(self, model_name: str = "gemini-2.5-pro", api_key: Optional[str] = None):
        super().__init__(model_name)
        self.api_key = api_key or config.gemini_api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # We don't raise immediately to allow instantiation in mock/test setups, but will check on call
            pass
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def get_provider_name(self) -> str:
        return "gemini"

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16384
    ) -> str:
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment or .env file.")

        url = f"{self.base_url}/{self.model_name}:generateContent?key={self.api_key}"
        
        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System Context:\n{system_prompt}\n\nPlease acknowledge."}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I am fully initialized with the requested persona and directives."}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "topP": 0.95
            }
        }

        # Generative models can take time for 65k+ char responses, set long timeout
        timeout = httpx.Timeout(connect=30.0, read=300.0, write=30.0, pool=30.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API error ({resp.status_code}): {resp.text}")
            
            data = resp.json()
            try:
                candidates = data.get("candidates", [])
                if not candidates:
                    raise RuntimeError("No candidate responses returned by Gemini API.")
                
                parts = candidates[0].get("content", {}).get("parts", [])
                text_chunks = [p.get("text", "") for p in parts if "text" in p]
                return "".join(text_chunks).strip()
            except Exception as e:
                raise RuntimeError(f"Failed to parse Gemini response: {e}\nRaw: {data}")
