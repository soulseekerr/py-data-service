
import logging
from datetime import date
from fastapi import APIRouter, Query

from ..schemas.counterparty import CounterpartyMapping

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    tags=["Counterparties"]
)

@router.get(
        "/counterparties", 
        response_model=list[CounterpartyMapping],
        summary="Get counterparties",
)
def get_counterparties(
    cob_date: date = Query(...),
) -> list[CounterpartyMapping]:

    logger.info(
        "Loading counterparties for cob_date=%s",
        cob_date,
    )

    results = [
        {
            "Counterparty": "BNP",
            "CVAMethod": "Financial",
            "Grr": 85.5,
            "Status": "OK",
            "Confidence": 100,
        },
        {
            "Counterparty": "HSBC",
            "CVAMethod": "Financial",
            "Grr": 73.5,
            "Status": "Changed",
            "Confidence": 89,
        },
        {
            "Counterparty": "Italy",
            "CVAMethod": "Sovereign",
            "Grr": 83.5,
            "Status": "OK",
            "Confidence": 81,
        },
        {
            "Counterparty": "Citi",
            "CVAMethod": "Financial",
            "Grr": 53.0,
            "Status": "Review",
            "Confidence": 55,
        },
        {
            "Counterparty": "Barclays",
            "CVAMethod": "Financial",
            "Grr": 25.0,
            "Status": "Error",
            "Confidence": 74,
        },
        {
            "Counterparty": "JPMorgan",
            "CVAMethod": "Financial",
            "Grr": 15.0,
            "Status": "Error",
            "Confidence": 60,
        }
    ]

    logger.info(
        "Loaded counterparties for cob_date=%s",
        cob_date,
    )

    return results