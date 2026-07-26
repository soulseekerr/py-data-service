
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from renderers import (
    TIER_RENDERER
)

def prepare_scenario_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and sort scenarios by Tier 1 to Tier 6."""

    prepared_df = df.copy()

    prepared_df["TierNumber"] = (
        prepared_df["Tier"]
        .str.extract(r"(\d+)", expand=False)
        .astype("Int64")
    )

    prepared_df = (
        prepared_df[
            prepared_df["TierNumber"].between(
                1,
                6,
                inclusive="both",
            )
        ]
        .sort_values(
            ["TierNumber", "Scenario"]
        )
        .reset_index(drop=True)
    )

    return prepared_df


def display_scenario_grid(df: pd.DataFrame):
    """Render the expandable scenario tree grouped by tier."""

    scenarios_df = prepare_scenario_data(df)

    scenario_gb = GridOptionsBuilder.from_dataframe(scenarios_df)

    scenario_gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True,
    )

    # Hidden helper column used to sort Tier 1 ... Tier 6 correctly.
    scenario_gb.configure_column(
        "TierNumber",
        hide=True,
        sort="asc",
    )

    # Make Tier the expandable grouping level.
    scenario_gb.configure_column(
        "Tier",
        rowGroup=True,
        hide=True,
    )

    scenario_gb.configure_column(
        "Scenario",
        minWidth=280,
    )

    scenario_gb.configure_column(
        "MercuryFile",
        header_name="Mercury File",
        minWidth=220,
    )

    scenario_gb.configure_column(
        "MrxFile",
        header_name="MRX File",
        minWidth=230,
    )

    scenario_gb.configure_column(
        "Path",
        minWidth=140,
    )

    scenario_gb.configure_column(
            "IsFilePresent",
            header_name="Is File Present",
            minWidth=100,
        )

    scenario_gb.configure_selection(
        selection_mode="single",
        use_checkbox=False,
    )

    scenario_gb.configure_grid_options(
        # 0 means tiers start collapsed.
        # Use -1 to open all tiers initially.
        groupDefaultExpanded=0,

        animateRows=True,

        autoGroupColumnDef={
            "headerName": "Tier / Scenario",
            "minWidth": 100,
            # "pinned": "left",
            "cellRenderer": "agGroupCellRenderer",
            "cellRendererParams": {
                "suppressCount": False,
                "innerRenderer": TIER_RENDERER,
            },
        },
    )

    grid_options = scenario_gb.build()

    return AgGrid(
        scenarios_df,
        gridOptions=grid_options,

        update_mode=GridUpdateMode.SELECTION_CHANGED,

        height=min(45 * len(scenarios_df) + 180, 550),

        fit_columns_on_grid_load=True,

        allow_unsafe_jscode=True,

        # Row grouping is an AG Grid Enterprise feature.
        enable_enterprise_modules=True,

        theme="streamlit",
        key="scenario-grid",
    )