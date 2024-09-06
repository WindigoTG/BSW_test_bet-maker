from fastapi import APIRouter

from .routers import bet_router
from .routers import event_router


router = APIRouter()
router.include_router(event_router, prefix="/events")
router.include_router(bet_router)
