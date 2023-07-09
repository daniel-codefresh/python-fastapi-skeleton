from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder

from .api.routes import router as api_router
from .helpers.helpers import fetch_message, fetch_message500
from .logger.logger import init_logging
from .middleware.correlation_id import (
    RequestCorrelationLogMiddleware,
)
from .route_error_handler import RouteErrorHandler
from functools import lru_cache

init_logging()


# @lru_cache()
# def get_settings():
#     return config.Settings()


app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_settings)])

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

app.include_router(api_router, prefix="/api")



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.get("/")
async def read_root():
    message = await fetch_message()
    logger.info("controller!")
    return {"message": message}


@app.get("/500/")
async def read_root500():
    message = await fetch_message500()
    logger.info("controller!")
    return {"message": message}
