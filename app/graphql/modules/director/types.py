from strawberry import Info, auto, experimental, field

from app.graphql.modules.base_type import StrawberryPydanticType
from app.graphql.modules.movie.types import MovieInDirectorType
from app.rest.schemas.directors import DirectorCreate, DirectorExtended, DirectorInDB, DirectorUpdate


@experimental.pydantic.type(model=DirectorCreate)
class DirectorBase:
    name: auto


@experimental.pydantic.type(model=DirectorInDB)
class DirectorType(StrawberryPydanticType):
    uuid: auto
    name: auto

    @field
    async def movies(
        self,
        info: Info,
    ) -> list[MovieInDirectorType] | None:
        loader = info.context.director_movies_loader
        movies_list = await loader.load(self.uuid)
        return [MovieInDirectorType.from_pydantic(m) for m in movies_list]


@experimental.pydantic.type(model=DirectorExtended)
class DirectorExtendedType:
    uuid: auto
    name: auto
    movies: auto


@experimental.pydantic.input(model=DirectorCreate)
class DirectorCreateInput:
    name: auto


@experimental.pydantic.input(model=DirectorUpdate)
class DirectorUpdateInput:
    uuid: auto
    name: auto
