
from dataclasses import dataclass
from datetime import date

import pandas as pd
import streamlit as st


@dataclass(slots=True)
class SidebarState:
    view: str
    cob_date: date


def render_sidebar(
    *,
    api_status: str,
    version: str,
    api_url: str,
    refresh_count: int,
) -> SidebarState:
    """Render the application sidebar."""

    st.sidebar.title("XVA Dashboard")

    view = st.sidebar.radio(
        "Navigation",
        options=[
            "Counterparties",
            "Scenario Mappings",
        ],
        index=0,
    )

    st.sidebar.divider()

    cob_date = st.sidebar.date_input(
        "COB Date",
        value=pd.Timestamp("2026-07-13"),
    )

    st.sidebar.divider()

    st.sidebar.caption("System")

    # status_icon = "🟢" if api_status == "Online" else "🔴"
    # st.write(f"{status_icon} **API:** {api_status}")

    if api_status == "Online":
        st.sidebar.success("API Online")
    else:
        st.sidebar.error("API Offline")

    st.sidebar.write(f"**Version:** {version}")
    st.sidebar.write(f"**Refresh:** {refresh_count}")

    st.sidebar.caption(api_url)

    return SidebarState(
        view=view,
        cob_date=cob_date,
    )
