"""Public hasta sohbeti (hafızalı agent) testleri.

Gerçek Gemini çağrısı yapılmaz; run_chat_turn mock'lanır. Testler token
erişimini, mesaj kalıcılığını (hafıza), rapor oluşturmayı ve izolasyonu doğrular.
"""

from httpx import AsyncClient

from app.agent.schemas import TreatmentArea, TriageAssessment, TriageTurn

PASSWORD = "SuperSecret123"

FAKE_ASSESSMENT = TriageAssessment(
    detected_language="tr",
    treatment_area=TreatmentArea.HAIR_TRANSPLANT,
    summary="Hasta saç ekimi ile ilgileniyor.",
    primary_concerns=["saç dökülmesi"],
    relevant_medical_history=[],
    missing_information=[],
    recommended_specialty="saç ekimi",
)


async def _clinic_token(client: AsyncClient, email: str) -> str:
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


async def _create_patient(client: AsyncClient, token: str) -> dict:
    await client.post("/api/v1/clinics", json={"name": "Klinik"}, headers=_headers(token))
    response = await client.post(
        "/api/v1/patients",
        json={"full_name": "Omar", "language": "en"},
        headers=_headers(token),
    )
    return response.json()


async def test_invalid_access_token(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/chat/gecersiz-token-123")
    assert response.status_code == 404


async def test_patient_has_access_token(client: AsyncClient) -> None:
    token = await _clinic_token(client, "chat0@gmail.com")
    patient = await _create_patient(client, token)
    assert patient["access_token"]
    assert len(patient["access_token"]) >= 20


async def test_chat_gathering_persists_memory(client: AsyncClient, monkeypatch) -> None:
    async def fake(messages):
        return TriageTurn(
            reply="Merhaba, size nasıl yardımcı olabilirim?",
            is_complete=False,
            assessment=None,
        )

    monkeypatch.setattr("app.services.chat.run_chat_turn", fake)
    token = await _clinic_token(client, "chat1@gmail.com")
    patient = await _create_patient(client, token)
    access = patient["access_token"]

    session = await client.get(f"/api/v1/public/chat/{access}")
    assert session.status_code == 200
    assert session.json()["patient_name"] == "Omar"
    assert session.json()["messages"] == []

    send = await client.post(
        f"/api/v1/public/chat/{access}", json={"message": "Merhaba"}
    )
    assert send.status_code == 201
    assert send.json()["is_complete"] is False
    assert send.json()["report_id"] is None
    assert send.json()["reply"]

    after = await client.get(f"/api/v1/public/chat/{access}")
    messages = after.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "agent"


async def test_chat_memory_accumulates_across_turns(
    client: AsyncClient, monkeypatch
) -> None:
    async def fake(messages):
        # Agent'a geçmiş dahil kaç mesaj geldiğini yansıt (hafıza kanıtı)
        return TriageTurn(
            reply=f"mesaj-sayisi:{len(messages)}", is_complete=False, assessment=None
        )

    monkeypatch.setattr("app.services.chat.run_chat_turn", fake)
    token = await _clinic_token(client, "chat2@gmail.com")
    patient = await _create_patient(client, token)
    access = patient["access_token"]

    await client.post(f"/api/v1/public/chat/{access}", json={"message": "birinci"})
    second = await client.post(
        f"/api/v1/public/chat/{access}", json={"message": "ikinci"}
    )
    # 2. turda: system + (birinci + agent yanıtı) + ikinci = 4 mesaj
    assert "mesaj-sayisi:4" in second.json()["reply"]


async def test_chat_completion_creates_report(
    client: AsyncClient, monkeypatch
) -> None:
    async def fake(messages):
        return TriageTurn(
            reply="Değerlendirmeniz hazır, ekibimiz sizinle iletişime geçecek.",
            is_complete=True,
            assessment=FAKE_ASSESSMENT,
        )

    monkeypatch.setattr("app.services.chat.run_chat_turn", fake)
    token = await _clinic_token(client, "chat3@gmail.com")
    patient = await _create_patient(client, token)
    access = patient["access_token"]

    send = await client.post(
        f"/api/v1/public/chat/{access}", json={"message": "Saç ekimi istiyorum"}
    )
    assert send.status_code == 201
    assert send.json()["is_complete"] is True
    assert send.json()["report_id"] is not None

    # Klinik, agent'ın ürettiği raporu panelinde görebilmeli
    reports = await client.get(
        "/api/v1/triage-reports?status=pending", headers=_headers(token)
    )
    assert len(reports.json()) == 1
    assert reports.json()[0]["structured_data"]["treatment_area"] == "hair_transplant"
