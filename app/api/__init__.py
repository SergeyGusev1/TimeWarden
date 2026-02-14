from fastapi import APIRouter

from app.api.v1.active_endpoints import router as active_router
from app.api.v1.stats_endpoints import router as stats_router


router = APIRouter()

router.include_router(active_router)
router.include_router(stats_router)
