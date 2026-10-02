from __future__ import annotations

from fastapi import APIRouter

from app.services.task_service import create_task, get_task_state

router = APIRouter()


@router.post("/tasks")
async def create_task_endpoint(prompt: str) -> dict[str, str]:
    return await create_task(prompt)


@router.get("/tasks/{task_id}")
async def get_task_endpoint(task_id: str) -> dict[str, str | None]:
    return get_task_state(task_id)
