
from pathlib import Path
from enum import StrEnum


class FilePresence(StrEnum):
    PRESENT = "Present"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


def probe_file(path: str, file_name: str, verbose: bool = False) -> FilePresence:
    """Probe the specified file and return its presence status."""
    if verbose:
        print(f"Probing file: {path}/{file_name}")

    try:
        if not path or not file_name:
            raise FileNotFoundError(f"Directory or file name is missing: {path}, {file_name}")

        file_path = Path(path).expanduser() / file_name

        is_present = True if file_path.is_file() else False

    except FileNotFoundError:
        return FilePresence.MISSING

    except Exception:
        return FilePresence.UNKNOWN

    return (
        FilePresence.PRESENT if is_present else FilePresence.MISSING
    )