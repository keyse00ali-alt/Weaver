from fastapi.testclient import TestClient

from main import app


def test_health_ok() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "healthy"}


def test_get_household_creates_default_household() -> None:
    client = TestClient(app)
    resp = client.get("/households/test_household_default")
    assert resp.status_code == 200

    data = resp.json()
    assert data["id"] == "test_household_default"
    assert data["household_type"] == "grid_only"
    assert isinstance(data["bidding_zone"], str)

