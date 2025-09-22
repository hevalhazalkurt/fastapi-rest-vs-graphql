from fastapi import APIRouter

from app.api import status
from app.api.rest import directors, genres, movies

rest_router = APIRouter(prefix="/rest")

rest_router.include_router(status.router, prefix="/status", tags=["Server Status"])
rest_router.include_router(directors.router, prefix="/directors", tags=["Directors"])
rest_router.include_router(movies.router, prefix="/movies", tags=["Movies"])
rest_router.include_router(genres.router, prefix="/genres", tags=["Genres"])
