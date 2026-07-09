"""Self-servis intake + hasta CRUD (not/silme) testleri."""

from httpx import AsyncClient

PASSWORD = "SuperSecret123"


async def _clinic(client: AsyncClient, email: str) -> tuple[str, dict]:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": PASSWORD, "full_name": "Yonetici"},
    )
    login = await client.post(
        "/api/v1/auth/login", data={"username": email, "password": PASSWORD}
    )
    token = login.json()["access_token"]
    clinic = await client.post(
        "/api/v1/clinics", json={"name": "Klinik"}, headers=_headers(token)
    )
    return token, clinic.json()


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_clinic_read_has_intake_token(client: AsyncClient) -> None:
    _, clinic = await _clinic(client, "crud0@gmail.com")
    assert clinic["intake_token"]


async def test_patient_soft_delete(client: AsyncClient) -> None:
    token, _ = await _clinic(client, "crud1@gmail.com")
    created = await client.post(
        "/api/v1/patients", json={"full_name": "Silinecek"}, headers=_headers(token)
    )
    patient_id = created.json()["id"]

    deleted = await client.delete(
        f"/api/v1/patients/{patient_id}", headers=_headers(token)
    )
    assert deleted.status_code == 204

    listing = await client.get("/api/v1/patients", headers=_headers(token))
    assert listing.json() == []
    detail = await client.get(
        f"/api/v1/patients/{patient_id}", headers=_headers(token)
    )
    assert detail.status_code == 404


async def test_patient_notes_update(client: AsyncClient) -> None:
    token, _ = await _clinic(client, "crud2@gmail.com")
    created = await client.post(
        "/api/v1/patients", json={"full_name": "Notlu"}, headers=_headers(token)
    )
    patient_id = created.json()["id"]

    updated = await client.patch(
        f"/api/v1/patients/{patient_id}",
        json={"notes": "VIP hasta, sabah aranacak", "country": "DE"},
        headers=_headers(token),
    )
    assert updated.status_code == 200
    assert updated.json()["notes"] == "VIP hasta, sabah aranacak"
    assert updated.json()["country"] == "DE"


async def test_self_service_intake_creates_patient(client: AsyncClient) -> None:
    token, clinic = await _clinic(client, "crud3@gmail.com")
    intake_token = clinic["intake_token"]

    info = await client.get(f"/api/v1/public/intake/{intake_token}")
    assert info.status_code == 200
    assert info.json()["clinic_name"] == "Klinik"

    start = await client.post(
        f"/api/v1/public/intake/{intake_token}",
        json={"full_name": "Self Servis Hasta", "language": "en"},
    )
    assert start.status_code == 201
    access_token = start.json()["access_token"]
    assert access_token

    # Klinik, self-kaydolan hastayı panelinde görür
    listing = await client.get("/api/v1/patients", headers=_headers(token))
    assert any(p["full_name"] == "Self Servis Hasta" for p in listing.json())

    # access_token ile chat oturumu açılabilir
    session = await client.get(f"/api/v1/public/chat/{access_token}")
    assert session.status_code == 200
    assert session.json()["patient_name"] == "Self Servis Hasta"


async def test_intake_invalid_token(client: AsyncClient) -> None:
    response = await client.get("/api/v1/public/intake/gecersiz-token")
    assert response.status_code == 404
