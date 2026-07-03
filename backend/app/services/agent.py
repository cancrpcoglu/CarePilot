"""Triage agent orkestrasyonu.

Hasta mesajını Gemini'ye verir, çıkan yapılandırılmış değerlendirmeyi
konuşma + mesajlar + bekleyen bir triage raporu olarak kalıcılaştırır.
Böylece klinik paneli AI'ın ürettiği raporları görüp onaylayabilir.
"""

import uuid

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent import triage as triage_runner
from app.agent.schemas import TriageAssessment
from app.core.exceptions import AppException
from app.models.conversation import Conversation, ConversationMode
from app.models.message import Message, MessageRole
from app.models.triage_report import TriageReport, TriageReportStatus
from app.repositories.patient import PatientRepository


class TriageAgentService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.patients = PatientRepository(session)

    async def run_for_patient(
        self,
        clinic_id: uuid.UUID,
        patient_id: uuid.UUID,
        message: str,
        language: str | None,
    ) -> tuple[TriageReport, Conversation, TriageAssessment]:
        patient = await self.patients.get_by_id(patient_id)
        if patient is None or patient.clinic_id != clinic_id:
            raise AppException("Hasta bulunamadı.", status.HTTP_404_NOT_FOUND)

        assessment = await triage_runner.run_triage(
            message, language or patient.language
        )

        conversation = Conversation(
            patient_id=patient_id, mode=ConversationMode.TRIAGE
        )
        self.session.add(conversation)
        await self.session.flush()

        self.session.add(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=message,
            )
        )
        self.session.add(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.AGENT,
                content=assessment.summary,
            )
        )

        report = TriageReport(
            patient_id=patient_id,
            conversation_id=conversation.id,
            structured_data=assessment.model_dump(mode="json"),
            status=TriageReportStatus.PENDING,
        )
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report, conversation, assessment
