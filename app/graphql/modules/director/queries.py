from strawberry import type, field, Info, ID

from app.graphql.modules.director.types import DirectorType
from app.rest.services.directors import DirectorsService


@type
class DirectorQuery:
    @field
    async def director(
            self,
            id: ID,
            info: Info
    ) -> DirectorType | None:
        service: DirectorsService = info.context.director_service

        director_data = await service.get_director_by_id(id=id, with_movies=True)

        if not director_data:
            return None

        return DirectorType.from_pydantic(director_data)


    @field
    async def directors(
            self,
            info: Info,
            skip: int = 0,
            limit: int = 100,
    ) -> list[DirectorType]:
        service: DirectorsService = info.context.director_service

        directors_data = await service.get_all_directors(skip=skip, limit=limit, with_movies=False)

        return [DirectorType.from_pydantic(d) for d in directors_data]

