"""Kimlik doğrulama request şemaları."""

from pydantic import BaseModel, EmailStr, Field

from app.core import constants


class RegisterRequest(BaseModel):
    """Klinik hesabı kayıt isteği (MVP: yalnızca klinik yöneticisi kaydı)."""

    email: EmailStr
    password: str = Field(
        min_length=constants.MIN_PASSWORD_LENGTH,
        max_length=constants.MAX_PASSWORD_LENGTH,
    )
    full_name: str | None = None
