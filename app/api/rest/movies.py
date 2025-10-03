from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth.security import get_current_user
from app.rest.schemas.movies import MovieCreate, MovieExtended, MovieInDB, MovieOrder, MovieSort, MovieUpdate
from app.rest.services.movies import MovieService

router = APIRouter()


@router.get("/")
async def get_all_directors(
    extended: bool = False, skip: int = 0, limit: int = 20, order_by: MovieOrder = MovieOrder.title, sort_by: MovieSort = MovieSort.asc, service: MovieService = Depends(MovieService), user: str = Depends(get_current_user)
) -> Sequence[MovieInDB | MovieExtended]:
    return await service.get_all_movies(skip, limit, order_by=order_by, sort_by=sort_by, extended=extended)


@router.get("/{id}")
async def get_movie(id: UUID, extended: bool = False, service: MovieService = Depends(MovieService), user: str = Depends(get_current_user)) -> MovieInDB | MovieExtended:
    return await service.get_movie_by_id(id, extended=extended)


@router.post("/movie")
async def create_movie(movie_data: MovieCreate, service: MovieService = Depends(MovieService), user: str = Depends(get_current_user)) -> MovieInDB:
    return await service.create_movie(movie_data)


@router.patch("/movie")
async def update_movie(movie_data: MovieUpdate, service: MovieService = Depends(MovieService), user: str = Depends(get_current_user)) -> MovieInDB:
    return await service.update_movie(movie_data)


@router.delete("/movie/{id}")
async def remove_movie(id: UUID, service: MovieService = Depends(MovieService), user: str = Depends(get_current_user)) -> MovieInDB:
    return await service.remove_movie(id)
