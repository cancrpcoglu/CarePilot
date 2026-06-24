"""Hasta yolculuğu adımı request/response şemaları."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.journey_step import JourneyStepStatus


class JourneyStepCreate(BaseModel):
    step_type: str
    scheduled_at: datetime | None = None


class JourneyStepUpdate(BaseModel):
    status: JourneyStepStatus | None = None
    scheduled_at: datetime | None = None
    completed_at: datetime | None = None


class JourneyStepRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    patient_id: uuid.UUID
    step_type: str
    status: JourneyStepStatus
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
