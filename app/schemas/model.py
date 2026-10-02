from __future__ import annotations

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    id: str
    name: str
    provider: str
    enabled: bool = True
    supports_tools: bool = False


class ModelListResponse(BaseModel):
    models: list[ModelInfo]
