from __future__ import annotations

from fastapi import APIRouter

from app.core.usage_tracker import UsageTracker

router = APIRouter()
tracker = UsageTracker()


@router.get("/analytics/summary")
async def analytics_summary() -> dict[str, object]:
    return tracker.summary()
