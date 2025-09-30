from enum import Enum
from uuid import UUID

from pydantic import ConfigDict

from app.rest.schemas.base_schema import ResponseSchema


class MovieOrder(Enum):
    title = "title"
    year = "year"


class MovieSort(Enum):
    asc = "asc"
    desc = "desc"


class MovieCreate(ResponseSchema):
    title: str
    release_year: int | None = None
    director_id: UUID | None = None
    genre: str | None = None


class MovieInDB(ResponseSchema):
    uuid: UUID
    title: str
    release_year: int | None = None
    director_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class MovieInDirector(ResponseSchema):
    uuid: UUID
    title: str
    release_year: int | None = None


class MovieExtended(MovieInDB):
    director: str | None = None
    genre: str | None = None

    model_config = ConfigDict(from_attributes=True)


class MovieUpdate(ResponseSchema):
    id: UUID
    title: str | None = None
    release_year: int | None = None
    director_id: UUID | None = None
    genre: str | None = None
