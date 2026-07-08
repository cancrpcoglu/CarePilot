"""Klinik request/response şemaları."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class ClinicBase(BaseModel):
    name: str
    country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None


class ClinicCreate(ClinicBase):
    pass


class ClinicUpdate(BaseModel):
    name: str | None = None
    country: str | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None


class ClinicRead(ClinicBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    intake_token: str
    created_at: datetime
