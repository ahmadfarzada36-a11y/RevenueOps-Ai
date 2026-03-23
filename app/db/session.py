from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine
)

from sqlalchemy.orm import sessionmaker

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL or (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@"
    f"{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/"
    f"{settings.POSTGRES_DB}"
)


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    future=True
)


AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():

    async with AsyncSessionLocal() as session:

        try:
            yield session
        finally:
            await session.close()