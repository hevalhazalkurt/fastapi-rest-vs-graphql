from typing import Sequence

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.logging_setup import logger
from app.db.session import get_db
from app.repository.movies import MovieCRUD, get_movie_crud
from app.schemas.movies import MovieExtended, MovieInDB, MovieOrder, MovieSort


class MovieService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        crud: MovieCRUD = Depends(get_movie_crud),
    ):
        self.db = db
        self.crud = crud

    async def get_all_movies(
        self, skip: int = 0, limit: int = 20, order_by: MovieOrder = MovieOrder.title, sort_by: MovieSort = MovieSort.asc, extended: bool = False
    ) -> Sequence[MovieInDB | MovieExtended]:
        try:
            results: Sequence = await self.crud.get_all(self.db, skip=skip, limit=limit, order_by=order_by, sort_by=sort_by, extended=extended)
            if extended:
                extended_movies: list[MovieExtended] = []
                for movie, director, genres in results:
                    movie_resp = MovieExtended.model_validate(movie)
                    movie_resp.director = director
                    movie_resp.genre = " | ".join([g for g in genres]) if genres else ""
                    extended_movies.append(movie_resp)
                return extended_movies
            return [MovieInDB.model_validate(data) for data in results]
        except Exception as e:
            error_detail = "An error occurred while fetching movies."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
