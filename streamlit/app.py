
import os
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from api_client import ApiError, check_api_health, load_api_version

from components.sidebar import render_sidebar

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

    sidebar = render_sidebar(
        api_status=api_status,
        version=version,
        api_url=API,
        refresh_count=st.session_state.TestCounter,
    )

    if sidebar.view == "Counterparties":
        show_counterparty_view(sidebar.cob_date)

    elif sidebar.view == "Scenario Mappings":
        show_scenario_view(sidebar.cob_date)

if __name__ == '__main__':
    main()