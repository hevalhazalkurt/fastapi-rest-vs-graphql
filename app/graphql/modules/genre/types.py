from strawberry import Info, auto, experimental, field

from app.graphql.modules.base_type import StrawberryPydanticType
from app.graphql.modules.movie.types import MovieInGenreType
from app.rest.schemas.genres import GenreCreate, GenreExtended, GenreInDB, GenreUpdate


@experimental.pydantic.type(model=GenreCreate)
class GenreBase:
    name: auto


@experimental.pydantic.type(model=GenreInDB)
class GenreType(StrawberryPydanticType):
    uuid: auto
    name: auto

    @field
    async def movies(
        self,
        info: Info,
    ) -> list[MovieInGenreType] | None:
        loader = info.context.genre_movies_loader
        movies_list = await loader.load(self.uuid)
        return [MovieInGenreType.from_pydantic(m) for m in movies_list]


@experimental.pydantic.type(model=GenreExtended)
class GenreExtendedType:
    uuid: auto
    name: auto
    movies: auto


@experimental.pydantic.input(model=GenreCreate)
class GenreCreateInput:
    name: auto


@experimental.pydantic.input(model=GenreUpdate)
class GenreUpdateInput:
    uuid: auto
    name: auto
