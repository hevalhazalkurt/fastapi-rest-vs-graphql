from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base_schema import ResponseSchema
from app.schemas.movies import MovieInDB


class DirectorCreate(ResponseSchema):
    name: str


class DirectorInDB(DirectorCreate):
    uuid: UUID

    model_config = ConfigDict(from_attributes=True)


class DirectorExtended(DirectorInDB):
    movies: list[MovieInDB] | None = []

    model_config = ConfigDict(from_attributes=True)


class DirectorUpdate(ResponseSchema):
    uuid: UUID
    name: str
