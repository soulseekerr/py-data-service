
import os
from typing import Any
import requests


API_URL = os.getenv(
    "API_URL",
    "http://api:8000/v1",
)

DEFAULT_TIMEOUT = 10


class ApiError(RuntimeError):
    """Raised when a backend API request fails."""


def get_json(
    path: str,
    *,
    params: dict[str, Any] | None = None,
) -> Any:
    url = f"{API_URL.rstrip('/')}/{path.lstrip('/')}"

    try:
        response = requests.get(
            url,
            params=params,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()

    except requests.Timeout as exc:
        raise ApiError(
            f"API request timed out: {url}"
        ) from exc

    except requests.ConnectionError as exc:
        raise ApiError(
            f"Could not connect to API: {url}"
        ) from exc

    except requests.HTTPError as exc:
        raise ApiError(
            f"API returned HTTP "
            f"{exc.response.status_code}: "
            f"{exc.response.text}"
        ) from exc

    except requests.RequestException as exc:
        raise ApiError(
            f"API request failed: {exc}"
        ) from exc

    except ValueError as exc:
        raise ApiError(
            f"API returned invalid JSON: {url}"
        ) from exc