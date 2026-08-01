"""Klinik iş mantığı."""

import uuid

from fastapi import status
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.clinic import Clinic
from app.models.patient import Patient
from app.models.user import User
from app.repositories.clinic import ClinicRepository
from app.schemas.clinic import ClinicCreate, ClinicUpdate


class ClinicService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.clinics = ClinicRepository(session)

    async def create_for_admin(self, admin: User, data: ClinicCreate) -> Clinic:
        """Klinik oluşturur ve oturum açan yöneticiye bağlar."""
        if admin.clinic_id is not None:
            raise AppException(
                "Zaten bir kliniğiniz var.",
                status.HTTP_409_CONFLICT,
            )
        clinic = Clinic(
            name=data.name,
            country=data.country,
            contact_email=data.contact_email,
            contact_phone=data.contact_phone,
        )
        clinic = await self.clinics.create(clinic)
        admin.clinic_id = clinic.id
        self.session.add(admin)
        await self.session.commit()
        await self.session.refresh(clinic)
        return clinic

    async def get(self, clinic_id: uuid.UUID) -> Clinic:
        clinic = await self.clinics.get_by_id(clinic_id)
        if clinic is None:
            raise AppException("Klinik bulunamadı.", status.HTTP_404_NOT_FOUND)
        return clinic

    async def update(self, clinic_id: uuid.UUID, data: ClinicUpdate) -> Clinic:
        clinic = await self.get(clinic_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(clinic, field, value)
        await self.session.commit()
        await self.session.refresh(clinic)
        return clinic

    async def delete(self, clinic_id: uuid.UUID, admin: User) -> None:
        """Kliniği soft-delete eder; bağlı hastaları da soft-delete eder ve
        yöneticinin klinik bağını koparır (yönetici tekrar onboarding'e döner,
        dilerse yeni bir klinik oluşturabilir). Veri DB'de korunur.
        """
        clinic = await self.get(clinic_id)  # yoksa/ait değilse 404
        clinic.is_deleted = True
        # Kliniğe bağlı tüm hastaları da soft-delete et (listelerden kaybolur)
        await self.session.execute(
            update(Patient)
            .where(Patient.clinic_id == clinic_id)
            .values(is_deleted=True)
        )
        # Yöneticinin klinik bağını kopar
        admin.clinic_id = None
        self.session.add(admin)
        await self.session.commit()
