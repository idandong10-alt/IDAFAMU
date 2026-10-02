from __future__ import annotations

from fastapi import APIRouter

from app.config import settings

router = APIRouter()


@router.get("/app-info")
async def app_info() -> dict[str, str | bool]:
    return {
        "app_name": settings.app_name,
        "default_model": settings.default_model,
        "debug": settings.debug,
        "database_url": settings.database_url,
    }
