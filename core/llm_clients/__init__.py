"""
LLM Client Factory
Instantiates and configures the requested backend provider.
"""

from typing import Optional
from core.llm_clients.base import BaseLLMClient
from core.llm_clients.gemini_client import GeminiClient
from core.llm_clients.openai_client import OpenAICompatibleClient
from core.llm_clients.anthropic_client import AnthropicClient
from core.llm_clients.ollama_client import OllamaClient
from core.llm_clients.mock_client import MockClient


def create_llm_client(
    backend: str = "gemini",
    model: Optional[str] = None,
    **kwargs
) -> BaseLLMClient:
    """
    Factory creating a configured BaseLLMClient instance.
    Supported backends: 'gemini', 'openai', 'anthropic', 'groq', 'openrouter', 'ollama', 'mock'.
    """
    backend = backend.lower()

    if backend == "gemini":
        model_name = model or "gemini-2.5-pro"
        return GeminiClient(model_name=model_name, **kwargs)

    elif backend == "openai":
        model_name = model or "gpt-4o"
        return OpenAICompatibleClient(model_name=model_name, provider_name="openai", **kwargs)

    elif backend == "groq":
        model_name = model or "deepseek-r1-distill-llama-70b"
        return OpenAICompatibleClient(
            model_name=model_name,
            base_url="https://api.groq.com/openai/v1",
            provider_name="groq",
            **kwargs
        )

    elif backend == "openrouter":
        model_name = model or "deepseek/deepseek-r1"
        return OpenAICompatibleClient(
            model_name=model_name,
            base_url="https://openrouter.ai/api/v1",
            provider_name="openrouter",
            **kwargs
        )

    elif backend == "anthropic":
        model_name = model or "claude-3-5-sonnet-20241022"
        return AnthropicClient(model_name=model_name, **kwargs)

    elif backend == "ollama":
        model_name = model or "qwen2.5-coder:14b"
        return OllamaClient(model_name=model_name, **kwargs)

    elif backend == "mock":
        model_name = model or "mock-generator"
        return MockClient(model_name=model_name)

    else:
        raise ValueError(
            f"Unsupported backend '{backend}'. "
            "Supported: 'gemini', 'openai', 'anthropic', 'groq', 'openrouter', 'ollama', 'mock'."
        )
