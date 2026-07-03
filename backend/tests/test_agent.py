"""Triage agent endpoint testleri.

Gerçek Gemini çağrısı yapılmaz; run_triage mock'lanır (deterministik, ücretsiz).
Testler agent'ın rapor/konuşma kalıcılaştırma ve scope davranışını doğrular.
"""

import pytest
from httpx import AsyncClient

from app.agent.schemas import TreatmentArea, TriageAssessment

PASSWORD = "SuperSecret123"

FAKE_ASSESSMENT = TriageAssessment(
    detected_language="tr",
    treatment_area=TreatmentArea.HAIR_TRANSPLANT,
    summary="Hasta saç dökülmesi nedeniyle saç ekimi ile ilgileniyor.",
    primary_concerns=["saç dökülmesi", "saç ekimi talebi"],
    patient_expectations="Doğal görünümlü saç çizgisi",
    relevant_medical_history=[],
    missing_information=["Yaş", "Kronik hastalık öyküsü"],
    recommended_specialty="saç ekimi",
)


async def _fake_run_triage(message: str, language: str | None) -> TriageAssessment:
    return FAKE_ASSESSMENT


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


async def _setup_patient(client: AsyncClient, token: str) -> str:
    await client.post(
        "/api/v1/clinics", json={"name": "AI Klinik"}, headers=_headers(token)
    )
    patient = await client.post(
        "/api/v1/patients",
        json={"full_name": "John Smith", "language": "en"},
        headers=_headers(token),
    )
    return patient.json()["id"]


@pytest.fixture(autouse=True)
def _mock_gemini(monkeypatch):
    monkeypatch.setattr("app.agent.triage.run_triage", _fake_run_triage)


async def test_triage_creates_pending_report(client: AsyncClient) -> None:
    token = await _token(client, "agent1@gmail.com")
    patient_id = await _setup_patient(client, token)

    response = await client.post(
        "/api/v1/agent/triage",
        json={"patient_id": patient_id, "message": "Saçlarım dökülüyor, yardım eder misiniz?"},
        headers=_headers(token),
    )
    assert response.status_code == 201
    body = response.json()
    assert body["assessment"]["treatment_area"] == "hair_transplant"
    assert body["assessment"]["detected_language"] == "tr"
    assert "report_id" in body

    # Agent'ın ürettiği rapor klinik panelinde bekleyen olarak görünmeli
    listing = await client.get(
        "/api/v1/triage-reports?status=pending", headers=_headers(token)
    )
    assert len(listing.json()) == 1
    assert listing.json()[0]["id"] == body["report_id"]

    # Ve onaylanabilmeli
    approved = await client.post(
        f"/api/v1/triage-reports/{body['report_id']}/approve",
        headers=_headers(token),
    )
    assert approved.status_code == 200
    assert approved.json()["status"] == "approved"


async def test_triage_requires_authentication(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/agent/triage",
        json={"patient_id": "00000000-0000-0000-0000-000000000000", "message": "x"},
    )
    assert response.status_code == 401


async def test_triage_rejects_other_clinic_patient(client: AsyncClient) -> None:
    token_a = await _token(client, "agentA@gmail.com")
    patient_id = await _setup_patient(client, token_a)

    token_b = await _token(client, "agentB@gmail.com")
    await client.post(
        "/api/v1/clinics", json={"name": "B"}, headers=_headers(token_b)
    )

    response = await client.post(
        "/api/v1/agent/triage",
        json={"patient_id": patient_id, "message": "test"},
        headers=_headers(token_b),
    )
    assert response.status_code == 404
