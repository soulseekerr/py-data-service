
from unittest.mock import Mock, patch

import pytest
import requests

from api_client.client import (
    API_URL,
    DEFAULT_TIMEOUT,
    ApiError,
    get_json,
)


@patch("api_client.client.requests.get")
def test_get_json_returns_payload(
    mock_get: Mock,
) -> None:
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "status": "ok",
    }

    mock_get.return_value = response

    result = get_json("/health")

    assert result == {
        "status": "ok",
    }

    mock_get.assert_called_once_with(
        f"{API_URL}/health",
        params=None,
        timeout=DEFAULT_TIMEOUT,
    )


@patch("api_client.client.requests.get")
def test_get_json_converts_timeout_to_api_error(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(
        ApiError,
        match="timed out",
    ):
        get_json("/health")


@patch("api_client.client.requests.get")
def test_get_json_converts_connection_error(
    mock_get: Mock,
) -> None:
    mock_get.side_effect = requests.ConnectionError()

    with pytest.raises(
        ApiError,
        match="Could not connect",
    ):
        get_json("/health")


@patch("api_client.client.requests.get")
def test_get_json_rejects_invalid_json(
    mock_get: Mock,
) -> None:
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.side_effect = ValueError(
        "Invalid JSON"
    )

    mock_get.return_value = response

    with pytest.raises(
        ApiError,
        match="invalid JSON",
    ):
        get_json("/health")

@patch("api_client.client.requests.get")
def test_get_json_converts_http_error(
    mock_get: Mock,
) -> None:
    response = Mock()
    response.status_code = 500
    response.text = "Internal Server Error"

    error = requests.HTTPError(
        response=response,
    )

    response.raise_for_status.side_effect = error
    mock_get.return_value = response

    with pytest.raises(
        ApiError,
        match="HTTP 500",
    ):
        get_json("/health")