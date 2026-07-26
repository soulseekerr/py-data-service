
import os
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from api import ApiError, check_api_health, load_api_version

from views import (
    show_counterparty_view,
    show_scenario_view,
)

API = os.getenv("API_URL", "http://api:8000/v1")

st.set_page_config(
    page_title="XVA Dashboard", 
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

def apply_page_style() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 1.5rem;
        }

        div[data-testid="stMetric"] {
            padding-top: 0.25rem;
            padding-bottom: 0.25rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    """Main function to run the Streamlit app."""

    apply_page_style()

    if "TestCounter" not in st.session_state:
        st.session_state.TestCounter = 0

    # Auto-refresh every 10 seconds
    st_autorefresh(interval=10000, key="dashboard_refresh")

    try:
        check_api_health()
        api_status = "Online"

        try:
            version = load_api_version()
        except ApiError:
            version = "Unavailable"

    except ApiError:
        api_status = "Offline"
        version = "Unavailable"

    except RuntimeError:
        version = "Unavailable"
        api_status = "Offline"

    st.session_state.TestCounter += 1

    with st.sidebar:
        st.title("XVA Dashboard")

        view = st.radio(
            "Navigation",
            options=[
                "Counterparties",
                "Scenario Mappings",
            ],
            index=0,
        )

        st.divider()

        cob_date = st.date_input(
            "COB Date",
            value=pd.to_datetime("2026-07-13"),
        )

        st.divider()

        st.caption("System")

        status_icon = "🟢" if api_status == "Online" else "🔴"

        st.write(
            f"{status_icon} **API:** {api_status}"
        )

        st.write(
            f"**Version:** {version}"
        )

        st.write(
            f"**Refresh:** "
            f"{st.session_state.TestCounter}"
        )

        st.caption(f"Endpoint: {API}")

    if view == "Counterparties":
        show_counterparty_view(cob_date)

    elif view == "Scenario Mappings":
        show_scenario_view(cob_date)


if __name__ == '__main__':
    main()