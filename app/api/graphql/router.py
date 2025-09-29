from uuid import UUID

import strawberry
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import field
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext, GraphQLRouter

from app.db.session import get_db
from app.graphql.modules.director.mutations import DirectorMutation
from app.graphql.modules.director.queries import DirectorQuery
from app.graphql.modules.genre.mutations import GenreMutation
from app.graphql.modules.genre.queries import GenreQuery
from app.rest.schemas.movies import MovieInDB, MovieInDirector
from app.rest.services.directors import DirectorsService
from app.rest.services.genres import GenresService


class Context(BaseContext):
    def __init__(self, db: AsyncSession, director_service: DirectorsService, genre_service: GenresService):
        super().__init__()
        self.db = db
        self.director_service = director_service
        self.director_movies_loader = DataLoader(load_fn=self._load_movies_for_directors)

        self.genre_service = genre_service
        self.genre_movies_loader = DataLoader(load_fn=self._load_movies_for_genres)

    async def _load_movies_for_directors(self, director_ids: list[UUID]) -> list[list[MovieInDirector]]:
        movies_map: dict = await self.director_service.get_director_movies(director_ids)
        return [movies_map.get(director_id, []) for director_id in director_ids]

    async def _load_movies_for_genres(self, genre_ids: list[UUID]) -> list[list[MovieInDB]]:
        movies_map: dict = await self.genre_service.get_genre_movies(genre_ids)
        return [movies_map.get(genre_id, []) for genre_id in genre_ids]


async def get_graphql_context(
    db: AsyncSession = Depends(get_db),
    director_service: DirectorsService = Depends(DirectorsService),
    genre_service: GenresService = Depends(GenresService),
) -> Context:
    return Context(db=db, director_service=director_service, genre_service=genre_service)


@strawberry.type
class Query(DirectorQuery, GenreQuery):
    @field
    def hello(self) -> str:
        return "Hello GraphQL!"


@strawberry.type
class Mutation(DirectorMutation, GenreMutation):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_graphql_context,  # type: ignore
    graphiql=True,
)
