from typing import Type, TypeVar

from pydantic import BaseModel
from strawberry import type as strawberry_type

T = TypeVar("T", bound="StrawberryPydanticType")
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


@strawberry_type
class StatusResponse:
    success: bool
    message: str


class StrawberryPydanticType:
    @classmethod
    def from_pydantic(
        cls: Type[T],
        model: PydanticModel,
        extra: dict | None = None,
    ) -> T:
        raise NotImplementedError
