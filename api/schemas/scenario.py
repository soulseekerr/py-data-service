
from pydantic import BaseModel

from api.services.file_service import FilePresence


class ScenarioMapping(BaseModel):
    Tier: str
    Scenario: str
    MercuryFile: str
    FileStatus: FilePresence = FilePresence.UNKNOWN
    MrxFile: str
    Path: str