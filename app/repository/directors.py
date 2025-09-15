import uuid
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import Row, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.utils import get_all, get_all_scalars, scalar
from app.models import Director, Movie
from app.repository.base_repo import AbstractCRUD
from app.schemas.directors import DirectorUpdate


class DirectorCRUD(AbstractCRUD):
    async def get_one(self, db: AsyncSession, id: UUID | None = None, name: str | None = None, with_movies: bool = False):
        filter = Director.uuid == id if id else Director.name == name
        if with_movies:
            base_query = (
                select(
                    Director,
                    func.coalesce(
                        func.array_agg(func.json_build_object("uuid", Movie.uuid, "title", Movie.title, "release_year", Movie.release_year)).filter(Movie.uuid.is_not(None)),
                        None,
                    ).label("movies"),
                )
                .outerjoin(Movie, Movie.director_id == Director.uuid)
                .where(filter)
                .group_by(Director.uuid)
            )
            return await get_all(db, base_query)
        return await scalar(db, select(Director).where(filter))

    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 20, with_movies: bool = False) -> Sequence[Director] | Sequence[Row[Any]]:
        if with_movies:
            base_query = (
                select(
                    Director,
                    func.coalesce(
                        func.array_agg(func.json_build_object("uuid", Movie.uuid, "title", Movie.title, "release_year", Movie.release_year)).filter(Movie.uuid.is_not(None)),
                        None,
                    ),
                )
                .outerjoin(Movie, Movie.director_id == Director.uuid)
                .group_by(Director.uuid)
                .order_by(Director.name)
                .offset(skip)
                .limit(limit)
            )
            return await get_all(db, base_query)

        return await get_all_scalars(db, select(Director).order_by(Director.name).offset(skip).limit(limit))

    async def create(self, db: AsyncSession, name: str) -> Director:
        new_director = Director(name=name, uuid=uuid.uuid4())
        db.add(new_director)
        await db.flush()
        return new_director

    async def update(self, db: AsyncSession, director_data: DirectorUpdate) -> Director:
        director = await self.get_one(db, id=director_data.uuid)
        director.name = director_data.name
        db.add(director)
        await db.flush()
        return director

    async def delete(self, db: AsyncSession, id: UUID) -> Director:
        director = await self.get_one(db, id=id)
        await db.delete(director)
        return director


def get_director_crud() -> DirectorCRUD:
    return DirectorCRUD()
