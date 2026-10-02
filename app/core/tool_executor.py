from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from app.tools.filesystem import list_dir, read_file, write_file
from app.tools.shell import run_shell_command
from app.tools.web import fetch_url, web_search


@dataclass
class ToolDefinition:
    name: str
    description: str
    category: str = "general"
    enabled: bool = True


class ToolExecutor:
    def __init__(self) -> None:
        self._registry: dict[str, Callable[..., Any]] = {
            "filesystem_list": list_dir,
            "filesystem_read": read_file,
            "filesystem_write": write_file,
            "shell_run": run_shell_command,
            "web_search": web_search,
            "web_fetch": fetch_url,
        }

    def list_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(name="filesystem_list", description="List files and folders inside the project", category="filesystem"),
            ToolDefinition(name="filesystem_read", description="Read a file from the project workspace", category="filesystem"),
            ToolDefinition(name="filesystem_write", description="Write text to a file in the project workspace", category="filesystem"),
            ToolDefinition(name="shell_run", description="Run a shell command inside the project directory", category="shell"),
            ToolDefinition(name="web_search", description="Search the web for information", category="web"),
            ToolDefinition(name="web_fetch", description="Fetch a web page and return its content", category="web"),
        ]

    async def execute(self, tool_name: str, **kwargs: Any) -> dict[str, Any]:
        if tool_name not in self._registry:
            return {"ok": False, "error": f"Unknown tool: {tool_name}"}

        handler = self._registry[tool_name]
        try:
            result = handler(**kwargs)
            if hasattr(result, "__await__"):
                result = await result
            return {"ok": True, "tool": tool_name, "result": result}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "tool": tool_name, "error": str(exc)}
