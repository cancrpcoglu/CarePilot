"""Self-servis hasta ön kaydı (public intake) şemaları."""

from pydantic import BaseModel, EmailStr, Field


class IntakeInfo(BaseModel):
    clinic_name: str


class IntakeStartRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    # Klinik hastaya ulaşabilsin diye telefon/WhatsApp zorunlu; e-posta opsiyonel.
    phone: str = Field(min_length=5, max_length=32)
    email: EmailStr | None = None
    language: str | None = None


class IntakeStartResponse(BaseModel):
    access_token: str
    patient_name: str
