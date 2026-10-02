from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class ChatRecord(Base):
    __tablename__ = "chat_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str | None] = mapped_column(String, nullable=True)
    model_id: Mapped[str | None] = mapped_column(String, nullable=True)
    user_message: Mapped[str] = mapped_column(String, nullable=False)
    assistant_message: Mapped[str | None] = mapped_column(String, nullable=True)


class ToolRecord(Base):
    __tablename__ = "tool_records"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String, nullable=True)
    enabled: Mapped[bool] = mapped_column(default=True)
