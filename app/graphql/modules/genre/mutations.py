from uuid import UUID

from strawberry import ID, Info, mutation, type

from app.graphql.modules.base_type import StatusResponse
from app.graphql.modules.genre.types import GenreCreateInput, GenreType, GenreUpdateInput
from app.rest.schemas.genres import GenreCreate, GenreUpdate
from app.rest.services.genres import GenresService


@type
class GenreMutation:
    @mutation
    async def create_genre(self, info: Info, genre_input: GenreCreateInput) -> GenreType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: GenresService = info.context.genre_service

        pydantic_data = GenreCreate.model_validate(genre_input)
        new_genre = await service.create_genre(pydantic_data)

        return GenreType.from_pydantic(new_genre)

    @mutation
    async def update_genre(self, info: Info, genre_input: GenreUpdateInput) -> GenreType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: GenresService = info.context.genre_service

        pydantic_data = GenreUpdate.model_validate(genre_input)
        updated_genre = await service.update_genre(pydantic_data)

        return GenreType.from_pydantic(updated_genre)

    @mutation
    async def delete_genre(self, info: Info, id: ID) -> StatusResponse:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: GenresService = info.context.genre_service

        try:
            deleted_genre = await service.remove_genre(id=UUID(id))
            if deleted_genre:
                return StatusResponse(success=True, message=f"Genre {deleted_genre.name} deleted successfully.")
            return StatusResponse(success=False, message="Genre could not be deleted.")
        except Exception as e:
            return StatusResponse(success=False, message=str(e))
