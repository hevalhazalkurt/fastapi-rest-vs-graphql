from typing import TYPE_CHECKING

from strawberry import ID, input, type

if TYPE_CHECKING:
    from app.graphql.modules.movie.types import MovieType


@type
class DirectorBase:
    name: str


@type
class DirectorType(DirectorBase):
    uuid: ID


@type
class DirectorExtendedType(DirectorType):
    movies: list[MovieType] | None = []


@input
class DirectorCreateInput:
    name: str


@input
class DirectorUpdateInput:
    uuid: ID
    name: str
