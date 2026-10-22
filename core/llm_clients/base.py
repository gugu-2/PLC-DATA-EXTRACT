"""
Abstract Base LLM Client Interface
Defines the standard asynchronous contract for all LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseLLMClient(ABC):
    """Abstract base class for asynchronous LLM client implementations."""

    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.extra_config = kwargs

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 16384
    ) -> str:
        """
        Asynchronously generates a complete response from the LLM.
        """
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Returns the identifier name of the provider."""
        pass
