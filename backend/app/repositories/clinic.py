"""Klinik veri erişim katmanı."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.clinic import Clinic


class ClinicRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, clinic_id: uuid.UUID) -> Clinic | None:
        stmt = select(Clinic).where(
            Clinic.id == clinic_id,
            Clinic.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, clinic: Clinic) -> Clinic:
        self.session.add(clinic)
        await self.session.flush()
        await self.session.refresh(clinic)
        return clinic
