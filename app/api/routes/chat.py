from __future__ import annotations

from fastapi import APIRouter

from app.core.tool_registry import DEFAULT_TOOLS

router = APIRouter()


@router.get("/tools")
async def list_tools() -> list[dict[str, str | bool]]:
    return [
        {"name": tool.name, "description": tool.description, "category": tool.category, "enabled": tool.enabled}
        for tool in DEFAULT_TOOLS
    ]
