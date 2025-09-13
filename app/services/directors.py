from typing import Sequence
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND

from app.db.session import get_db
from app.repository.directors import DirectorCRUD, get_director_crud
from app.schemas.directors import DirectorInDB, DirectorExtended
from app.schemas.movies import MovieInDB


class DirectorsService:
    def __init__(self,
                 db: AsyncSession = Depends(get_db),
                 crud: DirectorCRUD = Depends(get_director_crud),):
        self.db = db
        self.crud = crud


    async def get_all_directors(self, skip: int = 0, limit: int = 20, with_movies: bool = False) -> Sequence[DirectorInDB | DirectorExtended]:
        try:
            results: Sequence = await self.crud.get_all(self.db, skip=skip, limit=limit, with_movies=with_movies)
            if with_movies:
                directors_with_movies: list[DirectorExtended] = []
                for director, movies in results:
                    director_resp = DirectorExtended.model_validate(director)
                    director_resp.movies = [MovieInDB.model_validate(movie) for movie in movies]
                    directors_with_movies.append(director_resp)
                return directors_with_movies
            return [DirectorInDB.model_validate(data) for data in results]
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while fetching directors. {e}"
            )


    async def get_director_by_id(self, id: UUID, with_movies: bool = False) -> DirectorInDB | DirectorExtended:
        try:
            result = await self.crud.get_one(self.db, id=id, with_movies=with_movies)
            if with_movies:
                director = DirectorExtended.model_validate(result[0][0])
                director.movies = [MovieInDB.model_validate(movie) for movie in result[0][1]]
                return director
            return DirectorInDB.model_validate(result)
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Could not fetch a director by id {id}. {e}"
            )


    async def get_director_by_name(self, name: str, with_movies: bool = False) -> DirectorInDB | DirectorExtended:
        try:
            result = await self.crud.get_one(self.db, name=name, with_movies=with_movies)
            if with_movies:
                director = DirectorExtended.model_validate(result[0][0])
                director.movies = [MovieInDB.model_validate(movie) for movie in result[0][1]]
                return director
            return DirectorInDB.model_validate(result)
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Could not fetch a director by name {name}. {e}"
            )




