"""Self-servis hasta ön kaydı (public intake) şemaları."""

from pydantic import BaseModel, Field


class IntakeInfo(BaseModel):
    clinic_name: str


class IntakeStartRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    language: str | None = None


class IntakeStartResponse(BaseModel):
    access_token: str
    patient_name: str
