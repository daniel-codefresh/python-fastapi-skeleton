from typing import Any, Callable, Coroutine

from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response


class ExceptionHandlerRoute(APIRoute):
    """
    Custom APIRoute that handles application errors and exceptions.
    This is a wrapper for the original APIRoute class.
    We use this instead of an exception handler, because exception handlers
    for Exception class are buggy in FastAPI and mess up middleware execution order.
    """

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as exc:
                if (
                    isinstance(exc, HTTPException)
                    or isinstance(exc, RequestValidationError)
                    or isinstance(exc, ValueError)
                ):
                    raise exc
                logger.exception(exc)
                raise HTTPException(
                    status_code=500, detail="An unexpected error occurred."
                ) from exc

        return custom_route_handler
