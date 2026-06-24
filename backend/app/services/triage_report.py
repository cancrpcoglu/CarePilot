"""Ön değerlendirme raporu iş mantığı (klinik onay akışı)."""

import uuid
from collections.abc import Sequence

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.models.triage_report import TriageReport, TriageReportStatus
from app.repositories.triage_report import TriageReportRepository


class TriageReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.reports = TriageReportRepository(session)

    async def list(
        self,
        clinic_id: uuid.UUID,
        status_filter: TriageReportStatus | None,
        limit: int,
        offset: int,
    ) -> Sequence[TriageReport]:
        return await self.reports.list_by_clinic(
            clinic_id, status_filter, limit, offset
        )

    async def get_scoped(
        self, clinic_id: uuid.UUID, report_id: uuid.UUID
    ) -> TriageReport:
        report = await self.reports.get_by_id_scoped(clinic_id, report_id)
        if report is None:
            raise AppException("Rapor bulunamadı.", status.HTTP_404_NOT_FOUND)
        return report

    async def review(
        self,
        clinic_id: uuid.UUID,
        report_id: uuid.UUID,
        reviewer_id: uuid.UUID,
        new_status: TriageReportStatus,
    ) -> TriageReport:
        """Raporu onaylar veya reddeder (yalnızca bekleyen raporlar)."""
        report = await self.get_scoped(clinic_id, report_id)
        if report.status != TriageReportStatus.PENDING:
            raise AppException(
                "Bu rapor zaten değerlendirilmiş.",
                status.HTTP_409_CONFLICT,
            )
        report.status = new_status
        report.reviewed_by = reviewer_id
        await self.session.commit()
        await self.session.refresh(report)
        return report
