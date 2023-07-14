from fastapi import APIRouter

from .cron.routes import router as cron_router
from .health.routes import router as health_router

router = APIRouter()

router.include_router(cron_router, prefix="/cron")
router.include_router(health_router, prefix="/health")
