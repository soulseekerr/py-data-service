
import logging
from pathlib import Path
from enum import StrEnum

logger = logging.getLogger(__name__)

class FilePresence(StrEnum):
    PRESENT = "Present"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


def probe_file(path: str, file_name: str, verbose: bool = False) -> FilePresence:
    """Probe the specified file and return its presence status."""
    if verbose:
        logger.info(f"Probing file %s/%s", path, file_name)

    try:
        if not path or not file_name:
            raise FileNotFoundError(f"Directory or file name is missing: {path}, {file_name}")

        file_path = Path(path).expanduser() / file_name

        is_present = True if file_path.is_file() else False

    except FileNotFoundError:
        logger.warning(
            "File missing path=%s file_name=%s",
            path,
            file_name,
        )
        return FilePresence.MISSING

    except Exception:
        logger.exception(
            "File probe failed path=%s file_name=%s",
            path,
            file_name,
        )
        return FilePresence.UNKNOWN

    return (
        FilePresence.PRESENT if is_present else FilePresence.MISSING
    )