from __future__ import annotations

from fastapi import APIRouter

from app.core.orchestrator import Orchestrator
from app.core.usage_tracker import UsageTracker

router = APIRouter()
tracker = UsageTracker()
orchestrator = Orchestrator()


@router.get("/dashboard/overview")
async def dashboard_overview() -> dict[str, object]:
    return {
        "sessions": 0,
        "tasks": len(orchestrator.task_engine.tasks),
        "usage": tracker.summary(),
        "status": "active",
    }
