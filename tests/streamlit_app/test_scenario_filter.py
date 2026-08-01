import pandas as pd

from views.scenario_view import filter_scenarios


def make_scenarios() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Tier": "Tier 1",
                "Scenario": "IR Parallel Shift",
                "MercuryFile": "ir_parallel.csv",
                "MrxFile": "ir_parallel.mrx",
                "Path": "/risk/ir",
                "FileStatus": "Present",
            },
            {
                "Tier": "Tier 2",
                "Scenario": "FX Spot Shock",
                "MercuryFile": "fx_spot.csv",
                "MrxFile": "fx_spot.mrx",
                "Path": "/risk/fx",
                "FileStatus": "Not Present",
            },
        ]
    )


def test_empty_search_returns_all_rows():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "",
    )

    assert len(result) == 2


def test_search_by_scenario():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "parallel",
    )

    assert len(result) == 1
    assert result.iloc[0]["Scenario"] == "IR Parallel Shift"


def test_search_is_case_insensitive():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "FX SPOT",
    )

    assert len(result) == 1
    assert result.iloc[0]["Tier"] == "Tier 2"


def test_search_across_file_name():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "ir_parallel.mrx",
    )

    assert len(result) == 1


def test_search_with_no_results():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "nonexistent",
    )

    assert result.empty


def test_search_treats_special_characters_as_text():
    scenarios = make_scenarios()

    result = filter_scenarios(
        scenarios,
        "[",
    )

    assert result.empty