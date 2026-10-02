from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.analytics import router as analytics_router
from app.api.routes.chat import router as chat_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.health import router as health_router
from app.api.routes.models import router as models_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.tools import router as tools_router


def register_routes(app: FastAPI) -> None:
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(models_router, prefix="/api/v1")
    app.include_router(chat_router, prefix="/api/v1")
    app.include_router(tools_router, prefix="/api/v1")
    app.include_router(tasks_router, prefix="/api/v1")
    app.include_router(dashboard_router, prefix="/api/v1")
    app.include_router(analytics_router, prefix="/api/v1")
