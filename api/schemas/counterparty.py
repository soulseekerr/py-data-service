
from pydantic import BaseModel


class CounterpartyMapping(BaseModel):
    Counterparty: str
    CVAMethod: str
    Grr: float
    Status: str
    Confidence: float