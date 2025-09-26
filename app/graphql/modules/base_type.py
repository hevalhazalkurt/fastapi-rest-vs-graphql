from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound="StrawberryPydanticType")
PydanticModel = TypeVar("PydanticModel", bound=BaseModel)


class StrawberryPydanticType:
    @classmethod
    def from_pydantic(
        cls: Type[T],
        model: PydanticModel,
        extra: dict | None = None,
    ) -> T:
        raise NotImplementedError
