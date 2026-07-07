"""Public hasta sohbeti request/response şemaları."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ChatMessageRead(BaseModel):
    role: str
    content: str
    created_at: datetime


class ChatSessionRead(BaseModel):
    patient_name: str
    language: str
    messages: list[ChatMessageRead]


class ChatSendRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatSendResponse(BaseModel):
    reply: str
    is_complete: bool
    report_id: uuid.UUID | None
