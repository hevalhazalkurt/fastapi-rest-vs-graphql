from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base_schema import ResponseSchema
from app.schemas.movies import MovieInDB


class DirectorInDB(ResponseSchema):
    uuid: UUID
    name: str


class DirectorExtended(DirectorInDB):
    movies: list[MovieInDB] | None = []

    model_config = ConfigDict(from_attributes=True)