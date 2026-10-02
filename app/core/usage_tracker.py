from __future__ import annotations


class UsageTracker:
    def __init__(self) -> None:
        self.events: list[dict[str, object]] = []

    def record(self, kind: str, payload: dict[str, object]) -> None:
        self.events.append({"kind": kind, **payload})

    def summary(self) -> dict[str, object]:
        return {
            "total_events": len(self.events),
            "chat_count": sum(1 for e in self.events if e["kind"] == "chat"),
            "task_count": sum(1 for e in self.events if e["kind"] == "task"),
            "tool_count": sum(1 for e in self.events if e["kind"] == "tool"),
        }
