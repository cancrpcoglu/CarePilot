"""Gemini 2.5 Flash tabanlı triage çalıştırıcısı (structured output)."""

from fastapi import status
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.prompts.triage import TRIAGE_SYSTEM_PROMPT
from app.agent.schemas import TriageAssessment
from app.core import constants
from app.core.config import settings
from app.core.exceptions import AppException


def _build_structured_llm():
    """Gemini modelini structured output (function calling) ile hazırlar."""
    llm = ChatGoogleGenerativeAI(
        model=constants.GEMINI_MODEL,
        temperature=constants.TRIAGE_TEMPERATURE,
        api_key=settings.GEMINI_API_KEY,
    )
    return llm.with_structured_output(TriageAssessment)


async def run_triage(message: str, language: str | None) -> TriageAssessment:
    """Hasta mesajını Gemini'ye verir ve yapılandırılmış değerlendirme döner."""
    if not settings.GEMINI_API_KEY:
        raise AppException(
            "Yapay zeka servisi şu an yapılandırılmamış.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    language_hint = (
        f"Hastanın tercih ettiği dil: {language}.\n" if language else ""
    )
    messages = [
        SystemMessage(content=TRIAGE_SYSTEM_PROMPT),
        HumanMessage(content=f"{language_hint}Hasta mesajı:\n{message}"),
    ]

    structured_llm = _build_structured_llm()
    result = await structured_llm.ainvoke(messages)
    return result  # type: ignore[return-value]
