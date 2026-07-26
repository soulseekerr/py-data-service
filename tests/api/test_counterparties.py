
from datetime import date

from fastapi.testclient import TestClient

from api.app import app


client = TestClient(app)


def test_counterparties_requires_cob_date() -> None:
    response = client.get("/v1/counterparties")

    assert response.status_code == 422


def test_counterparties_returns_records() -> None:
    response = client.get(
        "/v1/counterparties",
        params={
            "cob_date": date(2026, 7, 13).isoformat(),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert isinstance(payload, list)
    assert len(payload) > 0

    first_counterparty = payload[0]

    assert set(first_counterparty) == {
        "Counterparty",
        "CVAMethod",
        "Grr",
        "Status",
        "Confidence",
    }


def test_counterparty_numeric_fields_are_numbers() -> None:
    response = client.get(
        "/v1/counterparties",
        params={
            "cob_date": "2026-07-13",
        },
    )

    assert response.status_code == 200

    for counterparty in response.json():
        assert isinstance(counterparty["Grr"], float | int)
        assert isinstance(
            counterparty["Confidence"],
            float | int,
        )

def test_counterparties_rejects_invalid_date() -> None:
    response = client.get(
        "/v1/counterparties",
        params={
            "cob_date": "not-a-date",
        },
    )

    assert response.status_code == 422