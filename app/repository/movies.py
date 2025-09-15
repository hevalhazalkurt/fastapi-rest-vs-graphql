from typing import Any, Sequence

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.utils import get_all, get_all_scalars
from app.models import Director, Genre, Movie, MovieGenreAssociation
from app.repository.base_repo import AbstractCRUD
from app.schemas.movies import MovieOrder, MovieSort


class MovieCRUD(AbstractCRUD):
    async def get_one(self, db: AsyncSession, *args) -> Any:
        pass

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 20, order_by: MovieOrder = MovieOrder.title, sort_by: MovieSort = MovieSort.asc, extended: bool = False
    ) -> Sequence[Movie] | Sequence[Row[Any]]:
        order_expression = Movie.release_year if order_by == MovieOrder.year else Movie.title
        sort_expression = order_expression.desc() if sort_by == MovieSort.desc else order_expression.asc()
        if extended:
            base_query = (
                select(
                    Movie,
                    Director.name,
                    func.coalesce(
                        func.array_agg(Genre.name).filter(Genre.uuid.is_not(None)),
                        None,
                    ).label("genres"),
                )
                .outerjoin(Director, Director.uuid == Movie.director_id)
                .outerjoin(MovieGenreAssociation, MovieGenreAssociation.movie_id == Movie.uuid)
                .outerjoin(Genre, Genre.uuid == MovieGenreAssociation.genre_id)
                .group_by(Movie.uuid, Movie.title, Movie.release_year, Director.name)
                .order_by(sort_expression)
                .offset(skip)
                .limit(limit)
            )
            return await get_all(db, base_query)

        return await get_all_scalars(db, select(Movie).order_by(sort_expression).offset(skip).limit(limit))

    async def create(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass

    async def update(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass

    async def delete(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass


def get_movie_crud() -> MovieCRUD:
    return MovieCRUD()
