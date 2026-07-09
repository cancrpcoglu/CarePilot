"""Self-servis hasta ön kaydı endpoint'leri (public, token tabanlı)."""

from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.schemas.intake import IntakeInfo, IntakeStartRequest, IntakeStartResponse
from app.services.intake import IntakeService

router = APIRouter(prefix="/public/intake", tags=["public-intake"])


@router.get("/{intake_token}", response_model=IntakeInfo)
async def get_intake_info(intake_token: str, session: DbSession) -> IntakeInfo:
    clinic = await IntakeService(session).get_info(intake_token)
    return IntakeInfo(clinic_name=clinic.name)


@router.post(
    "/{intake_token}",
    response_model=IntakeStartResponse,
    status_code=status.HTTP_201_CREATED,
)
async def start_intake(
    intake_token: str, data: IntakeStartRequest, session: DbSession
) -> IntakeStartResponse:
    patient = await IntakeService(session).start(
        intake_token, data.full_name, data.language
    )
    return IntakeStartResponse(
        access_token=patient.access_token, patient_name=patient.full_name
    )
