from enum import Enum

from strawberry import ID, auto, enum, experimental, input, type

from app.graphql.modules.base_type import StrawberryPydanticType
from app.rest.schemas.movies import MovieInDirector


@enum
class MovieOrder(Enum):
    title = "title"
    year = "year"


@enum
class MovieSort(Enum):
    asc = "asc"
    desc = "desc"


@type
class MovieBase:
    title: str
    year: int | None = None


@type
class MovieType(MovieBase):
    uuid: ID


@type
class MovieExtendedType(MovieType):
    director: str | None = None
    genre: str | None = None


@experimental.pydantic.type(model=MovieInDirector)
class MovieInDirectorType(StrawberryPydanticType):
    uuid: auto
    title: auto
    release_year: auto


@input
class MovieCreateInput:
    title: str
    release_year: int | None = None
    director_id: ID | None = None
    genre: str | None = None


@input
class MovieUpdateInput:
    uuid: ID
    title: str | None = None
    release_year: int | None = None
    director_id: ID | None = None
