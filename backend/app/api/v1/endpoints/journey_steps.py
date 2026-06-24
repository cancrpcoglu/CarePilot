"""Yolculuk adımı güncelleme endpoint'i (clinic_admin)."""

import uuid

from fastapi import APIRouter

from app.api.deps import CurrentClinicId, DbSession
from app.schemas.journey_step import JourneyStepRead, JourneyStepUpdate
from app.services.journey_step import JourneyStepService

router = APIRouter(prefix="/journey-steps", tags=["journey"])


@router.patch("/{step_id}", response_model=JourneyStepRead, summary="Adımı güncelle")
async def update_journey_step(
    step_id: uuid.UUID,
    data: JourneyStepUpdate,
    session: DbSession,
    clinic_id: CurrentClinicId,
) -> JourneyStepRead:
    return await JourneyStepService(session).update(clinic_id, step_id, data)
