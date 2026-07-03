"""Triage agent endpoint request/response şemaları."""

import uuid

from pydantic import BaseModel, Field

from app.agent.schemas import TriageAssessment


class TriageRequest(BaseModel):
    patient_id: uuid.UUID
    message: str = Field(min_length=1, max_length=5000)
    language: str | None = None


class TriageAgentResponse(BaseModel):
    report_id: uuid.UUID
    conversation_id: uuid.UUID
    assessment: TriageAssessment
