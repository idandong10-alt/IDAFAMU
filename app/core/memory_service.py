from __future__ import annotations

from dataclasses import dataclass, field


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
    ToolDefinition(name="filesystem_read", description="Read files from a working directory", category="filesystem"),
    ToolDefinition(name="filesystem_write", description="Write or edit files in a working directory", category="filesystem"),
    ToolDefinition(name="shell_run", description="Run shell commands in a sandboxed project directory", category="shell"),
    ToolDefinition(name="web_search", description="Search the web when network access is available", category="web"),
    ToolDefinition(name="memory_save", description="Store a memory snippet from the conversation", category="memory"),
]
