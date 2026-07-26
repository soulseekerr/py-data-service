
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from renderers import (
    CONFIDENCE_RENDERER,
    STATUS_BADGE_RENDERER,
)


def display_counterparty_grid(df: pd.DataFrame):
    """Render the counterparty monitoring grid."""

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True,
    )

    gb.configure_pagination(
        enabled=True,
        paginationPageSize=20,
    )

    gb.configure_selection(
        selection_mode="single",
        use_checkbox=True,
    )

    gb.configure_column(
        "Counterparty",
        pinned="left",
    )

    gb.configure_column(
        "CVA Method",
        pinned="left",
    )

    gb.configure_column(
        "GRR",
        type=["numericColumn"],
        valueFormatter="x.toFixed(1)",
    )

    gb.configure_column(
        "Status",
        cellRenderer=STATUS_BADGE_RENDERER,
        minWidth=100,
        maxWidth=100,
    )

    gb.configure_column(
        "Confidence",
        cellRenderer=CONFIDENCE_RENDERER,
        minWidth=120,
        maxWidth=120,
        sortable=True,
        filter="agNumberColumnFilter",
    )

    grid_options = gb.build()

    return AgGrid(
        df,
        gridOptions=grid_options,

        update_mode=GridUpdateMode.SELECTION_CHANGED,

        height=min(40 * len(df) + 70, 500),

        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        theme="streamlit",
        # Giving AgGrid a stable key, helps Streamlit preserve the component consistently across reruns.
        key="counterparty-grid",
    )

# theme="balham"
# theme="material"
# theme="alpine"
# theme="fresh"