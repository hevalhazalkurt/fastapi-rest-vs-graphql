from fastapi import APIRouter

from . import status
from .rest import directors

router = APIRouter()

router.include_router(status.router, prefix="/rest/status", tags=["Server Status"])
router.include_router(directors.router, prefix="/rest/directors", tags=["Directors"])
