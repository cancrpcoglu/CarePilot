"""Hasta veri erişim katmanı."""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient


class PatientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, patient_id: uuid.UUID) -> Patient | None:
        stmt = select(Patient).where(
            Patient.id == patient_id,
            Patient.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_clinic(
        self, clinic_id: uuid.UUID, limit: int, offset: int
    ) -> Sequence[Patient]:
        stmt = (
            select(Patient)
            .where(Patient.clinic_id == clinic_id, Patient.is_deleted.is_(False))
            .order_by(Patient.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, patient: Patient) -> Patient:
        self.session.add(patient)
        await self.session.flush()
        await self.session.refresh(patient)
        return patient
