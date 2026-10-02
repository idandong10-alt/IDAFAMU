from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class LLMProviderConfig:
    provider: str
    model: str
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = None


class LLMProviderSettings(BaseModel):
    provider: Literal["openai", "anthropic", "openrouter", "ollama"] = "openai"
    model: str = "gpt-4o-mini"
    api_key: str | None = None
    base_url: str | None = None
    temperature: float = 0.2
    max_tokens: int | None = Field(default=None, ge=1)


@lru_cache(maxsize=16)
def get_provider_config(provider: str, model: str) -> LLMProviderConfig:
    return LLMProviderConfig(
        provider=provider,
        model=model,
        api_key=None,
        base_url=None,
        temperature=0.2,
        max_tokens=None,
    )


class ProviderRouter:
    """Simple abstraction for selecting an LLM provider and model."""

    def __init__(self) -> None:
        self.providers = {
            "openai": "OpenAI",
            "anthropic": "Anthropic",
            "openrouter": "OpenRouter",
            "ollama": "Ollama",
        }

    def list_models(self) -> list[dict[str, str | bool]]:
        return [
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai", "enabled": True, "supports_tools": True},
            {"id": "claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "provider": "anthropic", "enabled": True, "supports_tools": True},
            {"id": "openrouter/auto", "name": "OpenRouter Auto", "provider": "openrouter", "enabled": True, "supports_tools": True},
            {"id": "llama3.1", "name": "Llama 3.1", "provider": "ollama", "enabled": True, "supports_tools": False},
        ]

    def get_model(self, model_id: str | None) -> dict[str, str | bool]:
        if model_id is None:
            return self.list_models()[0]
        for model in self.list_models():
            if str(model["id"]) == model_id:
                return model
        return self.list_models()[0]
