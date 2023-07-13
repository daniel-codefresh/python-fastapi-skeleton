from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from .api.routes import router as api_router
from .config import Settings
from .middleware.correlation_id import (
    RequestCorrelationLogMiddleware,
)
from .helpers.route_error_handler import RouteErrorHandler


def get_app(settings: Settings) -> FastAPI:
    app = FastAPI()

    app.router.route_class = RouteErrorHandler

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost",
            "http://localhost:8000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(RequestCorrelationLogMiddleware)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    @app.get("/", include_in_schema=False)
    def redirect_to_docs() -> RedirectResponse:
        return RedirectResponse("/docs")

    return app
