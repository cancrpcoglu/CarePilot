"""Hasta iş mantığı. Tüm işlemler oturum açan kliniğe scope'lanır."""

import uuid
from collections.abc import Sequence

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.patient import Patient
from app.repositories.patient import PatientRepository
from app.schemas.patient import PatientCreate, PatientUpdate


class PatientService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.patients = PatientRepository(session)

    async def create(self, clinic_id: uuid.UUID, data: PatientCreate) -> Patient:
        patient = Patient(
            clinic_id=clinic_id,
            full_name=data.full_name,
            language=data.language,
            country=data.country,
        )
        patient = await self.patients.create(patient)
        await self.session.commit()
        await self.session.refresh(patient)
        return patient

    async def list(
        self, clinic_id: uuid.UUID, limit: int, offset: int
    ) -> Sequence[Patient]:
        return await self.patients.list_by_clinic(clinic_id, limit, offset)

    async def get_scoped(self, clinic_id: uuid.UUID, patient_id: uuid.UUID) -> Patient:
        """Hastayı getirir; başka kliniğe aitse 404 (bilgi sızdırmaz)."""
        patient = await self.patients.get_by_id(patient_id)
        if patient is None or patient.clinic_id != clinic_id:
            raise AppException("Hasta bulunamadı.", status.HTTP_404_NOT_FOUND)
        return patient

    async def update(
        self, clinic_id: uuid.UUID, patient_id: uuid.UUID, data: PatientUpdate
    ) -> Patient:
        patient = await self.get_scoped(clinic_id, patient_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(patient, field, value)
        await self.session.commit()
        await self.session.refresh(patient)
        return patient
