
from pydantic import BaseModel


class ScenarioMapping(BaseModel):
    Tier: str
    Scenario: str
    MercuryFile: str
    MrxFile: str
    Path: str
    IsFilePresent: str