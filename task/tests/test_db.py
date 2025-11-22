import pytest_asyncio
from sqlalchemy import NullPool
from task.settings.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


@pytest_asyncio.fixture
async def setup_db():
    assert settings.DB_NAME == "test_alchemytask_db"
    assert settings.TESTING is True

    engine = create_async_engine(url=settings.db_url, poolclass=NullPool)

    test_session = async_sessionmaker(bind=engine, expire_on_commit=False)

    yield test_session
    await engine.dispose()
