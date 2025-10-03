from pydantic import UUID4
from strawberry import ID, Info, field, type

from app.graphql.modules.movie.types import MovieExtendedType, MovieOrderEnum, MovieSortEnum
from app.rest.schemas.movies import MovieOrder, MovieSort
from app.rest.services.movies import MovieService


@type
class MovieQuery:
    @field
    async def movies(
        self,
        info: Info,
        skip: int = 0,
        limit: int = 100,
        order_by: MovieOrderEnum = MovieOrderEnum.title,
        sort_by: MovieSortEnum = MovieSortEnum.asc,
    ) -> list[MovieExtendedType]:
        if not info.context.current_user:
            raise Exception("Not authenticated!")

        service: MovieService = info.context.movie_service

        movie_data = await service.get_all_movies(skip=skip, limit=limit, order_by=MovieOrder(order_by.value), sort_by=MovieSort(sort_by.value), extended=False)

        return [MovieExtendedType.from_pydantic(d) for d in movie_data]

    @field
    async def movie(self, info: Info, id: ID) -> MovieExtendedType:
        if not info.context.current_user:
            raise Exception("Not authenticated!")

        service: MovieService = info.context.movie_service

        movie_data = await service.get_movie_by_id(id=UUID4(id), extended=False)
        return MovieExtendedType.from_pydantic(movie_data)
