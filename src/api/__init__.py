from fastapi import APIRouter

from .routers import event_router


router = APIRouter()
router.include_router(event_router, prefix="/events")
