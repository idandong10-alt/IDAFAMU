from __future__ import annotations

import subprocess


async def run_shell_command(command: str, cwd: str = ".", timeout: int = 20) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
