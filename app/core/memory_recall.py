from __future__ import annotations


class MemoryRecallService:
    def __init__(self) -> None:
        self.memory_store: list[dict[str, str]] = []

    def add_memory(self, key: str, value: str) -> None:
        self.memory_store.append({"key": key, "value": value})

    def search(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        q = query.lower()
        matches: list[dict[str, str]] = []
        for item in self.memory_store:
            haystack = f"{item['key']} {item['value']}".lower()
            if q in haystack:
                matches.append(item)
        return matches[:limit]
