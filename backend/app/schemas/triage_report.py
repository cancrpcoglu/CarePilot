"""Ön değerlendirme raporu response şeması."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.triage_report import TriageReportStatus


class TriageReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    conversation_id: uuid.UUID
    structured_data: dict
    status: TriageReportStatus
    reviewed_by: uuid.UUID | None
    created_at: datetime
    updated_at: datetime
