from uuid import UUID

import strawberry
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry import field
from strawberry.dataloader import DataLoader
from strawberry.fastapi import GraphQLRouter, BaseContext

from app.db.session import get_db
from app.graphql.modules.director.queries import DirectorQuery
from app.rest.schemas.movies import MovieInDirector
from app.rest.services.directors import DirectorsService


class Context(BaseContext):
    def __init__(self, db: AsyncSession, director_service: DirectorsService):
        super().__init__()
        self.db = db
        self.director_service = director_service
        self.director_movies_loader = DataLoader(load_fn=self._load_movies_for_directors)

    async def _load_movies_for_directors(self, director_ids: list[UUID]) -> list[list[MovieInDirector]]:
        movies_map: dict = await self.director_service.get_director_movies(director_ids)
        return [movies_map.get(director_id, []) for director_id in director_ids]

async def get_graphql_context(
    db: AsyncSession = Depends(get_db),
    director_service: DirectorsService = Depends(DirectorsService),
) -> Context:
    return Context(db=db, director_service=director_service)


@strawberry.type
class Query(DirectorQuery):
    @field
    def hello(self) -> str:
        return "Hello GraphQL!"


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(
    schema,
    context_getter=get_graphql_context,
    graphiql=True
)
