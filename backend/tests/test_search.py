"""Anlamsal (embedding) rapor arama endpoint wiring testleri.

Gerçek pgvector araması SQLite'ta çalışmaz; embed + repo araması mock'lanır.
Gerçek vektör benzerliği canlı Postgres'e karşı doğrulanır.
"""

from httpx import AsyncClient

from app.repositories.triage_report import TriageReportRepository

PASSWORD = "SuperSecret123"


async def _token(client: AsyncClient, email: str) -> str:
    await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": PASSWORD, "full_name": "Yonetici"},
    )
    login = await client.post(
        "/api/v1/auth/login", data={"username": email, "password": PASSWORD}
    )
    return login.json()["access_token"]


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_search_requires_authentication(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/triage-reports/search", json={"query": "saç ekimi"}
    )
    assert response.status_code == 401


async def test_search_endpoint_wiring(client: AsyncClient, monkeypatch) -> None:
    token = await _token(client, "search1@gmail.com")
    await client.post("/api/v1/clinics", json={"name": "K"}, headers=_headers(token))

    async def fake_embed(query: str) -> list[float]:
        return [0.0] * 3072

    async def fake_search(self, clinic_id, query_vector_literal, limit):
        return []

    monkeypatch.setattr("app.services.triage_report.embed_text", fake_embed)
    monkeypatch.setattr(
        TriageReportRepository, "search_by_similarity", fake_search
    )

    response = await client.post(
        "/api/v1/triage-reports/search",
        json={"query": "diyabetli estetik hastaları"},
        headers=_headers(token),
    )
    assert response.status_code == 200
    assert response.json() == []
