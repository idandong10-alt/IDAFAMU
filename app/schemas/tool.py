from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ToolExecutionRequest:
    tool_name: str
    arguments: dict[str, object] | None = None


@dataclass
class ToolExecutionResponse:
    ok: bool
    tool: str
    result: object | None = None
    error: str | None = None
