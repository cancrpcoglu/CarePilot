"""Ön değerlendirme raporu request/response şemaları."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core import constants
from app.models.triage_report import TriageReportStatus


class TriageSearchRequest(BaseModel):
    query: str = Field(min_length=2, max_length=500)
    limit: int = Field(
        default=constants.SEARCH_DEFAULT_LIMIT, ge=1, le=constants.MAX_PAGE_SIZE
    )


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
