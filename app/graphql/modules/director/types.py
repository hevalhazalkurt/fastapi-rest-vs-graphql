from strawberry import experimental, Info, field

from app.graphql.modules.movie.types import MovieInDirectorType
from app.rest.schemas.directors import DirectorCreate, DirectorInDB, DirectorExtended, DirectorUpdate


@experimental.pydantic.type(model=DirectorCreate, all_fields=True)
class DirectorBase:
    pass


@experimental.pydantic.type(model=DirectorInDB, all_fields=True)
class DirectorType:
    @field
    async def movies(
            self,
            info: Info,
    ) -> list[MovieInDirectorType] | None:
        loader = info.context.director_movies_loader
        movies_list = await loader.load(self.uuid)
        return [MovieInDirectorType.from_pydantic(m) for m in movies_list]


@experimental.pydantic.type(model=DirectorExtended, all_fields=True)
class DirectorExtendedType:
    pass


@experimental.pydantic.input(model=DirectorCreate, all_fields=True)
class DirectorCreateInput:
    pass


@experimental.pydantic.input(model=DirectorUpdate, all_fields=True)
class DirectorUpdateInput:
    pass
