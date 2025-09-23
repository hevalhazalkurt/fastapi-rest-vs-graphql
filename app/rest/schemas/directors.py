from uuid import UUID

from pydantic import ConfigDict

from app.rest.schemas.base_schema import ResponseSchema
from app.rest.schemas.movies import MovieInDirector


class DirectorCreate(ResponseSchema):
    name: str


class DirectorInDB(DirectorCreate):
    uuid: UUID

    model_config = ConfigDict(from_attributes=True)


class DirectorExtended(DirectorInDB):
    movies: list[MovieInDirector] | None = []

    model_config = ConfigDict(from_attributes=True)


class DirectorUpdate(ResponseSchema):
    uuid: UUID
    name: str
