"""Hasta yolculuğu adımı iş mantığı. Adımlar hastanın kliniğine scope'lanır."""

import uuid
from collections.abc import Sequence

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.journey_step import JourneyStep
from app.repositories.journey_step import JourneyStepRepository
from app.repositories.patient import PatientRepository
from app.schemas.journey_step import JourneyStepCreate, JourneyStepUpdate


class JourneyStepService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.steps = JourneyStepRepository(session)
        self.patients = PatientRepository(session)

    async def _ensure_patient_in_clinic(
        self, clinic_id: uuid.UUID, patient_id: uuid.UUID
    ) -> None:
        patient = await self.patients.get_by_id(patient_id)
        if patient is None or patient.clinic_id != clinic_id:
            raise AppException("Hasta bulunamadı.", status.HTTP_404_NOT_FOUND)

    async def list_for_patient(
        self, clinic_id: uuid.UUID, patient_id: uuid.UUID
    ) -> Sequence[JourneyStep]:
        await self._ensure_patient_in_clinic(clinic_id, patient_id)
        return await self.steps.list_by_patient(patient_id)

    async def create(
        self, clinic_id: uuid.UUID, patient_id: uuid.UUID, data: JourneyStepCreate
    ) -> JourneyStep:
        await self._ensure_patient_in_clinic(clinic_id, patient_id)
        step = JourneyStep(
            patient_id=patient_id,
            step_type=data.step_type,
            scheduled_at=data.scheduled_at,
        )
        step = await self.steps.create(step)
        await self.session.commit()
        await self.session.refresh(step)
        return step

    async def update(
        self, clinic_id: uuid.UUID, step_id: uuid.UUID, data: JourneyStepUpdate
    ) -> JourneyStep:
        step = await self.steps.get_by_id(step_id)
        if step is None:
            raise AppException("Adım bulunamadı.", status.HTTP_404_NOT_FOUND)
        await self._ensure_patient_in_clinic(clinic_id, step.patient_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(step, field, value)
        await self.session.commit()
        await self.session.refresh(step)
        return step
