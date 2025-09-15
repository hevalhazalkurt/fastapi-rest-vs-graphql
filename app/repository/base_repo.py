import abc
from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractCRUD(abc.ABC):
    @abc.abstractmethod
    async def get_one(self, db: AsyncSession, *args) -> Any:
        pass

    @abc.abstractmethod
    async def get_all(self, db: AsyncSession, *args, **kwargs) -> Sequence[Any]:
        pass

    @abc.abstractmethod
    async def create(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass

    @abc.abstractmethod
    async def update(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass

    @abc.abstractmethod
    async def delete(self, db: AsyncSession, *args, **kwargs) -> Any:
        pass
