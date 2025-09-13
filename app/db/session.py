from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL or "",
    echo=settings.ECHO,
    pool_size=settings.POOL_SIZE,
    max_overflow=settings.MAX_OVERFLOW,
    pool_recycle=600,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


async def get_db() -> AsyncGenerator:
    """
    Dependency to get an async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        else:
            await session.commit()
        finally:
            await session.close()
