"""Public hasta sohbeti orkestrasyonu.

Token tabanlı erişim (kimlik doğrulama yok). Konuşma hafızası messages
tablosundan yüklenir, LangGraph agent'ı çalıştırılır, hasta + agent mesajları
kalıcılaştırılır. Agent yeterli bilgi topladığında klinik onayına bir triage
raporu (pending) oluşturur/günceller.
"""

import uuid

from fastapi import status
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import run_chat_turn
from app.agent.prompts.chat import TRIAGE_CHAT_SYSTEM_PROMPT
from app.agent.schemas import TriageTurn
from app.core.exceptions import AppException
from app.models.conversation import Conversation, ConversationMode
from app.models.message import Message, MessageRole
from app.models.patient import Patient
from app.models.triage_report import TriageReport, TriageReportStatus
from app.services.report_embedding import store_report_embedding


class PublicChatService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_patient(self, access_token: str) -> Patient:
        stmt = select(Patient).where(
            Patient.access_token == access_token,
            Patient.is_deleted.is_(False),
        )
        patient = (await self.session.execute(stmt)).scalar_one_or_none()
        if patient is None:
            raise AppException(
                "Geçersiz erişim bağlantısı.", status.HTTP_404_NOT_FOUND
            )
        return patient

    async def _find_conversation(self, patient_id: uuid.UUID) -> Conversation | None:
        stmt = (
            select(Conversation)
            .where(
                Conversation.patient_id == patient_id,
                Conversation.mode == ConversationMode.TRIAGE,
                Conversation.is_deleted.is_(False),
            )
            .order_by(Conversation.created_at.asc())
        )
        return (await self.session.execute(stmt)).scalars().first()

    async def _load_messages(self, conversation_id: uuid.UUID) -> list[Message]:
        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.is_deleted.is_(False),
            )
            .order_by(Message.created_at.asc())
        )
        return list((await self.session.execute(stmt)).scalars().all())

    def _system_prompt(self, patient: Patient) -> str:
        return (
            f"{TRIAGE_CHAT_SYSTEM_PROMPT}\n\n"
            f"Hasta adı: {patient.full_name}. "
            f"Tercih edilen dil kodu: {patient.language}."
        )

    async def get_session(
        self, access_token: str
    ) -> tuple[Patient, list[Message]]:
        patient = await self._get_patient(access_token)
        conversation = await self._find_conversation(patient.id)
        messages = (
            await self._load_messages(conversation.id) if conversation else []
        )
        return patient, messages

    async def send_message(
        self, access_token: str, text: str
    ) -> tuple[TriageTurn, uuid.UUID | None]:
        patient = await self._get_patient(access_token)
        conversation = await self._find_conversation(patient.id)
        if conversation is None:
            conversation = Conversation(
                patient_id=patient.id, mode=ConversationMode.TRIAGE
            )
            self.session.add(conversation)
            await self.session.flush()

        history = await self._load_messages(conversation.id)

        lc_messages = [SystemMessage(content=self._system_prompt(patient))]
        for message in history:
            if message.role == MessageRole.USER:
                lc_messages.append(HumanMessage(content=message.content))
            else:
                lc_messages.append(AIMessage(content=message.content))
        lc_messages.append(HumanMessage(content=text))

        turn = await run_chat_turn(lc_messages)

        self.session.add(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=text,
            )
        )
        self.session.add(
            Message(
                conversation_id=conversation.id,
                role=MessageRole.AGENT,
                content=turn.reply,
            )
        )

        report_id: uuid.UUID | None = None
        if turn.is_complete and turn.assessment is not None:
            report = await self._existing_report(patient.id, conversation.id)
            payload = turn.assessment.model_dump(mode="json")
            if report is None:
                report = TriageReport(
                    patient_id=patient.id,
                    conversation_id=conversation.id,
                    structured_data=payload,
                    status=TriageReportStatus.PENDING,
                )
                self.session.add(report)
                await self.session.flush()
            else:
                report.structured_data = payload
            report_id = report.id

        await self.session.commit()

        # Yeni/güncellenen rapor için embedding üret (best-effort)
        if report_id is not None and turn.assessment is not None:
            await store_report_embedding(self.session, report_id, turn.assessment)

        return turn, report_id

    async def _existing_report(
        self, patient_id: uuid.UUID, conversation_id: uuid.UUID
    ) -> TriageReport | None:
        stmt = select(TriageReport).where(
            TriageReport.patient_id == patient_id,
            TriageReport.conversation_id == conversation_id,
            TriageReport.is_deleted.is_(False),
        )
        return (await self.session.execute(stmt)).scalar_one_or_none()
