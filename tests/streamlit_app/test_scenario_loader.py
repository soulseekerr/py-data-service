
from datetime import date
from unittest.mock import patch

import pandas as pd
import pytest

from api_client.scenarios import (
    EXPECTED_COLUMNS,
    load_scenarios,
)


VALID_PAYLOAD = [
    {
        "Tier": "Tier 1",
        "Scenario": "Credit Delta Gear",
        "MercuryFile": "CR_SP01.csv",
        "MrxFile": "CREDIT_DELTA_GEAR.DAT",
        "Path": "downstream",
        "FileStatus": "Present",
    }
]


@patch("api_client.scenarios.get_json")
def test_load_scenarios_returns_dataframe(
    mock_get_json,
) -> None:
    mock_get_json.return_value = VALID_PAYLOAD

    result = load_scenarios(
        date(2026, 7, 13)
    )

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == EXPECTED_COLUMNS
    assert len(result) == 1

    mock_get_json.assert_called_once_with(
        "/scenarios",
        params={
            "cob_date": "2026-07-13",
        },
    )


@patch("api_client.scenarios.get_json")
def test_load_scenarios_rejects_non_list_payload(
    mock_get_json,
) -> None:
    mock_get_json.return_value = {
        "data": VALID_PAYLOAD,
    }

    with pytest.raises(
        ValueError,
        match="Unexpected response",
    ):
        load_scenarios(
            date(2026, 7, 13)
        )


@patch("api_client.scenarios.get_json")
def test_load_scenarios_rejects_missing_columns(
    mock_get_json,
) -> None:
    mock_get_json.return_value = [
        {
            "Tier": "Tier 1",
            "Scenario": "Credit Delta Gear",
        }
    ]

    with pytest.raises(
        ValueError,
        match="missing columns",
    ):
        load_scenarios(
            date(2026, 7, 13)
        )