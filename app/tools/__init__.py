from __future__ import annotations

from app.core.agent_runtime import AgentRuntime

_runtime = AgentRuntime()


async def get_runtime_tools() -> list[dict[str, str | bool]]:
    return [
        {"name": tool.name, "description": tool.description, "category": tool.category, "enabled": tool.enabled}
        for tool in _runtime.tool_registry.list()
    ]
