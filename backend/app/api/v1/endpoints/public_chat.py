"""Public hasta sohbeti endpoint'leri (token tabanlı, kimlik doğrulama yok)."""

from fastapi import APIRouter, status

from app.api.deps import DbSession
from app.schemas.chat import (
    ChatMessageRead,
    ChatSendRequest,
    ChatSendResponse,
    ChatSessionRead,
)
from app.services.chat import PublicChatService

router = APIRouter(prefix="/public/chat", tags=["public-chat"])


@router.get("/{access_token}", response_model=ChatSessionRead)
async def get_chat_session(access_token: str, session: DbSession) -> ChatSessionRead:
    service = PublicChatService(session)
    patient, messages = await service.get_session(access_token)
    return ChatSessionRead(
        patient_name=patient.full_name,
        language=patient.language,
        messages=[
            ChatMessageRead(
                role=message.role.value,
                content=message.content,
                created_at=message.created_at,
            )
            for message in messages
        ],
    )


@router.post(
    "/{access_token}",
    response_model=ChatSendResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_chat_message(
    access_token: str, data: ChatSendRequest, session: DbSession
) -> ChatSendResponse:
    service = PublicChatService(session)
    turn, report_id = await service.send_message(access_token, data.message)
    return ChatSendResponse(
        reply=turn.reply,
        is_complete=turn.is_complete,
        report_id=report_id,
    )
