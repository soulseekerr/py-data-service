
from datetime import date
from typing import Any

import requests
import pandas as pd
import streamlit as st

from api import load_counterparty_data
from grids import display_counterparty_grid


def get_selected_row(
    selected_rows: Any,
) -> dict[str, Any] | None:
    """Return the first selected AG Grid row as a dictionary."""

    if selected_rows is None:
        return None

    if isinstance(selected_rows, pd.DataFrame):
        if selected_rows.empty:
            return None

        return selected_rows.iloc[0].to_dict()

    if isinstance(selected_rows, list):
        if not selected_rows:
            return None

        first_row = selected_rows[0]

        if isinstance(first_row, dict):
            return first_row

    return None

def display_counterparty_details(
    counterparty: dict[str, Any],
) -> None:
    """Display details for the selected counterparty."""

    st.divider()
    st.subheader("Counterparty Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**Counterparty Code**")
        st.write(
            counterparty.get(
                "CptyCode",
                counterparty.get("Counterparty", "—"),
            )
        )

        st.markdown("**Counterparty Type**")
        st.write(counterparty.get("CptyType", "—"))

    with col2:
        st.markdown("**Risk Site**")
        st.write(counterparty.get("RiskSite", "—"))

        st.markdown("**GRR**")
        st.write(counterparty.get("GRR", "—"))

    with col3:
        st.markdown("**Status**")
        st.write(counterparty.get("Status", "—"))

        st.markdown("**Confidence**")
        st.write(counterparty.get("Confidence", "—"))

def show_counterparty_view(cob_date: date) -> None:
    """Load and render the counterparty view."""

    st.subheader("Counterparties")

    if "selected_counterparty" not in st.session_state:
        st.session_state.selected_counterparty = None

    try:
        counterparty_df = load_counterparty_data(cob_date)

    except requests.ConnectionError:
        st.error(
            "Could not connect to the counterparty API."
        )
        return

    except requests.Timeout:
        st.error(
            "The counterparty API request timed out."
        )
        return

    except requests.HTTPError as exc:
        status_code = (
            exc.response.status_code
            if exc.response is not None
            else "unknown"
        )

        response_text = (
            exc.response.text
            if exc.response is not None
            else str(exc)
        )

        st.error(
            f"Counterparty API returned HTTP "
            f"{status_code}: {response_text}"
        )
        return

    except RuntimeError as exc:
        st.error(str(exc))
        return

    except requests.RequestException as exc:
        st.error(
            f"Could not load counterparties: {exc}"
        )
        return

    except ValueError as exc:
        st.error(
            f"Invalid counterparty response: {exc}"
        )
        return

    if counterparty_df.empty:
        st.info(
            f"No counterparty data found for "
            f"{cob_date:%d %B %Y}."
        )
        return

    grid_response = display_counterparty_grid(
        counterparty_df
    )

    selected_cpties = grid_response.get(
        "selected_rows"
    )

    selected = get_selected_row(
        selected_cpties
    )

    if selected is not None:
        st.session_state.selected_counterparty = (
            selected
        )

    current_selection = (
            st.session_state.selected_counterparty
        )

    if current_selection is not None:
        display_counterparty_details(
            current_selection
        )
