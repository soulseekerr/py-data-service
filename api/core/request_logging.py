import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)


logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        request_id = request.headers.get(
            "X-Request-ID",
            str(uuid4()),
        )

        started_at = perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            duration_ms = round(
                (perf_counter() - started_at)
                * 1_000
            )

            logger.exception(
                "Request failed request_id=%s "
                "method=%s path=%s duration_ms=%d",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )

            raise

        duration_ms = round(
            (perf_counter() - started_at)
            * 1_000
        )

        response.headers[
            "X-Request-ID"
        ] = request_id

        logger.info(
            "Request completed request_id=%s "
            "method=%s path=%s status_code=%d "
            "duration_ms=%d",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )

        return response