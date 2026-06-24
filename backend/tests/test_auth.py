"""Kayıt, giriş ve yetkilendirme testleri."""

from httpx import AsyncClient

REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
ME_URL = "/api/v1/auth/me"

VALID_PAYLOAD = {
    "email": "klinik@example.com",
    "password": "SuperSecret123",
    "full_name": "Test Kliniği",
}


async def _register(client: AsyncClient, **overrides) -> object:
    payload = {**VALID_PAYLOAD, **overrides}
    return await client.post(REGISTER_URL, json=payload)


async def _login(client: AsyncClient, email: str, password: str) -> object:
    return await client.post(LOGIN_URL, data={"username": email, "password": password})


async def test_register_creates_clinic_admin(client: AsyncClient) -> None:
    response = await _register(client)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == VALID_PAYLOAD["email"]
    assert body["role"] == "clinic_admin"
    assert body["is_active"] is True
    assert "id" in body
    # Parola hiçbir zaman dönmemeli
    assert "password" not in body
    assert "hashed_password" not in body


async def test_register_duplicate_email_conflict(client: AsyncClient) -> None:
    await _register(client)
    response = await _register(client)
    assert response.status_code == 409


async def test_register_short_password_validation(client: AsyncClient) -> None:
    response = await _register(client, password="123")
    assert response.status_code == 422


async def test_login_returns_token(client: AsyncClient) -> None:
    await _register(client)
    response = await _login(
        client, VALID_PAYLOAD["email"], VALID_PAYLOAD["password"]
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


async def test_login_wrong_password(client: AsyncClient) -> None:
    await _register(client)
    response = await _login(client, VALID_PAYLOAD["email"], "WrongPassword1")
    assert response.status_code == 401


async def test_me_requires_authentication(client: AsyncClient) -> None:
    response = await client.get(ME_URL)
    assert response.status_code == 401


async def test_me_returns_current_user(client: AsyncClient) -> None:
    await _register(client)
    login_response = await _login(
        client, VALID_PAYLOAD["email"], VALID_PAYLOAD["password"]
    )
    token = login_response.json()["access_token"]

    response = await client.get(ME_URL, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == VALID_PAYLOAD["email"]
    assert body["role"] == "clinic_admin"
