import uuid
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.utils import get_all, get_all_scalars, scalar
from app.models import Director, Genre, Movie, MovieGenreAssociation
from app.rest.repository.base_repo import AbstractCRUD
from app.rest.repository.directors import DirectorCRUD
from app.rest.schemas.movies import MovieCreate, MovieOrder, MovieSort, MovieUpdate


class MovieCRUD(AbstractCRUD):
    async def get_one(self, db: AsyncSession, id: UUID, extended: bool = False) -> Movie | Sequence[Row[Any]] | None:
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
                .where(Movie.uuid == id)
                .group_by(Movie.uuid, Movie.title, Movie.release_year, Director.name)
            )
            return await get_all(db, base_query)
        return await scalar(db, select(Movie).where(Movie.uuid == id))

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

    async def create(self, db: AsyncSession, movie_data: MovieCreate) -> Movie | None:
        director = await DirectorCRUD().get_one(db=db, id=movie_data.director_id)
        new_movie = Movie(title=movie_data.title, release_year=movie_data.release_year, uuid=uuid.uuid4(), director_id=movie_data.director_id if director else None)
        db.add(new_movie)
        await db.flush()
        return new_movie

    async def update(self, db: AsyncSession, movie_data: MovieUpdate) -> Movie | Sequence[Row[Any]] | None:
        movie = await self.get_one(db, id=movie_data.id)
        director = await DirectorCRUD().get_one(db=db, id=movie_data.director_id) if movie_data.director_id else None
        if movie and isinstance(movie, Movie):
            movie.title = movie_data.title if movie_data.title else movie.title
            movie.release_year = movie_data.release_year if movie_data.release_year else movie.release_year
            movie.director_id = movie_data.director_id if movie_data.director_id and director else movie.director_id  # type: ignore
            db.add(movie)
            await db.flush()
        return movie

    async def delete(self, db: AsyncSession, id: UUID) -> Movie | Sequence[Row[Any]] | None:
        movie = await self.get_one(db, id=id)
        await db.delete(movie)
        return movie


def get_movie_crud() -> MovieCRUD:
    return MovieCRUD()
