from __future__ import annotations

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    app_name: str = "IDAFAMU"
    default_model: str = "gpt-4o-mini"
    safe_mode: bool = True
    max_tool_calls: int = 8
    enable_memory: bool = True
