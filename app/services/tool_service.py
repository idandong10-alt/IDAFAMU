from __future__ import annotations

from app.core.tool_executor import ToolExecutor

executor = ToolExecutor()


async def execute_tool_call(tool_name: str, **kwargs: object) -> dict[str, object]:
    return await executor.execute(tool_name, **kwargs)
