
from datetime import date
from typing import Any
import requests
import pandas as pd
import streamlit as st

from api_client import load_scenarios
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

def filter_scenarios(
    scenario_df: pd.DataFrame,
    search_text: str,
) -> pd.DataFrame:
    """Filter scenarios using a case-insensitive search across all columns."""

    search_text = search_text.strip()

    if not search_text:
        return scenario_df

    searchable_columns = [
        "Scenario",
        "MercuryFile",
        "MrxFile",
    ]

    search_mask = pd.Series(
        False,
        index=scenario_df.index,
    )

    for column in searchable_columns:
        if column not in scenario_df.columns:
            continue

        column_matches = (
            scenario_df[column]
            .fillna("")
            .astype(str)
            .str.contains(
                search_text,
                case=False,
                regex=False,
            )
        )

        search_mask = search_mask | column_matches

    return scenario_df.loc[search_mask].copy()

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

    # grid_response = display_scenario_grid(scenario_df)

    search_text = st.text_input(
        "Search scenarios",
        placeholder=(
            "Search by scenario or file name"
        ),
        key="scenario_search",
    )

    filtered_scenario_df = filter_scenarios(
        scenario_df,
        search_text,
    )

    result_count = len(filtered_scenario_df)
    total_count = len(scenario_df)

    if search_text:
        st.caption(
            f"Showing {result_count} of {total_count} scenarios"
        )
    else:
        st.caption(
            f"{total_count} scenarios"
        )

    if filtered_scenario_df.empty:
        st.session_state.selected_scenario = None

        st.info(
            f'No scenarios match "{search_text}".'
        )
        return

    if "scenario_group_expansion" not in st.session_state:
        st.session_state.scenario_group_expansion = 0

    expand_column, collapse_column, spacer = st.columns([1, 1, 6])

    with expand_column:
        if st.button(
            "⊞ Expand all",
            key="expand_all_scenarios",
            use_container_width=True,
        ):
            st.session_state.scenario_group_expansion = -1

    with collapse_column:
        if st.button(
            "⊟ Collapse all",
            key="collapse_all_scenarios",
            use_container_width=True,
        ):
            st.session_state.scenario_group_expansion = 0

    st.caption(
        f"Showing {len(filtered_scenario_df)} "
        f"of {len(scenario_df)} scenarios"
    )

    grid_response = display_scenario_grid(
        filtered_scenario_df,
        group_expansion=(
            st.session_state.scenario_group_expansion
        ),
    )

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