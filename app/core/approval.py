from __future__ import annotations


class ApprovalPolicy:
    def __init__(self) -> None:
        self.safe_tools = {"filesystem_read", "web_search", "web_fetch"}
        self.risky_tools = {"filesystem_write", "shell_run"}

    def should_approve(self, tool_name: str) -> bool:
        if tool_name in self.safe_tools:
            return True
        if tool_name in self.risky_tools:
            return False
        return False

    def reason(self, tool_name: str) -> str:
        if tool_name in self.risky_tools:
            return "This tool can modify files or run commands. Approval required."
        return "Tool is considered low risk."
