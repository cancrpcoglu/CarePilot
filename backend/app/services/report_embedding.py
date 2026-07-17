"""Ön değerlendirme raporlarını embedding'leyip pgvector kolonuna yazar.

Embedding en iyi çaba (best-effort) ile yapılır: bir hata olursa rapor
oluşturma akışını bloklamaz, yalnızca arama sonuçlarında çıkmaz.
"""

import logging
import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.embeddings import (
    assessment_to_text,
    embed_text,
    format_vector_literal,
)
from app.agent.schemas import TriageAssessment
from app.core.config import settings

logger = logging.getLogger("carepilot")


async def store_report_embedding(
    session: AsyncSession,
    report_id: uuid.UUID,
    assessment: TriageAssessment,
) -> None:
    if not settings.GEMINI_API_KEY:
        return
    try:
        vector = await embed_text(assessment_to_text(assessment))
        await session.execute(
            text(
                "UPDATE triage_reports SET embedding = CAST(:emb AS vector) "
                "WHERE id = :rid"
            ),
            {"emb": format_vector_literal(vector), "rid": str(report_id)},
        )
        await session.commit()
    except Exception as exc:
        logger.warning("Rapor embedding üretilemedi (%s): %s", report_id, exc)
