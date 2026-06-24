"""Hasta yolculuğu adımı veri erişim katmanı."""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.journey_step import JourneyStep


class JourneyStepRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, step_id: uuid.UUID) -> JourneyStep | None:
        stmt = select(JourneyStep).where(
            JourneyStep.id == step_id,
            JourneyStep.is_deleted.is_(False),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_patient(self, patient_id: uuid.UUID) -> Sequence[JourneyStep]:
        stmt = (
            select(JourneyStep)
            .where(
                JourneyStep.patient_id == patient_id,
                JourneyStep.is_deleted.is_(False),
            )
            .order_by(JourneyStep.created_at.asc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, step: JourneyStep) -> JourneyStep:
        self.session.add(step)
        await self.session.flush()
        await self.session.refresh(step)
        return step
