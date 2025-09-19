from typing import Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND

from app.core.logging_setup import logger
from app.db.session import get_db
from app.repository.movies import MovieCRUD, get_movie_crud
from app.schemas.movies import MovieExtended, MovieInDB, MovieOrder, MovieSort, MovieCreate, MovieUpdate


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


    async def get_movie_by_id(self, id: UUID, extended: bool = False) -> MovieInDB | MovieExtended:
        result = None
        try:
            result = await self.crud.get_one(self.db, id=id, extended=extended)

            if extended and isinstance(result, Sequence):
                movie = MovieExtended.model_validate(result[0][0])
                movie.director = result[0][1]
                movie.genre = " | ".join([g for g in result[0][2]]) if result[0][2] else ""
                return movie
            return MovieInDB.model_validate(result)
        except Exception as e:
            error_detail = f"An error occurred while fetching movie. {e}" if result else f"Movie with id {id} not found."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)


    async def create_movie(self, movie_data: MovieCreate) -> MovieInDB:
        result = None
        try:
            result = await self.crud.create(self.db, movie_data=movie_data)
            return MovieInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while creating a movie." if result else "Director not found"
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


    async def update_movie(self, movie_data: MovieUpdate) -> MovieInDB:
        try:
            result = await self.crud.update(self.db, movie_data=movie_data)
            return MovieInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while updating a movie."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
