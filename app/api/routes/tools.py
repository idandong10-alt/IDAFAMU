from __future__ import annotations

from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import create_agent_response

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    result = await create_agent_response(
        payload.message,
        model=payload.model,
        system_prompt=payload.system_prompt,
        context=[{"role": item.role, "content": item.content} for item in payload.context],
    )
    return ChatResponse(
        response=str(result["response"]),
        model=str(result["model"]),
        provider=str(result["provider"]),
        success=bool(result["success"]),
    )
