import abc
from typing import Sequence, Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractCRUD(abc.ABC):
    @abc.abstractmethod
    async def get_one(self, db: AsyncSession, id: UUID) -> Any:
        pass


    @abc.abstractmethod
    async def get_all(self, db: AsyncSession) -> Sequence[Any]:
        pass


    @abc.abstractmethod
    async def create(self, db: AsyncSession) -> Any:
        pass


    @abc.abstractmethod
    async def update(self, db: AsyncSession, id: UUID) -> Any:
        pass


    @abc.abstractmethod
    async def delete(self, db: AsyncSession, id: UUID) -> Any:
        pass