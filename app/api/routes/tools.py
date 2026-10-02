from __future__ import annotations

from fastapi import APIRouter

from app.core.tool_executor import ToolExecutor
from app.schemas.tool import ToolExecutionRequest

router = APIRouter()
executor = ToolExecutor()


@router.get("/tools")
async def list_tools() -> list[dict[str, str | bool]]:
    return [
        {"name": tool.name, "description": tool.description, "category": tool.category, "enabled": tool.enabled}
        for tool in executor.list_tools()
    ]


@router.post("/tools/execute")
async def execute_tool(payload: ToolExecutionRequest) -> dict[str, object]:
    result = await executor.execute(payload.tool_name, **(payload.arguments or {}))
    return result
