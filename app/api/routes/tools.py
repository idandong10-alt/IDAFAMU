from __future__ import annotations

from fastapi import APIRouter

from app.llm.providers import ProviderRouter
from app.schemas.model import ModelListResponse

router = APIRouter()
provider_router = ProviderRouter()


@router.get("/models", response_model=ModelListResponse)
async def list_models() -> ModelListResponse:
    return ModelListResponse(models=provider_router.list_models())
