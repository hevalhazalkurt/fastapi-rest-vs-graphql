from uuid import UUID

from strawberry import ID, Info, mutation, type

from app.graphql.modules.base_type import StatusResponse
from app.graphql.modules.director.types import DirectorCreateInput, DirectorType, DirectorUpdateInput
from app.rest.schemas.directors import DirectorCreate, DirectorUpdate
from app.rest.services.directors import DirectorsService


@type
class DirectorMutation:
    @mutation
    async def create_director(
        self,
        director_input: DirectorCreateInput,
        info: Info,
    ) -> DirectorType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: DirectorsService = info.context.director_service

        pydantic_data = DirectorCreate.model_validate(director_input)
        new_director = await service.create_director(pydantic_data)

        return DirectorType.from_pydantic(new_director)

    @mutation
    async def update_director(
        self,
        director_input: DirectorUpdateInput,
        info: Info,
    ) -> DirectorType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: DirectorsService = info.context.director_service
        pydantic_data = DirectorUpdate.model_validate(director_input)
        updated_director = await service.update_director(director_data=pydantic_data)

        return DirectorType.from_pydantic(updated_director)

    @mutation
    async def delete_director(
        self,
        id: ID,
        info: Info,
    ) -> StatusResponse:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: DirectorsService = info.context.director_service

        try:
            deleted_director = await service.remove_director(id=UUID(id))
            if deleted_director:
                return StatusResponse(success=True, message=f"Director {deleted_director.name} deleted successfully.")
            return StatusResponse(success=False, message="Director could not be deleted.")
        except Exception as e:
            return StatusResponse(success=False, message=str(e))
