from __future__ import annotations

from app.core.approval import ApprovalPolicy
from app.core.memory_recall import MemoryRecallService
from app.core.task_engine import TaskEngine, TaskStatus


class Orchestrator:
    def __init__(self) -> None:
        self.task_engine = TaskEngine()
        self.approval_policy = ApprovalPolicy()
        self.memory = MemoryRecallService()

    async def handle(self, prompt: str) -> dict[str, str]:
        task = self.task_engine.create_task(prompt)
        context = self.memory.search(prompt)
        if context:
            task.tool_plan.append({"memory": context})

        if "write" in prompt.lower() or "edit" in prompt.lower() or "run" in prompt.lower():
            task.status = TaskStatus.WAITING_FOR_APPROVAL
            return {
                "task_id": task.id,
                "status": "waiting_for_approval",
                "message": "This request may modify files or run commands. Approval required.",
            }

        task.status = TaskStatus.RUNNING
        result = f"Handled prompt: {prompt}. Relevant memory: {context}"
        self.task_engine.complete(task.id, result)
        return {
            "task_id": task.id,
            "status": "completed",
            "result": result,
        }
