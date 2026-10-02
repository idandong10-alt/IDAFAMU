from __future__ import annotations

import os
from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "IDAFAMU"
    debug: bool = bool(os.getenv("DEBUG", "false").lower() == "true")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./idafamu.db")
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    ollama_base_url: str | None = os.getenv("OLLAMA_BASE_URL")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
