from __future__ import annotations

from typing import Any

from app.config import settings
from app.core.memory_service import MemoryService
from app.core.tool_registry import DEFAULT_TOOLS, ToolRegistry
from app.llm.providers import build_provider


class AgentRuntime:
    def __init__(self, default_model: str = "gpt-4o-mini") -> None:
        self.default_model = default_model
        self.memory = MemoryService()
        self.tool_registry = ToolRegistry()
        for tool in DEFAULT_TOOLS:
            self.tool_registry.register(tool)

    async def run(
        self,
        message: str,
        *,
        model: str | None = None,
        system_prompt: str | None = None,
        context: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        selected_model = model or self.default_model
        provider_name = self._provider_name(selected_model)

        provider = build_provider(
            provider_name,
            selected_model,
            api_key=self._api_key(provider_name),
            base_url=self._base_url(provider_name),
            temperature=0.2,
        )

        messages = [{"role": "user", "content": message}]
        if context:
            messages = [
                {"role": item["role"], "content": item["content"]}
                for item in context
            ] + [{"role": "user", "content": message}]

        text = await provider.complete(messages, system_prompt=system_prompt)
        self.memory.add("latest_message", message, tags=["chat"])
        return {
            "response": text,
            "model": selected_model,
            "provider": provider_name,
            "success": True,
        }

    def _provider_name(self, model: str) -> str:
        lowered = model.lower()
        if lowered.startswith("gpt") or "openai" in lowered:
            return "openai"
        if lowered.startswith("claude") or "anthropic" in lowered:
            return "anthropic"
        if lowered.startswith("openrouter") or "openrouter/" in lowered:
            return "openrouter"
        if lowered.startswith("llama") or "mistral" in lowered:
            return "ollama"
        return "openai"

    def _api_key(self, provider: str) -> str | None:
        mapping = {
            "openai": settings.openai_api_key,
            "anthropic": settings.anthropic_api_key,
            "openrouter": settings.openrouter_api_key,
            "ollama": None,
        }
        return mapping.get(provider)

    def _base_url(self, provider: str) -> str | None:
        mapping = {
            "openai": settings.openai_base_url,
            "anthropic": settings.anthropic_base_url,
            "openrouter": settings.openrouter_base_url,
            "ollama": settings.ollama_base_url,
        }
        return mapping.get(provider)
