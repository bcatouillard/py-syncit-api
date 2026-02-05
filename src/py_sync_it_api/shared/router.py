"""App router."""

from fastapi import APIRouter

from py_sync_it_api.health.endpoints import router as health_check_router
from py_sync_it_api.systems.endpoints import router as system_router

router = APIRouter()
router.include_router(health_check_router)
router.include_router(system_router)
