
from datetime import date
from typing import Any
import requests
import pandas as pd
import streamlit as st

from api import load_scenarios
from grids import display_scenario_grid


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

def display_scenario_details(
    scenario: dict[str, Any],
) -> None:
    """Display details for the selected scenario."""

    st.divider()
    st.subheader("Scenario Details")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Scenario**")
        st.write(scenario.get("Scenario", "—"))

        st.markdown("**Tier**")
        st.write(scenario.get("Tier", "—"))

        st.markdown("**Path**")
        st.write(scenario.get("Path", "—"))

    with col2:
        st.markdown("**Mercury File**")
        st.write(scenario.get("MercuryFile", "—"))

        st.markdown("**MRX File**")
        st.write(scenario.get("MrxFile", "—"))

def show_scenario_view(cob_date: date) -> None:
    """Load and render the scenario mapping view."""

    st.subheader("Scenario Mappings")

    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = None

    try:
        scenario_df = load_scenarios(
            cob_date
        )

    except RuntimeError as exc:
        st.error(str(exc))
        return

    except requests.ConnectionError:
        st.error(
            "Could not connect to the scenario API."
        )
        return

    except requests.Timeout:
        st.error(
            "The scenario API request timed out."
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
            f"Scenario API returned HTTP "
            f"{status_code}: {response_text}"
        )
        return

    except requests.RequestException as exc:
        st.error(
            f"Could not load scenarios: {exc}"
        )
        return

    except ValueError as exc:
        st.error(
            f"Invalid scenario response: {exc}"
        )
        return

    if scenario_df.empty:
        st.session_state.selected_scenario = None

        st.info(
            f"No scenario data found for "
            f"{cob_date:%d %B %Y}."
        )
        return

    grid_response = display_scenario_grid(scenario_df)

    selected_scenario = get_selected_row(grid_response.get("selected_rows"))

    if selected_scenario is not None:
        st.session_state.selected_scenario = (
            selected_scenario
        )

    current_selection = (
        st.session_state.selected_scenario
    )

    if current_selection is not None:
        display_scenario_details(current_selection)