from fastapi import FastAPI, APIRouter
from .core.logging import configure_logging
from .routers.version import router as version_router
from .routers.counterparties import router as counterparty_router
from .routers.scenarios import router as scenarios_router

from .core.request_logging import (
    RequestLoggingMiddleware,
)

configure_logging()

app = FastAPI(title="My Risk Analytics API")

router = APIRouter(prefix="/v1")

app.include_router(scenarios_router)
app.include_router(counterparty_router)
app.include_router(version_router)

app.add_middleware(
    RequestLoggingMiddleware
)