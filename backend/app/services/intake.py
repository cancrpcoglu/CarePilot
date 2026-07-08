"""Self-servis hasta ön kaydı orkestrasyonu.

Klinik tek bir davet token'ı paylaşır; yeni hasta bu token ile kendi kaydını
oluşturur ve chat için bir access_token alır. Klinik önceden hasta oluşturmaz.
"""

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.clinic import Clinic
from app.models.patient import Patient


class IntakeService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_clinic(self, intake_token: str) -> Clinic:
        stmt = select(Clinic).where(
            Clinic.intake_token == intake_token,
            Clinic.is_deleted.is_(False),
        )
        clinic = (await self.session.execute(stmt)).scalar_one_or_none()
        if clinic is None:
            raise AppException(
                "Geçersiz davet bağlantısı.", status.HTTP_404_NOT_FOUND
            )
        return clinic

    async def get_info(self, intake_token: str) -> Clinic:
        return await self._get_clinic(intake_token)

    async def start(
        self, intake_token: str, full_name: str, language: str | None
    ) -> Patient:
        clinic = await self._get_clinic(intake_token)
        patient = Patient(
            clinic_id=clinic.id,
            full_name=full_name,
            language=language or "en",
        )
        self.session.add(patient)
        await self.session.flush()
        await self.session.refresh(patient)
        await self.session.commit()
        return patient
