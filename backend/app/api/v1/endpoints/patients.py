"""Hasta endpoint'leri ve hastaya bağlı yolculuk adımları (clinic_admin)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrentClinicId, DbSession
from app.core import constants
from app.schemas.journey_step import JourneyStepCreate, JourneyStepRead
from app.schemas.patient import PatientCreate, PatientRead, PatientUpdate
from app.services.journey_step import JourneyStepService
from app.services.patient import PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post(
    "",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Hasta oluştur",
)
async def create_patient(
    data: PatientCreate, session: DbSession, clinic_id: CurrentClinicId
) -> PatientRead:
    return await PatientService(session).create(clinic_id, data)


@router.get("", response_model=list[PatientRead], summary="Hastaları listele")
async def list_patients(
    session: DbSession,
    clinic_id: CurrentClinicId,
    limit: Annotated[
        int, Query(ge=1, le=constants.MAX_PAGE_SIZE)
    ] = constants.DEFAULT_PAGE_SIZE,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[PatientRead]:
    return await PatientService(session).list(clinic_id, limit, offset)


@router.get("/{patient_id}", response_model=PatientRead, summary="Hasta detayı")
async def get_patient(
    patient_id: uuid.UUID, session: DbSession, clinic_id: CurrentClinicId
) -> PatientRead:
    return await PatientService(session).get_scoped(clinic_id, patient_id)


@router.patch("/{patient_id}", response_model=PatientRead, summary="Hasta güncelle")
async def update_patient(
    patient_id: uuid.UUID,
    data: PatientUpdate,
    session: DbSession,
    clinic_id: CurrentClinicId,
) -> PatientRead:
    return await PatientService(session).update(clinic_id, patient_id, data)


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Hasta sil (soft delete)",
)
async def delete_patient(
    patient_id: uuid.UUID, session: DbSession, clinic_id: CurrentClinicId
) -> None:
    await PatientService(session).delete(clinic_id, patient_id)


@router.get(
    "/{patient_id}/journey",
    response_model=list[JourneyStepRead],
    summary="Hastanın yolculuk adımları",
)
async def list_patient_journey(
    patient_id: uuid.UUID, session: DbSession, clinic_id: CurrentClinicId
) -> list[JourneyStepRead]:
    return await JourneyStepService(session).list_for_patient(clinic_id, patient_id)


@router.post(
    "/{patient_id}/journey",
    response_model=JourneyStepRead,
    status_code=status.HTTP_201_CREATED,
    summary="Hastaya yolculuk adımı ekle",
)
async def create_patient_journey_step(
    patient_id: uuid.UUID,
    data: JourneyStepCreate,
    session: DbSession,
    clinic_id: CurrentClinicId,
) -> JourneyStepRead:
    return await JourneyStepService(session).create(clinic_id, patient_id, data)
