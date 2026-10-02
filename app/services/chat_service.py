from __future__ import annotations

from typing import Any

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

    async def run(self, message: str, *, model: str | None = None, system_prompt: str | None = None, context: list[dict[str, str]] | None = None) -> dict[str, Any]:
        selected_model = model or self.default_model
        provider_name = selected_model.split("/", 1)[0] if "/" in selected_model else "openai"

        if provider_name == "gpt":
            provider_name = "openai"

        provider = build_provider(provider_name, selected_model)

        messages = [
            {"role": "user", "content": message},
        ]
        if context:
            messages = [
                {"role": item["role"], "content": item["content"]}
                for item in context
            ] + [{"role": "user", "content": message}]

        response = await provider.complete(messages, system_prompt=system_prompt)
        return {
            "response": response,
            "model": selected_model,
            "provider": provider_name,
            "success": True,
        }
