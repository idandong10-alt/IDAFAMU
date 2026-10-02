from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IDAFAMU"
    debug: bool = False
    database_url: str = "sqlite:///./idafamu.db"
    default_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    anthropic_api_key: str | None = None
    anthropic_base_url: str | None = None
    openrouter_api_key: str | None = None
    openrouter_base_url: str | None = None
    ollama_base_url: str | None = "http://localhost:11434"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
