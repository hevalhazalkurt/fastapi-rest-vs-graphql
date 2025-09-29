from uuid import UUID

from strawberry import ID, Info, field, type

from app.graphql.modules.genre.types import GenreType
from app.rest.services.genres import GenresService


@type
class GenreQuery:
    @field
    async def genre(self, id: ID, info: Info) -> GenreType | None:
        service: GenresService = info.context.genre_service

        genre_data = await service.get_genre_by_id(id=UUID(id))

        if not genre_data:
            return None

        return GenreType.from_pydantic(genre_data)

    @field
    async def genres(
        self,
        info: Info,
        skip: int = 0,
        limit: int = 100,
    ) -> list[GenreType] | None:
        service: GenresService = info.context.genre_service

        genres_data = await service.get_all_genres(skip=skip, limit=limit)

        return [GenreType.from_pydantic(g) for g in genres_data]
