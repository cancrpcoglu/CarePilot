"""Klinik, hasta ve yolculuk adımı akışları + klinikler arası izolasyon."""

from httpx import AsyncClient

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


async def _create_clinic(client: AsyncClient, token: str, name: str = "Test Klinik") -> dict:
    response = await client.post(
        "/api/v1/clinics", json={"name": name}, headers=_headers(token)
    )
    return response.json()


async def test_create_and_get_clinic(client: AsyncClient) -> None:
    token = await _token(client, "klinik1@gmail.com")
    create = await client.post(
        "/api/v1/clinics",
        json={"name": "Estetik Merkezi", "country": "TR"},
        headers=_headers(token),
    )
    assert create.status_code == 201
    assert create.json()["name"] == "Estetik Merkezi"

    me = await client.get("/api/v1/clinics/me", headers=_headers(token))
    assert me.status_code == 200
    assert me.json()["country"] == "TR"


async def test_second_clinic_creation_conflicts(client: AsyncClient) -> None:
    token = await _token(client, "klinik2@gmail.com")
    await _create_clinic(client, token)
    second = await client.post(
        "/api/v1/clinics", json={"name": "Ikinci"}, headers=_headers(token)
    )
    assert second.status_code == 409


async def test_patients_require_clinic_first(client: AsyncClient) -> None:
    token = await _token(client, "klinik3@gmail.com")
    response = await client.post(
        "/api/v1/patients",
        json={"full_name": "Hasta", "language": "tr"},
        headers=_headers(token),
    )
    assert response.status_code == 409


async def test_patient_crud_and_listing(client: AsyncClient) -> None:
    token = await _token(client, "klinik4@gmail.com")
    await _create_clinic(client, token)

    created = await client.post(
        "/api/v1/patients",
        json={"full_name": "Ahmet Yilmaz", "language": "tr", "country": "DE"},
        headers=_headers(token),
    )
    assert created.status_code == 201
    patient_id = created.json()["id"]

    listing = await client.get("/api/v1/patients", headers=_headers(token))
    assert listing.status_code == 200
    assert len(listing.json()) == 1

    detail = await client.get(
        f"/api/v1/patients/{patient_id}", headers=_headers(token)
    )
    assert detail.status_code == 200
    assert detail.json()["full_name"] == "Ahmet Yilmaz"

    updated = await client.patch(
        f"/api/v1/patients/{patient_id}",
        json={"country": "NL"},
        headers=_headers(token),
    )
    assert updated.status_code == 200
    assert updated.json()["country"] == "NL"


async def test_patient_isolation_between_clinics(client: AsyncClient) -> None:
    token_a = await _token(client, "klinikA@gmail.com")
    await _create_clinic(client, token_a, "Klinik A")
    created = await client.post(
        "/api/v1/patients",
        json={"full_name": "Gizli Hasta"},
        headers=_headers(token_a),
    )
    patient_id = created.json()["id"]

    token_b = await _token(client, "klinikB@gmail.com")
    await _create_clinic(client, token_b, "Klinik B")

    # B klinigi A'nin hastasini gormemeli
    leaked = await client.get(
        f"/api/v1/patients/{patient_id}", headers=_headers(token_b)
    )
    assert leaked.status_code == 404

    b_list = await client.get("/api/v1/patients", headers=_headers(token_b))
    assert b_list.json() == []


async def test_journey_step_flow(client: AsyncClient) -> None:
    token = await _token(client, "klinik5@gmail.com")
    await _create_clinic(client, token)
    patient = await client.post(
        "/api/v1/patients", json={"full_name": "Yolcu Hasta"}, headers=_headers(token)
    )
    patient_id = patient.json()["id"]

    step = await client.post(
        f"/api/v1/patients/{patient_id}/journey",
        json={"step_type": "pre_op_consultation"},
        headers=_headers(token),
    )
    assert step.status_code == 201
    step_id = step.json()["id"]
    assert step.json()["status"] == "pending"

    journey = await client.get(
        f"/api/v1/patients/{patient_id}/journey", headers=_headers(token)
    )
    assert journey.status_code == 200
    assert len(journey.json()) == 1

    completed = await client.patch(
        f"/api/v1/journey-steps/{step_id}",
        json={"status": "completed"},
        headers=_headers(token),
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "completed"


async def test_clinic_endpoints_require_authentication(client: AsyncClient) -> None:
    response = await client.get("/api/v1/clinics/me")
    assert response.status_code == 401


async def test_delete_clinic_soft_deletes_and_detaches(client: AsyncClient) -> None:
    token = await _token(client, "sil1@gmail.com")
    await _create_clinic(client, token, "Silinecek Klinik")
    await client.post(
        "/api/v1/patients", json={"full_name": "Hasta"}, headers=_headers(token)
    )

    # Kliniği sil
    deleted = await client.delete("/api/v1/clinics/me", headers=_headers(token))
    assert deleted.status_code == 204

    # Klinik bağı koptu → /clinics/me artık 409 (yeni klinik gerekir)
    me_clinic = await client.get("/api/v1/clinics/me", headers=_headers(token))
    assert me_clinic.status_code == 409

    # Kullanıcı hâlâ geçerli ama clinic_id null
    me = await client.get("/api/v1/auth/me", headers=_headers(token))
    assert me.status_code == 200
    assert me.json()["clinic_id"] is None

    # Yönetici dilerse yeni bir klinik oluşturabilir (onboarding)
    again = await client.post(
        "/api/v1/clinics", json={"name": "Yeni Klinik"}, headers=_headers(token)
    )
    assert again.status_code == 201
    # Yeni klinik boş: eski hastalar (soft-deleted) taşınmaz
    listing = await client.get("/api/v1/patients", headers=_headers(token))
    assert listing.json() == []


async def test_delete_clinic_does_not_touch_other_clinic(client: AsyncClient) -> None:
    token_a = await _token(client, "silA@gmail.com")
    await _create_clinic(client, token_a, "Klinik A")
    await client.post(
        "/api/v1/patients", json={"full_name": "A Hasta"}, headers=_headers(token_a)
    )

    token_b = await _token(client, "silB@gmail.com")
    await _create_clinic(client, token_b, "Klinik B")
    await client.post(
        "/api/v1/patients", json={"full_name": "B Hasta"}, headers=_headers(token_b)
    )

    # A kliniğini sil
    await client.delete("/api/v1/clinics/me", headers=_headers(token_a))

    # B kliniği ve hastası etkilenmemeli
    b_clinic = await client.get("/api/v1/clinics/me", headers=_headers(token_b))
    assert b_clinic.status_code == 200
    b_list = await client.get("/api/v1/patients", headers=_headers(token_b))
    assert len(b_list.json()) == 1
    assert b_list.json()[0]["full_name"] == "B Hasta"
