import uuid
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.utils import get_all, get_all_scalars, scalar
from app.models import Genre, Movie, MovieGenreAssociation
from app.rest.repository.base_repo import AbstractCRUD
from app.rest.schemas.genres import GenreUpdate


class GenreCRUD(AbstractCRUD):
    async def get_one(self, db: AsyncSession, id: UUID | None = None, name: str | None = None, with_movies: bool = False) -> Genre | Sequence[Row[Any]] | None:
        filter = Genre.uuid == id if id else Genre.name == name
        if with_movies:
            base_query = (
                select(
                    Genre,
                    func.coalesce(
                        func.array_agg(
                            func.json_build_object(
                                "uuid",
                                Movie.uuid,
                                "title",
                                Movie.title,
                                "release_year",
                                Movie.release_year,
                                "director_id",
                                Movie.director_id,
                            )
                        ),
                        None,
                    ).label("movies"),
                )
                .outerjoin(MovieGenreAssociation, MovieGenreAssociation.genre_id == Genre.uuid)
                .outerjoin(Movie, Movie.uuid == MovieGenreAssociation.movie_id)
                .where(filter)
                .group_by(Genre.uuid)
            )
            return await get_all(db, base_query)
        return await scalar(db, select(Genre).where(filter))

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 20) -> Sequence[Genre] | Sequence[Row[Any]]:
        return await get_all_scalars(db, select(Genre).order_by(Genre.name).offset(skip).limit(limit))

    async def create(self, db: AsyncSession, name: str) -> Genre:
        existing_genre = await self.get_one(db, name=name)
        if not existing_genre:
            new_genre = Genre(name=name, uuid=uuid.uuid4())
            db.add(new_genre)
            await db.flush()
            return new_genre
        return existing_genre  # type: ignore

    async def update(self, db: AsyncSession, genre_data: GenreUpdate) -> Genre | Sequence[Row[Any]] | None:
        genre = await self.get_one(db, id=genre_data.uuid)
        if genre and isinstance(genre, Genre):
            genre.name = genre_data.name
            db.add(genre)
            await db.flush()
        return genre

    async def delete(self, db: AsyncSession, id: UUID) -> Genre | Sequence[Row[Any]] | None:
        genre = await self.get_one(db, id=id)
        await db.delete(genre)
        return genre


def get_genre_crud() -> GenreCRUD:
    return GenreCRUD()
