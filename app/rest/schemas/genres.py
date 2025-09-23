from uuid import UUID

from app.rest.schemas.base_schema import ResponseSchema
from app.rest.schemas.movies import MovieInDB


class GenreCreate(ResponseSchema):
    name: str


class GenreInDB(GenreCreate):
    uuid: UUID


class GenreExtended(GenreInDB):
    movies: list[MovieInDB] | None = []


class GenreUpdate(ResponseSchema):
    uuid: UUID
    name: str
