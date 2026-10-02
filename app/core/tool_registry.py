from __future__ import annotations

import json
import os
from typing import Any


class LLMProviderError(RuntimeError):
    pass


class BaseLLMProvider:
    def __init__(self, provider: str, model: str, api_key: str | None = None, base_url: str | None = None, temperature: float = 0.2):
        self.provider = provider
        self.model = model
        self.api_key = api_key or os.getenv(f"{provider.upper()}_API_KEY")
        self.base_url = base_url or os.getenv(f"{provider.upper()}_BASE_URL")
        self.temperature = temperature

    async def complete(self, messages: list[dict[str, str]], *, system_prompt: str | None = None) -> str:
        prompt_messages = list(messages)
        if system_prompt:
            prompt_messages = [{"role": "system", "content": system_prompt}, *messages]

        if self.provider == "openai" and self.api_key:
            try:
                from openai import OpenAI

                client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                response = client.chat.completions.create(
                    model=self.model,
                    messages=prompt_messages,
                    temperature=self.temperature,
                )
                text = response.choices[0].message.content
                if text:
                    return text
            except Exception:
                pass

        if self.provider == "ollama" and self.base_url:
            try:
                import httpx

                payload = {"model": self.model, "messages": prompt_messages, "stream": False}
                response = httpx.post(f"{self.base_url}/api/chat", json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content")
                if content:
                    return str(content)
            except Exception:
                pass

        if self.provider == "openrouter" and self.api_key:
            try:
                import httpx

                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {"model": self.model, "messages": prompt_messages}
                response = httpx.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()
                choice = data["choices"][0]
                return str(choice["message"]["content"])
            except Exception:
                pass

        return self._mock_response(prompt_messages, system_prompt)

    def _mock_response(self, messages: list[dict[str, str]], system_prompt: str | None = None) -> str:
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "Hello")
        if system_prompt:
            return f"[IDAFAMU mock response] System: {system_prompt}\nUser: {last_user}"
        return f"[IDAFAMU mock response] {last_user}"


class OpenAIProvider(BaseLLMProvider):
    pass


class AnthropicProvider(BaseLLMProvider):
    pass


class OpenRouterProvider(BaseLLMProvider):
    pass


class OllamaProvider(BaseLLMProvider):
    pass


def build_provider(provider: str, model: str, api_key: str | None = None, base_url: str | None = None, temperature: float = 0.2) -> BaseLLMProvider:
    mapping = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "openrouter": OpenRouterProvider,
        "ollama": OllamaProvider,
    }
    cls = mapping.get(provider, BaseLLMProvider)
    return cls(provider, model, api_key=api_key, base_url=base_url, temperature=temperature)
