"""Ön değerlendirme raporu endpoint'leri (clinic_admin onay akışı)."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Query

from app.api.deps import ClinicAdmin, CurrentClinicId, DbSession
from app.core import constants
from app.models.triage_report import TriageReportStatus
from app.schemas.triage_report import TriageReportRead
from app.services.triage_report import TriageReportService

router = APIRouter(prefix="/triage-reports", tags=["triage-reports"])


@router.get("", response_model=list[TriageReportRead], summary="Raporları listele")
async def list_reports(
    session: DbSession,
    clinic_id: CurrentClinicId,
    status_filter: Annotated[TriageReportStatus | None, Query(alias="status")] = None,
    limit: Annotated[
        int, Query(ge=1, le=constants.MAX_PAGE_SIZE)
    ] = constants.DEFAULT_PAGE_SIZE,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[TriageReportRead]:
    return await TriageReportService(session).list(
        clinic_id, status_filter, limit, offset
    )


@router.get("/{report_id}", response_model=TriageReportRead, summary="Rapor detayı")
async def get_report(
    report_id: uuid.UUID, session: DbSession, clinic_id: CurrentClinicId
) -> TriageReportRead:
    return await TriageReportService(session).get_scoped(clinic_id, report_id)


@router.post(
    "/{report_id}/approve",
    response_model=TriageReportRead,
    summary="Raporu onayla",
)
async def approve_report(
    report_id: uuid.UUID,
    session: DbSession,
    admin: ClinicAdmin,
    clinic_id: CurrentClinicId,
) -> TriageReportRead:
    return await TriageReportService(session).review(
        clinic_id, report_id, admin.id, TriageReportStatus.APPROVED
    )


@router.post(
    "/{report_id}/reject",
    response_model=TriageReportRead,
    summary="Raporu reddet",
)
async def reject_report(
    report_id: uuid.UUID,
    session: DbSession,
    admin: ClinicAdmin,
    clinic_id: CurrentClinicId,
) -> TriageReportRead:
    return await TriageReportService(session).review(
        clinic_id, report_id, admin.id, TriageReportStatus.REJECTED
    )
