"""Gemini text-embedding-004 ile metin embedding üretimi (anlamsal arama için)."""

from fastapi import status
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.agent.schemas import TriageAssessment
from app.core import constants
from app.core.config import settings
from app.core.exceptions import AppException


def _build_embedder() -> GoogleGenerativeAIEmbeddings:
    return GoogleGenerativeAIEmbeddings(
        model=constants.EMBEDDING_MODEL,
        google_api_key=settings.GEMINI_API_KEY,
    )


async def embed_text(text: str) -> list[float]:
    """Bir metni 768 boyutlu vektöre çevirir."""
    if not settings.GEMINI_API_KEY:
        raise AppException(
            "Yapay zeka servisi şu an yapılandırılmamış.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    embedder = _build_embedder()
    return await embedder.aembed_query(text)


def assessment_to_text(assessment: TriageAssessment) -> str:
    """Bir ön değerlendirmeyi embedding için düz metne dönüştürür."""
    parts = [
        f"Tedavi alanı: {assessment.treatment_area.value}",
        f"Özet: {assessment.summary}",
    ]
    if assessment.primary_concerns:
        parts.append("Şikayetler: " + ", ".join(assessment.primary_concerns))
    if assessment.patient_expectations:
        parts.append(f"Beklenti: {assessment.patient_expectations}")
    if assessment.relevant_medical_history:
        parts.append(
            "Sağlık geçmişi: " + ", ".join(assessment.relevant_medical_history)
        )
    if assessment.recommended_specialty:
        parts.append(f"Önerilen uzmanlık: {assessment.recommended_specialty}")
    return "\n".join(parts)


def format_vector_literal(vector: list[float]) -> str:
    """Vektörü pgvector'ın kabul ettiği '[1,2,3]' string biçimine getirir."""
    return "[" + ",".join(str(x) for x in vector) + "]"
