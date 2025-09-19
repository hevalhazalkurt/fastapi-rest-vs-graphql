from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends

from app.schemas.movies import MovieExtended, MovieInDB, MovieOrder, MovieSort, MovieCreate, MovieUpdate
from app.services.movies import MovieService

router = APIRouter()


@router.get("/")
async def get_all_directors(
    extended: bool = False,
    skip: int = 0,
    limit: int = 20,
    order_by: MovieOrder = MovieOrder.title,
    sort_by: MovieSort = MovieSort.asc,
    service: MovieService = Depends(MovieService)
) -> Sequence[MovieInDB | MovieExtended]:
    return await service.get_all_movies(skip, limit, order_by=order_by, sort_by=sort_by, extended=extended)


@router.get("/{id}")
async def get_movie(
        id: UUID,
        extended: bool = False,
        service: MovieService = Depends(MovieService)
) -> MovieInDB | MovieExtended:
    return await service.get_movie_by_id(id, extended=extended)


@router.post("/movie")
async def create_movie(
        movie_data: MovieCreate,
        service: MovieService = Depends(MovieService)
) -> MovieInDB:
    return await service.create_movie(movie_data)


@router.patch("/movie")
async def update_movie(
        movie_data: MovieUpdate,
        service: MovieService = Depends(MovieService)
) -> MovieInDB:
    return await service.update_movie(movie_data)
