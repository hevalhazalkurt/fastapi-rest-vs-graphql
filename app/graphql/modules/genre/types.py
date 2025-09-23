from typing import TYPE_CHECKING

from strawberry import ID, input, type

if TYPE_CHECKING:
    from app.graphql.modules.movie.types import MovieType


@type
class GenreBase:
    name: str


@type
class GenreType(GenreBase):
    uuid: ID


@type
class GenreExtendedType(GenreType):
    movies: list[MovieType] | None = []


@input
class GenreCreateInput:
    name: str


@input
class GenreUpdateInput:
    uuid: ID
    name: str
