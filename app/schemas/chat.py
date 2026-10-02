from __future__ import annotations

from app.core.agent_runtime import AgentRuntime
from app.services.chat_store import create_chat_session, save_message

_runtime = AgentRuntime()


async def create_agent_response(
    message: str,
    *,
    model: str | None = None,
    system_prompt: str | None = None,
    context: list[dict[str, str]] | None = None,
    session_id: str | None = None,
) -> dict[str, str | bool]:
    if session_id is None:
        session_id = create_chat_session(model_id=model, title=(message[:60] if message else "New chat"))

    save_message(session_id, "user", message)
    result = await _runtime.run(message, model=model, system_prompt=system_prompt, context=context)
    save_message(session_id, "assistant", str(result["response"]))
    result["session_id"] = session_id
    return result
