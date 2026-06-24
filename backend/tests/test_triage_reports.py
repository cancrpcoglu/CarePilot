"""Ön değerlendirme raporu listeleme ve onay/ret akışı.

Raporlar normalde AI agent tarafından üretilir (Sprint 2); burada DB'ye
doğrudan seed ederek klinik onay akışını test ediyoruz.
"""

import uuid

from httpx import AsyncClient

from app.models.conversation import Conversation, ConversationMode
from app.models.patient import Patient
from app.models.triage_report import TriageReport, TriageReportStatus
from tests.conftest import TestSessionLocal

PASSWORD = "SuperSecret123"


async def _token(client: AsyncClient, email: str) -> str:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": PASSWORD, "full_name": "Yonetici"},
    )
    response = await client.post(
        "/api/v1/auth/login", data={"username": email, "password": PASSWORD}
    )
    return response.json()["access_token"]


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def _seed_triage_report(clinic_id: str) -> str:
    """Verilen kliniğe ait bir hasta + konuşma + bekleyen rapor oluşturur."""
    async with TestSessionLocal() as session:
        patient = Patient(
            clinic_id=uuid.UUID(clinic_id), full_name="Seed Hasta", language="tr"
        )
        session.add(patient)
        await session.flush()

        conversation = Conversation(
            patient_id=patient.id, mode=ConversationMode.TRIAGE
        )
        session.add(conversation)
        await session.flush()

        report = TriageReport(
            patient_id=patient.id,
            conversation_id=conversation.id,
            structured_data={"hair_loss_grade": 4, "expectation": "natural hairline"},
            status=TriageReportStatus.PENDING,
        )
        session.add(report)
        await session.commit()
        return str(report.id)


async def test_list_and_approve_report(client: AsyncClient) -> None:
    token = await _token(client, "triage1@gmail.com")
    clinic = await client.post(
        "/api/v1/clinics", json={"name": "Triage Klinik"}, headers=_headers(token)
    )
    report_id = await _seed_triage_report(clinic.json()["id"])

    listing = await client.get(
        "/api/v1/triage-reports?status=pending", headers=_headers(token)
    )
    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert listing.json()[0]["id"] == report_id

    approved = await client.post(
        f"/api/v1/triage-reports/{report_id}/approve", headers=_headers(token)
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"
    assert approved.json()["reviewed_by"] is not None


async def test_double_review_conflicts(client: AsyncClient) -> None:
    token = await _token(client, "triage2@gmail.com")
    clinic = await client.post(
        "/api/v1/clinics", json={"name": "Triage Klinik 2"}, headers=_headers(token)
    )
    report_id = await _seed_triage_report(clinic.json()["id"])

    first = await client.post(
        f"/api/v1/triage-reports/{report_id}/reject", headers=_headers(token)
    )
    assert first.status_code == 200
    assert first.json()["status"] == "rejected"

    second = await client.post(
        f"/api/v1/triage-reports/{report_id}/approve", headers=_headers(token)
    )
    assert second.status_code == 409


async def test_report_isolation_between_clinics(client: AsyncClient) -> None:
    token_a = await _token(client, "triageA@gmail.com")
    clinic_a = await client.post(
        "/api/v1/clinics", json={"name": "A"}, headers=_headers(token_a)
    )
    report_id = await _seed_triage_report(clinic_a.json()["id"])

    token_b = await _token(client, "triageB@gmail.com")
    await client.post(
        "/api/v1/clinics", json={"name": "B"}, headers=_headers(token_b)
    )

    leaked = await client.get(
        f"/api/v1/triage-reports/{report_id}", headers=_headers(token_b)
    )
    assert leaked.status_code == 404
