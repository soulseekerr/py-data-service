
import os
import requests
import pandas as pd


API = os.getenv("API_URL", "http://api:8000/v1")


def load_counterparty_data(selected_date) -> pd.DataFrame:
    """Load counterparty monitoring data from the API."""

    endpoint_url = f"{API}/counterparties"

    params = {
        "cob_date": selected_date.isoformat(),
    }

    try:
        response = requests.get(
            endpoint_url,
            params=params,
            timeout=10,
        )

        response.raise_for_status()
        payload = response.json()

        # Support either:
        # [...]
        #
        # or:
        # {"data": [...]}
        if isinstance(payload, dict):
            records = payload.get("data", [])
        elif isinstance(payload, list):
            records = payload
        else:
            raise ValueError("Unexpected API response format")

        df = pd.DataFrame(records)

        if df.empty:
            return pd.DataFrame(
                columns=[
                    "Counterparty",
                    "CVA Method",
                    "GRR",
                    "Status",
                    "Confidence"
                ]
            )

        # Rename API field names to UI-friendly column names.
        df = df.rename(
            columns={
                "counterparty": "Counterparty",
                "cva_method": "CVA Method",
                "grr": "GRR",
                "status": "Status",
                "confidence": "Confidence",

                "CVAMethod": "CVA Method",
                "Grr": "GRR",
            }
        )

        required_columns = [
            "Counterparty",
            "CVA Method",
            "GRR",
            "Status",
            "Confidence"
        ]

        missing_columns = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                "API response is missing columns: "
                + ", ".join(missing_columns)
            )

        # Keep only the columns shown in the grid.
        df = df[required_columns].copy()

        # Defensive type conversion.
        df["GRR"] = pd.to_numeric(df["GRR"], errors="coerce")
        df["Confidence"] = pd.to_numeric(
            df["Confidence"],
            errors="coerce",
        ).fillna(0)

        df["Confidence"] = df["Confidence"].clip(0, 100)

        return df

    except requests.Timeout as exc:
        raise RuntimeError(
            f"The API request timed out: {endpoint_url}"
        ) from exc

    except requests.ConnectionError as exc:
        raise RuntimeError(
            f"Could not connect to the API: {endpoint_url}"
        ) from exc

    except requests.HTTPError as exc:
        status_code = exc.response.status_code

        raise RuntimeError(
            f"API request failed with HTTP {status_code}: "
            f"{exc.response.text}"
        ) from exc

    except requests.RequestException as exc:
        raise RuntimeError(
            f"API request failed: {exc}"
        ) from exc

    except (ValueError, TypeError) as exc:
        raise RuntimeError(
            f"Invalid API response: {exc}"
        ) from exc
    