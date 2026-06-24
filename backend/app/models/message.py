"""Konuşma mesajı modeli."""

import enum
import uuid

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class MessageRole(str, enum.Enum):
    """Mesajı kimin gönderdiği."""

    USER = "user"
    AGENT = "agent"


class Message(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "messages"

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id"), nullable=False, index=True
    )
    role: Mapped[MessageRole] = mapped_column(
        SAEnum(MessageRole, name="message_role"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self) -> str:
        return f"<Message {self.role.value}>"
