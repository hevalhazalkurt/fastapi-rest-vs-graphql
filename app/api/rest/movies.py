from typing import Sequence

from fastapi import APIRouter, Depends

from app.schemas.movies import MovieExtended, MovieInDB, MovieOrder, MovieSort
from app.services.movies import MovieService

router = APIRouter()


@router.get("/")
async def get_all_directors(
    extended: bool = False, skip: int = 0, limit: int = 20, order_by: MovieOrder = MovieOrder.title, sort_by: MovieSort = MovieSort.asc, service: MovieService = Depends(MovieService)
) -> Sequence[MovieInDB | MovieExtended]:
    return await service.get_all_movies(skip, limit, order_by=order_by, sort_by=sort_by, extended=extended)
