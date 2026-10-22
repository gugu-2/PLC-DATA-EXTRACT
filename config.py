"""
Configuration and Environment Management
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

try:
    from dotenv import load_dotenv
    # Load .env from project root
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        load_dotenv()
except ImportError:
    pass


@dataclass
class Settings:
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parent)
    
    # LLM Provider settings
    default_backend: str = field(
        default_factory=lambda: os.getenv("DEFAULT_BACKEND", "gemini").lower()
    )
    default_model: str = field(
        default_factory=lambda: os.getenv("DEFAULT_MODEL", "gemini-2.5-pro")
    )
    
    # API Keys
    gemini_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY")
    )
    openai_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY")
    )
    anthropic_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY")
    )
    groq_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("GROQ_API_KEY")
    )
    openrouter_api_key: Optional[str] = field(
        default_factory=lambda: os.getenv("OPENROUTER_API_KEY")
    )
    
    # Local Ollama / vLLM settings
    ollama_base_url: str = field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    
    # Swarm parameters
    concurrent_agents: int = field(
        default_factory=lambda: int(os.getenv("CONCURRENT_AGENTS", "8"))
    )
    token_consumption_level: str = field(
        default_factory=lambda: os.getenv("TOKEN_CONSUMPTION_LEVEL", "extreme")
    )
    min_code_characters: int = field(
        default_factory=lambda: int(os.getenv("MIN_CODE_CHARACTERS", "3500"))
    )
    target_code_characters: int = field(
        default_factory=lambda: int(os.getenv("TARGET_CODE_CHARACTERS", "65000"))
    )
    auto_repair: bool = field(
        default_factory=lambda: os.getenv("AUTO_REPAIR_ON_SYNTAX_ERROR", "true").lower() in ("true", "1", "yes")
    )
    infinite_loop: bool = field(
        default_factory=lambda: os.getenv("INFINITE_LOOP", "true").lower() in ("true", "1", "yes")
    )
    
    # Paths
    save_dir: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / os.getenv("SAVE_DIRECTORY", "data/raw")
    )
    exports_dir: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / os.getenv("EXPORTS_DIRECTORY", "data/exports")
    )
    log_dir: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / os.getenv("LOG_DIRECTORY", "data/logs")
    )

    def __post_init__(self):
        self.save_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


config = Settings()
