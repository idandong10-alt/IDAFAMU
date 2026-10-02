from __future__ import annotations


class WorkspaceManager:
    def __init__(self) -> None:
        self.workspaces: dict[str, dict[str, object]] = {}

    def create_workspace(self, name: str) -> str:
        workspace_id = f"ws-{len(self.workspaces) + 1}"
        self.workspaces[workspace_id] = {"name": name, "files": []}
        return workspace_id

    def list_workspaces(self) -> list[dict[str, object]]:
        return [
            {"id": wid, "name": data["name"], "files": data.get("files", [])}
            for wid, data in self.workspaces.items()
        ]
