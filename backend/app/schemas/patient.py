"""Hasta request/response şemaları."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PatientBase(BaseModel):
    full_name: str
    language: str = "en"
    country: str | None = None


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    full_name: str | None = None
    language: str | None = None
    country: str | None = None
    notes: str | None = None


class PatientRead(PatientBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    clinic_id: uuid.UUID
    user_id: uuid.UUID | None
    access_token: str
    notes: str | None
    created_at: datetime
