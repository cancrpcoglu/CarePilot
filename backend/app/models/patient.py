"""Hasta profili modeli.

user_id nullable'dir: klinik, hastayı sisteme henüz giriş yapmadan önce
(örn. ilk koordinasyon sırasında) profil olarak oluşturabilir; hasta daha
sonra kendi kullanıcı hesabıyla eşleştirilir.
"""

import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, SoftDeleteMixin, TimestampMixin, UUIDMixin


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

    def __repr__(self) -> str:
        return f"<Patient {self.full_name}>"
