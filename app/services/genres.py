from typing import Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.logging_setup import logger
from app.db.session import get_db
from app.repository.genres import GenreCRUD, get_genre_crud
from app.schemas.genres import GenreCreate, GenreExtended, GenreInDB, GenreUpdate
from app.schemas.movies import MovieInDB


class GenresService:
    def __init__(
        self,
        db: AsyncSession = Depends(get_db),
        crud: GenreCRUD = Depends(get_genre_crud),
    ):
        self.db = db
        self.crud = crud

    async def get_all_genres(self, skip: int = 0, limit: int = 20) -> Sequence[GenreInDB]:
        try:
            results: Sequence = await self.crud.get_all(self.db, skip=skip, limit=limit)
            return [GenreInDB.model_validate(data) for data in results]
        except Exception as e:
            error_detail = "An error occurred while fetching genres."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def get_genre_by_id(self, id: UUID, with_movies: bool = False) -> GenreInDB | GenreExtended:
        result = None
        try:
            result = await self.crud.get_one(self.db, id=id, with_movies=with_movies)
            if with_movies and isinstance(result, Sequence):
                genre = GenreExtended.model_validate(result[0][0])
                genre.movies = [MovieInDB.model_validate(movie) for movie in result[0][1]] if result[0][1] else []
                return genre
            return GenreInDB.model_validate(result)
        except Exception as e:
            error_detail = f"An error occurred while fetching genre. {e}" if result else f"Genre with id {id} not found."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)

    async def get_genre_by_name(self, name: str, with_movies: bool = False) -> GenreInDB | GenreExtended:
        result = None
        try:
            result = await self.crud.get_one(self.db, name=name, with_movies=with_movies)
            if with_movies and isinstance(result, Sequence):
                genre = GenreExtended.model_validate(result[0][0])
                genre.movies = [MovieInDB.model_validate(movie) for movie in result[0][1]] if result[0][1] else []
                return genre
            return GenreInDB.model_validate(result)
        except Exception as e:
            error_detail = f"An error occurred while fetching genre. {e}" if result else f"Genre with name {name} not found."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=error_detail)

    async def create_genre(self, genre_data: GenreCreate) -> GenreInDB:
        try:
            result = await self.crud.create(self.db, name=genre_data.name)
            return GenreInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while creating a genre."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def update_genre(self, genre_data: GenreUpdate) -> GenreInDB:
        try:
            result = await self.crud.update(self.db, genre_data=genre_data)
            return GenreInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while updating a genre."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

    async def remove_genre(self, id: UUID) -> GenreInDB:
        try:
            result = await self.crud.delete(self.db, id=id)
            return GenreInDB.model_validate(result)
        except Exception as e:
            error_detail = "An error occurred while removing a genre."
            logger.error(f"{error_detail} - details: {e}", exc_info=e)
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
