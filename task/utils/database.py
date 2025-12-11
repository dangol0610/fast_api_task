from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from task.settings.settings import settings

engine = create_async_engine(url=settings.db_url, echo=True)

local_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with local_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
