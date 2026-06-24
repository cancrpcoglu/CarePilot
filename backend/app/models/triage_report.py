"""Agent'ın ürettiği yapılandırılmış ön değerlendirme raporu modeli."""

import enum
import uuid

from sqlalchemy import JSON, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class TriageReportStatus(str, enum.Enum):
    """Klinik onay durumu."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class TriageReport(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "triage_reports"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("patients.id"), nullable=False, index=True
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("conversations.id"), nullable=False, index=True
    )
    # Agent'ın structured output ile ürettiği ön değerlendirme verisi
    structured_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[TriageReportStatus] = mapped_column(
        SAEnum(TriageReportStatus, name="triage_report_status"),
        nullable=False,
        default=TriageReportStatus.PENDING,
    )
    reviewed_by: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    def __repr__(self) -> str:
        return f"<TriageReport {self.id} ({self.status.value})>"
