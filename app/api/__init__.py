from fastapi import APIRouter

from . import status
from .rest import directors, movies

router = APIRouter()

router.include_router(status.router, prefix="/rest/status", tags=["Server Status"])
router.include_router(directors.router, prefix="/rest/directors", tags=["Directors"])
router.include_router(movies.router, prefix="/rest/movies", tags=["Movies"])
