from fastapi import APIRouter

from . import status
from .rest import directors, genres, movies

router = APIRouter()

router.include_router(status.router, prefix="/rest/status", tags=["Server Status"])
router.include_router(directors.router, prefix="/rest/directors", tags=["Directors"])
router.include_router(movies.router, prefix="/rest/movies", tags=["Movies"])
router.include_router(genres.router, prefix="/rest/genres", tags=["Genres"])
