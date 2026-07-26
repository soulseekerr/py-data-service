
import os
import streamlit as st
from api_client.client import get_json


def load_api_version() -> str:
    payload = get_json("/version")

    if not isinstance(payload, dict):
        raise ValueError(
            "Invalid response returned by the version endpoint."
        )

    version = payload.get("version")

    if not version:
        raise ValueError(
            "The version endpoint did not return a version."
        )

    return str(version)

def check_api_health() -> bool:
    get_json("/health")
    return True