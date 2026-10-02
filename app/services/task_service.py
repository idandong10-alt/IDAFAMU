from __future__ import annotations

from app.core.orchestrator import Orchestrator

_orchestrator = Orchestrator()


async def create_task(prompt: str) -> dict[str, str]:
    return await _orchestrator.handle(prompt)


def get_task_state(task_id: str) -> dict[str, str | None]:
    task = _orchestrator.task_engine.tasks.get(task_id)
    if not task:
        return {"error": "task_not_found"}
    return {
        "task_id": task.id,
        "status": task.status.value,
        "result": task.result,
        "error": task.error,
    }
