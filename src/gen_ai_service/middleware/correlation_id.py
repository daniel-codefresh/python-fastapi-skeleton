from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

CORRELATION_ID_CTX_KEY: str = "correlation_id"
REQUEST_ID_CTX_KEY: str = "request_id"

_correlation_id_ctx_var: ContextVar[str | None] = ContextVar(
    CORRELATION_ID_CTX_KEY, default=None
)
_request_id_ctx_var: ContextVar[str | None] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_correlation_id() -> str:
    return _correlation_id_ctx_var.get() or ""


def get_request_id() -> str:
    return _request_id_ctx_var.get() or ""


class RequestCorrelationLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        correlation_id = _correlation_id_ctx_var.set(
            request.headers.get("X-Correlation-ID", str(uuid4()))
        )
        request_id = _request_id_ctx_var.set(str(uuid4()))

        with logger.contextualize(
            request_id=get_request_id(), correlation_id=get_correlation_id()
        ):
            try:
                response = await call_next(request)
                response.headers["X-Correlation-ID"] = get_correlation_id()
                response.headers["X-Request-ID"] = get_request_id()
                return response
            finally:
                _correlation_id_ctx_var.reset(correlation_id)
                _request_id_ctx_var.reset(request_id)
