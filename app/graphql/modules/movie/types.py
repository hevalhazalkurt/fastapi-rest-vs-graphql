from enum import Enum

from strawberry import Info, auto, enum, experimental, field

from app.graphql.modules.base_type import StrawberryPydanticType
from app.rest.schemas.movies import MovieCreate, MovieExtended, MovieInDB, MovieInDirector, MovieUpdate


@enum
class MovieOrderEnum(Enum):
    title = "title"
    year = "year"


@enum
class MovieSortEnum(Enum):
    asc = "asc"
    desc = "desc"


@experimental.pydantic.type(model=MovieCreate)
class MovieBase:
    title: auto
    release_year: auto
    director_id: auto
    genre: auto


@experimental.pydantic.type(model=MovieInDB)
class MovieType(StrawberryPydanticType):
    uuid: auto
    title: auto
    release_year: auto
    director_id: auto


@experimental.pydantic.type(model=MovieExtended)
class MovieExtendedType(StrawberryPydanticType):
    uuid: auto
    title: auto
    release_year: auto
    director_id: auto

    @field
    async def director(self, info: Info) -> str | None:
        loader = info.context.movie_detail_loader
        details = await loader.load(self.uuid)
        return details.get("director")

    @field
    async def genre(self, info: Info) -> str | None:
        loader = info.context.movie_detail_loader
        details = await loader.load(self.uuid)
        return details.get("genre")


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


@experimental.pydantic.input(model=MovieCreate)
class MovieCreateInput:
    title: auto
    release_year: auto
    director_id: auto
    genre: auto


@experimental.pydantic.input(model=MovieUpdate)
class MovieUpdateInput:
    id: auto
    title: auto
    release_year: auto
    director_id: auto
    genre: auto
