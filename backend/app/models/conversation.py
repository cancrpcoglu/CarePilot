"""Hasta-agent konuşma oturumu modeli."""

import enum
import uuid

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class ConversationMode(str, enum.Enum):
    """Agent'ın bu oturumda çalıştığı mod."""

    TRIAGE = "triage"
    FOLLOWUP = "followup"


class Conversation(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "conversations"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )
    mode: Mapped[ConversationMode] = mapped_column(
        SAEnum(ConversationMode, name="conversation_mode"), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Conversation {self.id} ({self.mode.value})>"
