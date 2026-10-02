from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_FOR_APPROVAL = "waiting_for_approval"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    id: str
    user_prompt: str
    status: TaskStatus = TaskStatus.QUEUED
    tool_plan: list[dict[str, Any]] = field(default_factory=list)
    result: str | None = None
    error: str | None = None


class TaskEngine:
    def __init__(self) -> None:
        self.tasks: dict[str, Task] = {}

    def create_task(self, prompt: str) -> Task:
        task = Task(id=f"task-{len(self.tasks) + 1}", user_prompt=prompt)
        self.tasks[task.id] = task
        return task

    def update_status(self, task_id: str, status: TaskStatus) -> None:
        self.tasks[task_id].status = status

    def add_tool_plan(self, task_id: str, tool_name: str, args: dict[str, Any]) -> None:
        self.tasks[task_id].tool_plan.append({"tool": tool_name, "args": args})

    def complete(self, task_id: str, result: str) -> None:
        self.tasks[task_id].status = TaskStatus.COMPLETED
        self.tasks[task_id].result = result

    def fail(self, task_id: str, error: str) -> None:
        self.tasks[task_id].status = TaskStatus.FAILED
        self.tasks[task_id].error = error
