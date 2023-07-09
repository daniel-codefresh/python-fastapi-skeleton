from typing import Callable

from fastapi import HTTPException
from fastapi.routing import APIRoute
from loguru import logger
from starlette.requests import Request
from starlette.responses import Response


class RouteErrorHandler(APIRoute):
    """Custom APIRoute that handles application errors and exceptions"""

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except Exception as ex:
                if isinstance(ex, HTTPException):
                    raise ex
                logger.exception("uncaught error")
                # wrap error into pretty 500 exception
                raise HTTPException(
                    status_code=500, detail="An unexpected error occurred."
                )

        return custom_route_handler
