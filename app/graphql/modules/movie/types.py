from enum import Enum

from strawberry import ID, auto, enum, experimental, input, type

from app.graphql.modules.base_type import StrawberryPydanticType
from app.rest.schemas.movies import MovieCreate, MovieInDB, MovieInDirector


@enum
class MovieOrder(Enum):
    title = "title"
    year = "year"


@enum
class MovieSort(Enum):
    asc = "asc"
    desc = "desc"


@experimental.pydantic.type(model=MovieCreate)
class MovieBase:
    title: auto
    release_year: auto
    director_id: auto
    genre: auto


@experimental.pydantic.type(model=MovieInDB)
class MovieType:
    uuid: auto


@type
class MovieExtendedType(MovieType):
    director: str | None = None
    genre: str | None = None


@experimental.pydantic.type(model=MovieInDirector)
class MovieInDirectorType(StrawberryPydanticType):
    uuid: auto
    title: auto
    release_year: auto


@experimental.pydantic.type(model=MovieInDB)
class MovieInGenreType(StrawberryPydanticType):
    uuid: auto
    title: auto
    release_year: auto
    director_id: auto


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
