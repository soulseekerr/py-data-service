
import os
from datetime import date
import pandas as pd

from .client import get_json

EXPECTED_COLUMNS = [
    "Tier",
    "Scenario",
    "MercuryFile",
    "MrxFile",
    "Path",
    "IsFilePresent"
]


def load_scenarios(
        selected_date: date
) -> pd.DataFrame:
    """Load scenario mappings from the API."""

    payload = get_json(
        "/scenarios",
        params={"cob_date": selected_date.isoformat()},
    )

    if not isinstance(payload, list):
        raise ValueError(
            "Unexpected response from /scenarios"
        )

    df = pd.DataFrame(payload)

    missing = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]
    
    if missing:
        raise ValueError(
            f"Scenario response is missing columns: {', '.join(missing)}"
        )

    return df[EXPECTED_COLUMNS]
