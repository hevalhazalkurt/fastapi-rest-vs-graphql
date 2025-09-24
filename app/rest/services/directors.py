from typing import Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from strawberry import ID

from app.core.logging_setup import logger
from app.db.session import get_db
from app.db.utils import get_all
from app.models import Movie
from app.rest.repository.directors import DirectorCRUD, get_director_crud
from app.rest.schemas.directors import DirectorCreate, DirectorExtended, DirectorInDB, DirectorUpdate
from app.rest.schemas.movies import MovieInDirector


class DirectorsService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        crud: DirectorCRUD = Depends(get_director_crud),
    ):
        self.db = db
        self.crud = crud

    async def get_all_directors(self, skip: int = 0, limit: int = 20, with_movies: bool = False) -> Sequence[DirectorInDB | DirectorExtended]:
        try:
            results: Sequence = await self.crud.get_all(self.db, skip=skip, limit=limit, with_movies=with_movies)
            if with_movies:
                directors_with_movies: list[DirectorExtended] = []
                for director, movies in results:
                    director_resp = DirectorExtended.model_validate(director)
                    director_resp.movies = [MovieInDirector.model_validate(movie) for movie in movies] if movies else []
                    directors_with_movies.append(director_resp)
                return directors_with_movies
            return [DirectorInDB.model_validate(data) for data in results]
        except Exception as e:
            error_detail = "An error occurred while fetching directors."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def get_director_by_id(self, id: UUID | ID, with_movies: bool = False) -> DirectorInDB | DirectorExtended:
        result = None
        try:
            result = await self.crud.get_one(self.db, id=id, with_movies=with_movies)
            if with_movies and isinstance(result, Sequence):
                director = DirectorExtended.model_validate(result[0][0])
                director.movies = [MovieInDirector.model_validate(movie) for movie in result[0][1]] if result[0][1] else []
                return director
            return DirectorInDB.model_validate(result)
        except Exception as e:
            error_detail = f"An error occurred while fetching director. {e}" if result else f"Director with id {id} not found."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)

    async def get_director_by_name(self, name: str, with_movies: bool = False) -> DirectorInDB | DirectorExtended:
        result = None
        try:
            result = await self.crud.get_one(self.db, name=name, with_movies=with_movies)
            if with_movies and isinstance(result, Sequence):
                director = DirectorExtended.model_validate(result[0][0])
                director.movies = [MovieInDirector.model_validate(movie) for movie in result[0][1]] if result[0][1] else []
                return director
            return DirectorInDB.model_validate(result)
        except Exception as e:
            error_detail = f"An error occurred while fetching director. {e}" if result else f"Director with name {name} not found."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)

    async def get_director_movies(self, director_ids: list[UUID]) -> dict:
        try:
            if not director_ids:
                return {}

            query = (
                select(
                    Movie.director_id,
                    func.array_agg(
                        func.jsonb_build_object(
                            "uuid", Movie.uuid,
                            "title", Movie.title,
                            "release_year", Movie.release_year
                        )))
                .where(Movie.director_id.in_(director_ids)).group_by(Movie.director_id)
            )
            result = await get_all(self.db, query)
            director_movies_map = {
                director_id: [MovieInDirector.model_validate(m) for m in movies]
                for director_id, movies in result
            }
            return director_movies_map
        except Exception as e:
            error_detail = f"An error occurred while fetching directors' movies. {e}"
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)

    async def create_director(self, director_data: DirectorCreate) -> DirectorInDB:
        try:
            result = await self.crud.create(self.db, name=director_data.name)
            return DirectorInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while creating a director."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def update_director(self, director_data: DirectorUpdate) -> DirectorInDB:
        try:
            result = await self.crud.update(self.db, director_data=director_data)
            return DirectorInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while updating a director."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def remove_director(self, id: UUID) -> DirectorInDB:
        try:
            result = await self.crud.delete(self.db, id=id)
            return DirectorInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while removing a director."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
