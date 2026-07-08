"""Hasta profili modeli.

user_id nullable'dir: klinik, hastayı sisteme henüz giriş yapmadan önce
(örn. ilk koordinasyon sırasında) profil olarak oluşturabilir; hasta daha
sonra kendi kullanıcı hesabıyla eşleştirilir.
"""

import secrets
import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


def generate_access_token() -> str:
    """Hastanın chat linkine erişimi için tahmin edilemez token üretir."""
    return secrets.token_urlsafe(24)


class Patient(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "patients"

    clinic_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("clinics.id"), nullable=False, index=True
    )
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    # Hastanın kimlik doğrulaması olmadan chat'e eriştiği benzersiz token
    access_token: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
        default=generate_access_token,
    )
    # Kliniğe özel serbest not (hasta göremez)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Patient {self.full_name}>"
