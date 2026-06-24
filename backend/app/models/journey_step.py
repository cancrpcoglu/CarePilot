"""Hasta yolculuğu adımı modeli (ameliyat öncesi/sonrası checklist)."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class JourneyStepStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class JourneyStep(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "journey_steps"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )
    # Serbest metin: klinikler kendi checklist adımlarını tanımlayabilir
    # (örn. "pre_op_consultation", "surgery_day", "post_op_week_1")
    step_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[JourneyStepStatus] = mapped_column(
        SAEnum(JourneyStepStatus, name="journey_step_status"),
        nullable=False,
        default=JourneyStepStatus.PENDING,
    )
    scheduled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<JourneyStep {self.step_type} ({self.status.value})>"
