from fastapi import FastAPI, APIRouter
from .routers.version import router as version_router
from .routers.counterparties import router as counterparty_router
from .routers.scenarios import router as scenarios_router

app = FastAPI(title="My Risk Analytics API")

router = APIRouter(prefix="/v1")

app.include_router(scenarios_router)
app.include_router(counterparty_router)
app.include_router(version_router)