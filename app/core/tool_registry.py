from __future__ import annotations

import os
from typing import Any


class LLMProviderError(RuntimeError):
    pass


class BaseLLMProvider:
    def __init__(self, provider: str, model: str, api_key: str | None = None, base_url: str | None = None):
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.base_url = base_url or os.getenv(f"{provider.upper()}_BASE_URL")

    async def complete(self, messages: list[dict[str, str]], *, system_prompt: str | None = None) -> str:
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        if system_prompt:
            prompt = f"system: {system_prompt}\n{prompt}"
        return f"Mock response from {self.provider}/{self.model}: {prompt[:200]}"


class OpenAIProvider(BaseLLMProvider):
    pass


class AnthropicProvider(BaseLLMProvider):
    pass


class OpenRouterProvider(BaseLLMProvider):
    pass


class OllamaProvider(BaseLLMProvider):
    pass


def build_provider(provider: str, model: str, api_key: str | None = None, base_url: str | None = None) -> BaseLLMProvider:
    mapping = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "openrouter": OpenRouterProvider,
        "ollama": OllamaProvider,
    }
    cls = mapping.get(provider, BaseLLMProvider)
    return cls(provider, model, api_key=api_key, base_url=base_url)
