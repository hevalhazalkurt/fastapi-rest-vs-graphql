from uuid import UUID

from strawberry import ID, Info, mutation, type

from app.graphql.modules.base_type import StatusResponse
from app.graphql.modules.movie.types import MovieCreateInput, MovieType, MovieUpdateInput
from app.rest.schemas.movies import MovieCreate, MovieUpdate
from app.rest.services.movies import MovieService


@type
class MovieMutation:
    @mutation
    async def create_movie(self, info: Info, movie_input: MovieCreateInput) -> MovieType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: MovieService = info.context.movie_service

        pydantic_data = MovieCreate.model_validate(movie_input)
        new_movie = await service.create_movie(pydantic_data)
        return MovieType.from_pydantic(new_movie)

    @mutation
    async def update_movie(self, info: Info, movie_input: MovieUpdateInput) -> MovieType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: MovieService = info.context.movie_service
        pydantic_data = MovieUpdate.model_validate(movie_input)
        updated_movie = await service.update_movie(pydantic_data)
        return MovieType.from_pydantic(updated_movie)

    @mutation
    async def delete_movie(self, info: Info, id: ID) -> StatusResponse:
        if not info.context.current_user:
            raise Exception("Not authenticated!")
        elif "admin" not in info.context.current_user.get("scopes", []):
            raise Exception("Not authorized!")

        service: MovieService = info.context.movie_service

        try:
            deleted_movie = await service.remove_movie(id=UUID(id))
            if deleted_movie:
                return StatusResponse(success=True, message=f"Movie {deleted_movie.title} deleted successfully.")
            return StatusResponse(success=False, message="Movie could not be deleted.")
        except Exception as e:
            return StatusResponse(success=False, message=str(e))
