from enum import Enum
from uuid import UUID

from pydantic import ConfigDict

from app.schemas.base_schema import ResponseSchema


class MovieOrder(Enum):
    title = "title"
    year = "year"


class MovieSort(Enum):
    asc = "asc"
    desc = "desc"


class MovieInDB(ResponseSchema):
    uuid: UUID
    title: str
    release_year: int

    model_config = ConfigDict(from_attributes=True)


class MovieExtended(MovieInDB):
    director: str | None = None
    genre: str | None = None

    model_config = ConfigDict(from_attributes=True)
