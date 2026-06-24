"""Ön değerlendirme raporu veri erişim katmanı.

Raporlar hastaya bağlıdır; klinik scope'u hasta üzerinden (join) uygulanır.
"""

import uuid
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patient import Patient
from app.models.triage_report import TriageReport, TriageReportStatus


class TriageReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id_scoped(
        self, clinic_id: uuid.UUID, report_id: uuid.UUID
    ) -> TriageReport | None:
        stmt = (
            select(TriageReport)
            .join(Patient, TriageReport.patient_id == Patient.id)
            .where(
                TriageReport.id == report_id,
                Patient.clinic_id == clinic_id,
                TriageReport.is_deleted.is_(False),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_clinic(
        self,
        clinic_id: uuid.UUID,
        status: TriageReportStatus | None,
        limit: int,
        offset: int,
    ) -> Sequence[TriageReport]:
        stmt = (
            select(TriageReport)
            .join(Patient, TriageReport.patient_id == Patient.id)
            .where(Patient.clinic_id == clinic_id, TriageReport.is_deleted.is_(False))
        )
        if status is not None:
            stmt = stmt.where(TriageReport.status == status)
        stmt = stmt.order_by(TriageReport.created_at.desc()).limit(limit).offset(offset)
        result = await self.session.execute(stmt)
        return result.scalars().all()
