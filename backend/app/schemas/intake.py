"""Self-servis hasta ön kaydı (public intake) şemaları."""

from pydantic import BaseModel, EmailStr, Field, field_validator


class IntakeInfo(BaseModel):
    clinic_name: str


class IntakeStartRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    # Klinik hastaya ulaşabilsin diye telefon/WhatsApp zorunlu; e-posta opsiyonel.
    phone: str = Field(min_length=5, max_length=32)
    email: EmailStr | None = None
    language: str | None = None
    # KVKK açık rıza: hasta onaylamadan ön kayıt yapılamaz.
    consent: bool

    @field_validator("consent")
    @classmethod
    def _must_consent(cls, value: bool) -> bool:
        if value is not True:
            raise ValueError("Verilerin işlenmesi için açık rıza gereklidir.")
        return value


class IntakeStartResponse(BaseModel):
    access_token: str
    patient_name: str
