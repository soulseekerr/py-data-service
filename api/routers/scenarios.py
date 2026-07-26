
from datetime import date
from fastapi import APIRouter, Query

from ..schemas.scenario import ScenarioMapping

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

    return [
        ScenarioMapping(
            Tier="Tier 1",
            Scenario="Credit Delta Gear",
            MercuryFile="CR_SP01.csv",
            MrxFile="CREDIT_DELTA_GEAR.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear EUR Tenors",
            MercuryFile="IR_delta_EUR_tenors.csv",
            MrxFile="DELTA_IR_EUR_TENORS.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear USD Tenors",
            MercuryFile="IR_delta_USD_tenors.csv",
            MrxFile="DELTA_IR_USD_TENORS.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear GBP Tenors",
            MercuryFile="IR_delta_GBP_tenors.csv",
            MrxFile="DELTA_IR_GBP_TENORS.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 2",
            Scenario="IR Delta Gear JPY Tenors",
            MercuryFile="IR_delta_JPY_tenors.csv",
            MrxFile="DELTA_IR_JPY_TENORS.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta KRW",
            MercuryFile="FX_delta_KRW.csv",
            MrxFile="DELTA_FX_KRW.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta KRO",
            MercuryFile="FX_delta_KRO.csv",
            MrxFile="DELTA_FX_KRO.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta BRL",
            MercuryFile="FX_delta_BRL.csv",
            MrxFile="DELTA_FX_BRL.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 3",
            Scenario="FX Delta BRO",
            MercuryFile="FX_delta_BRO.csv",
            MrxFile="DELTA_FX_BRO.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EURXT",
            MercuryFile="Infl_delta_EURXT.csv",
            MrxFile="DELTA_INFLATION_EURXT.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EURXT",
            MercuryFile="Infl_delta_EURXT.csv",
            MrxFile="DELTA_INFLATION_EURXT.DAT",
            Path="downstream",
            IsFilePresent="No",
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta EUR",
            MercuryFile="Infl_delta_EUR.csv",
            MrxFile="DELTA_INFLATION_EUR.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta USD",
            MercuryFile="Infl_delta_USD.csv",
            MrxFile="DELTA_INFLATION_USD.DAT",
            Path="downstream",
            IsFilePresent="No",
        ),
        ScenarioMapping(
            Tier="Tier 4",
            Scenario="Inflation Delta BROCPI",
            MercuryFile="Infl_delta_BROCPI.csv",
            MrxFile="DELTA_INFLATION_BROCPI.DAT",
            Path="downstream",
            IsFilePresent="Yes",
        ),
        
    ]