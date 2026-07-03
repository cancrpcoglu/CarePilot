"""AI agent endpoint'leri (clinic_admin)."""

from fastapi import APIRouter, status

from app.api.deps import CurrentClinicId, DbSession
from app.schemas.agent import TriageAgentResponse, TriageRequest
from app.services.agent import TriageAgentService

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post(
    "/triage",
    response_model=TriageAgentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Hasta mesajından AI ön değerlendirme üretir ve rapor oluşturur",
)
async def run_triage(
    data: TriageRequest, session: DbSession, clinic_id: CurrentClinicId
) -> TriageAgentResponse:
    service = TriageAgentService(session)
    report, conversation, assessment = await service.run_for_patient(
        clinic_id, data.patient_id, data.message, data.language
    )
    return TriageAgentResponse(
        report_id=report.id,
        conversation_id=conversation.id,
        assessment=assessment,
    )
