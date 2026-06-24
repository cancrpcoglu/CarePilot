"""Sağlık ve kök endpoint testleri (DB gerektirmez)."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "CarePilot"


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "CarePilot API"
