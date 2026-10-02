from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import create_agent_response
from app.services.chat_store import create_chat_session, list_session_messages, save_message

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    result = await create_agent_response(
        payload.message,
        model=payload.model,
        system_prompt=payload.system_prompt,
        context=[{"role": item.role, "content": item.content} for item in payload.context],
        session_id=payload.session_id,
    )
    return ChatResponse(
        response=str(result["response"]),
        model=str(result["model"]),
        provider=str(result["provider"]),
        session_id=str(result["session_id"]),
        success=bool(result["success"]),
    )


@router.post("/chat/stream")
async def stream_chat_endpoint(payload: ChatRequest) -> StreamingResponse:
    async def event_generator() -> Any:
        session_id = payload.session_id or create_chat_session(
            model_id=payload.model,
            title=(payload.message[:60] if payload.message else "New chat"),
        )

        save_message(session_id, "user", payload.message)

        yield "event: start\n"
        yield f"data: {json.dumps({'type': 'start', 'session_id': session_id})}\n\n"

        result = await create_agent_response(
            payload.message,
            model=payload.model,
            system_prompt=payload.system_prompt,
            context=[{"role": item.role, "content": item.content} for item in payload.context],
            session_id=session_id,
        )

        yield "event: chunk\n"
        yield f"data: {json.dumps({'type': 'chunk', 'content': str(result['response'])})}\n\n"

        yield "event: done\n"
        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id, 'model': result['model'], 'provider': result['provider']})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/chat/history/{session_id}")
async def chat_history(session_id: str) -> dict[str, Any]:
    messages = list_session_messages(session_id)
    return {"session_id": session_id, "messages": messages}
