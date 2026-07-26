
from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_version_returns_version_number() -> None:
    response = client.get("/v1/version")

    assert response.status_code == 200

    payload = response.json()

    assert "version" in payload
    assert isinstance(payload["version"], str)
    assert payload["version"]