from api.services.file_service import probe_file, FilePresence


def test_existing_file_returns_true(
    tmp_path,
):
    test_file = tmp_path / "scenario.csv"
    test_file.write_text(
        "scenario,value\nbase,100\n",
        encoding="utf-8",
    )

    result = probe_file(
        path=str(tmp_path),
        file_name="scenario.csv",
    )

    assert result == FilePresence.PRESENT


def test_missing_file_returns_false(
    tmp_path,
):
    result = probe_file(
        path=str(tmp_path),
        file_name="missing.csv",
    )

    assert result == FilePresence.MISSING


def test_directory_is_not_treated_as_file(
    tmp_path,
):
    directory = tmp_path / "scenario.csv"
    directory.mkdir()

    result = probe_file(
        path=str(tmp_path),
        file_name="scenario.csv",
    )

    assert result == FilePresence.MISSING


def test_empty_file_name_returns_false(
    tmp_path,
):
    result = probe_file(
        path=str(tmp_path),
        file_name="",
    )

    assert result == FilePresence.MISSING