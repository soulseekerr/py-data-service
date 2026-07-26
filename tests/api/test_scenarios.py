
from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


EXPECTED_FIELDS = {
    "Tier",
    "Scenario",
    "MercuryFile",
    "MrxFile",
    "Path",
    "IsFilePresent",
}


def test_scenarios_requires_cob_date() -> None:
    response = client.get("/v1/scenarios")

    assert response.status_code == 422


def test_scenarios_returns_expected_schema() -> None:
    response = client.get(
        "/v1/scenarios",
        params={
            "cob_date": "2026-07-13",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, list)
    assert payload

    for scenario in payload:
        assert set(scenario) == EXPECTED_FIELDS


def test_scenario_file_presence_has_known_value() -> None:
    response = client.get(
        "/v1/scenarios",
        params={
            "cob_date": "2026-07-13",
        },
    )

    assert response.status_code == 200

    for scenario in response.json():
        assert scenario["IsFilePresent"] in {
            "Yes",
            "No",
        }