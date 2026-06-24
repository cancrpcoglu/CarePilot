"""Kullanıcı modeli — klinik yöneticisi veya hasta."""

import enum

from sqlalchemy import Boolean, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


class UserRole(str, enum.Enum):
    """Sistemdeki kullanıcı rolleri."""

    CLINIC_ADMIN = "clinic_admin"
    PATIENT = "patient"


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, name="user_role"),
        nullable=False,
        default=UserRole.PATIENT,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role.value})>"
