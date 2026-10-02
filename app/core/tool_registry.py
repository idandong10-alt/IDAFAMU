from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MemoryItem:
    key: str
    value: str
    tags: list[str] = field(default_factory=list)


class MemoryService:
    def __init__(self) -> None:
        self.memories: list[MemoryItem] = []

    def add(self, key: str, value: str, tags: list[str] | None = None) -> MemoryItem:
        item = MemoryItem(key=key, value=value, tags=tags or [])
        self.memories.append(item)
        return item

    def search(self, query: str) -> list[MemoryItem]:
        query_lower = query.lower().strip()
        if not query_lower:
            return self.memories
        return [item for item in self.memories if query_lower in item.key.lower() or query_lower in item.value.lower()]

    def summary(self) -> str:
        if not self.memories:
            return "No memories yet."
        return "\n".join(f"- {item.key}: {item.value}" for item in self.memories)
