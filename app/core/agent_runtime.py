from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolDefinition:
    name: str
    description: str
    category: str = "general"
    enabled: bool = True


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition | None:
        return self._tools.get(name)

    def list(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    def enabled_tools(self) -> list[ToolDefinition]:
        return [tool for tool in self._tools.values() if tool.enabled]


DEFAULT_TOOLS = [
    ToolDefinition(name="filesystem_read", description="Read files from the active workspace", category="filesystem"),
    ToolDefinition(name="filesystem_write", description="Create or modify files inside the active workspace", category="filesystem"),
    ToolDefinition(name="shell_run", description="Run commands in a sandboxed project directory", category="shell"),
    ToolDefinition(name="web_search", description="Search the web when network access is enabled", category="web"),
    ToolDefinition(name="memory_save", description="Store a short memory fragment from the conversation", category="memory"),
]
