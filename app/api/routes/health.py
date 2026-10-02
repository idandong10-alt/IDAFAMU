from __future__ import annotations

import uuid

from app.core.agent_runtime import AgentRuntime

_runtime = AgentRuntime()


async def create_agent_response(
    message: str,
    *,
    model: str | None = None,
    system_prompt: str | None = None,
    context: list[dict[str, str]] | None = None,
) -> dict[str, str | bool]:
    result = await _runtime.run(message, model=model, system_prompt=system_prompt, context=context)
    result["session_id"] = str(uuid.uuid4())
    return result
