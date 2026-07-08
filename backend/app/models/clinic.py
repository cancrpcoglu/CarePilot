"""Klinik modeli (B2B taraf)."""

import secrets

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


def generate_intake_token() -> str:
    """Kliniğin self-servis davet linki için benzersiz token üretir."""
    return secrets.token_urlsafe(16)


class Clinic(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "clinics"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(320), nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # Self-servis hasta ön kaydı için paylaşılabilir tek link token'ı
    intake_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        default=generate_intake_token,
    )

    def __repr__(self) -> str:
        return f"<Clinic {self.name}>"
