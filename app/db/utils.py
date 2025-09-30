from typing import Any, Sequence

from sqlalchemy import Executable, Row
from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_scalars(db: AsyncSession, query: Executable) -> Sequence[Any]:
    return (await db.execute(query)).scalars().all()


async def get_all(db: AsyncSession, query: Executable) -> Sequence[Row[Any]]:
    return (await db.execute(query)).all()


async def scalar(db: AsyncSession, query: Executable) -> Any | None:
    return await db.scalar(query)


async def execute(db: AsyncSession, query: Executable, *args, **kwargs) -> Any | None:
    return await db.execute(query, *args, **kwargs)
