from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select

from app.db.models import ChatMessageRecord, ChatSession
from app.db.session import SessionLocal


def create_chat_session(model_id: str | None = None, title: str | None = None) -> str:
    session_id = str(uuid.uuid4())
    with SessionLocal() as db:
        session = ChatSession(
            id=session_id,
            model_id=model_id,
            title=title or "New chat",
            created_at=datetime.now(timezone.utc),
        )
        db.add(session)
        db.commit()
    return session_id


def save_message(session_id: str, role: str, content: str) -> None:
    with SessionLocal() as db:
        message = ChatMessageRecord(
            id=str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=content,
        )
        db.add(message)
        db.commit()


def list_session_messages(session_id: str) -> list[dict[str, str]]:
    with SessionLocal() as db:
        rows = db.execute(
            select(ChatMessageRecord).where(ChatMessageRecord.session_id == session_id).order_by(ChatMessageRecord.created_at.asc())
        ).scalars().all()
    return [
        {"id": row.id, "role": row.role, "content": row.content, "created_at": row.created_at.isoformat()}
        for row in rows
    ]
