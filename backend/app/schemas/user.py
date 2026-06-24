"""Kullanıcı request/response şemaları (Pydantic v2)."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core import constants
from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    password: str = Field(
        min_length=constants.MIN_PASSWORD_LENGTH,
        max_length=constants.MAX_PASSWORD_LENGTH,
    )
    role: UserRole = UserRole.PATIENT


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: UserRole
    is_active: bool
    created_at: datetime
