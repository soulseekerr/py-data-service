
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from fastapi import APIRouter, Query

from api.services.file_service import FilePresence, probe_file
from ..schemas.scenario import ScenarioMapping

logger = logging.getLogger(__name__)

def probe_files(files: list[ScenarioMapping]) -> list[ScenarioMapping]:
    """Probe files in concurrent threads and update the FileStatus attribute of each ScenarioMapping object."""

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(probe_file, file.Path, file.MercuryFile): file
            for file in files
        }

        for future in as_completed(futures):
            file = futures[future]

            try:
                file.FileStatus = future.result()
            except Exception:
                file.FileStatus = FilePresence.UNKNOWN

    return files


router = APIRouter(
    prefix="/v1",
    tags=["Scenarios"],
)   

@router.get(
    "/scenarios",
    response_model=list[ScenarioMapping],
    summary="Get scenarios",
)
def get_scenarios(
    cob_date: date = Query(...),
) -> list[ScenarioMapping]:
    """Get scenarios status for the given COB date."""

    logger.info(
        "Loading scenarios for cob_date=%s",
        cob_date,
    )

    SCENARIOS = [
        ScenarioMapping(
            Tier="Tier 1",
            Scenario="Credit Delta Gear",
            MercuryFile="CR_SP01.csv",
            MrxFile="CREDIT_DELTA_GEAR.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear EUR Tenors",
            MercuryFile="IR_delta_EUR_tenors.csv",
            MrxFile="DELTA_IR_EUR_TENORS.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear USD Tenors",
            MercuryFile="IR_delta_USD_tenors.csv",
            MrxFile="DELTA_IR_USD_TENORS.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear GBP Tenors",
            MercuryFile="IR_delta_GBP_tenors.csv",
            MrxFile="DELTA_IR_GBP_TENORS.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear JPY Tenors",
            MercuryFile="IR_delta_JPY_tenors.csv",
            MrxFile="DELTA_IR_JPY_TENORS.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta KRW",
            MercuryFile="FX_delta_KRW.csv",
            MrxFile="DELTA_FX_KRW.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta KRO",
            MercuryFile="FX_delta_KRO.csv",
            MrxFile="DELTA_FX_KRO.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta BRL",
            MercuryFile="FX_delta_BRL.csv",
            MrxFile="DELTA_FX_BRL.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta BRO",
            MercuryFile="FX_delta_BRO.csv",
            MrxFile="DELTA_FX_BRO.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EURCPI",
            MercuryFile="Infl_delta_EURCPI.csv",
            MrxFile="DELTA_INFLATION_EURCPI.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EURXT",
            MercuryFile="Infl_delta_EURXT.csv",
            MrxFile="DELTA_INFLATION_EURXT.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EUR",
            MercuryFile="Infl_delta_EUR.csv",
            MrxFile="DELTA_INFLATION_EUR.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta USD",
            MercuryFile="Infl_delta_USD.csv",
            MrxFile="DELTA_INFLATION_USD.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta BROCPI",
            MercuryFile="Infl_delta_BROCPI.csv",
            MrxFile="DELTA_INFLATION_BROCPI.DAT",
            Path="/app/mock_data/scenarios",
            FileStatus=FilePresence.UNKNOWN,
        ),
        
    ]

    probe_results = probe_files(SCENARIOS)

    results = [
        scenario.model_copy(
            update={
                "FileStatus": result.FileStatus,
            }
        )
        for scenario, result in zip(
            SCENARIOS,
            probe_results,
            strict=True,
        )
    ]

    logger.info(
        "Loaded scenarios for cob_date=%s",
        cob_date,
    )

    return results