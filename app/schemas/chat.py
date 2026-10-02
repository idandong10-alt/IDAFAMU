from __future__ import annotations

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="Message role: user or assistant")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User prompt")
    model: str | None = Field(default=None, description="Model ID to use")
    system_prompt: str | None = Field(default=None, description="Optional system prompt")
    context: list[ChatMessage] = Field(default_factory=list, description="Optional prior conversation")


class ChatResponse(BaseModel):
    response: str
    model: str
    provider: str
    success: bool = True
