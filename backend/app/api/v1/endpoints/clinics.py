"""Klinik endpoint'leri (yalnızca clinic_admin)."""

from fastapi import APIRouter, status

from app.api.deps import ClinicAdmin, CurrentClinicId, DbSession
from app.schemas.clinic import ClinicCreate, ClinicRead, ClinicUpdate
from app.services.clinic import ClinicService

router = APIRouter(prefix="/clinics", tags=["clinics"])


@router.post(
    "",
    response_model=ClinicRead,
    status_code=status.HTTP_201_CREATED,
    summary="Klinik oluştur (oturum açan yöneticiye bağlanır)",
)
async def create_clinic(
    data: ClinicCreate, session: DbSession, admin: ClinicAdmin
) -> ClinicRead:
    return await ClinicService(session).create_for_admin(admin, data)


@router.get("/me", response_model=ClinicRead, summary="Kendi kliniğim")
async def get_my_clinic(session: DbSession, clinic_id: CurrentClinicId) -> ClinicRead:
    return await ClinicService(session).get(clinic_id)


@router.patch("/me", response_model=ClinicRead, summary="Kendi kliniğimi güncelle")
async def update_my_clinic(
    data: ClinicUpdate, session: DbSession, clinic_id: CurrentClinicId
) -> ClinicRead:
    return await ClinicService(session).update(clinic_id, data)
