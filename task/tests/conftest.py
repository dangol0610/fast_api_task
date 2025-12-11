from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from task.apps.auth.dependencies import get_current_user
from task.settings.settings import settings
from task.utils.database import Base, get_session
from task.main import app
from task.utils.dependencies import httpx_client


@pytest_asyncio.fixture(scope="function")
async def setup_db():
    test_engine = create_async_engine(url=settings.db_url)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(bind=test_engine, expire_on_commit=False)
    async with Session() as session:
        yield session
        await session.rollback()
    await test_engine.dispose()

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()


@pytest.fixture
def fake_current_user():
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "hashed_password": "fakehashedsecret",
    }


@pytest.fixture
def fake_session():
    return AsyncMock()


@pytest.fixture
def client(fake_current_user, fake_session):
    async def override_current_user():
        return fake_current_user

    async def override_session():
        return fake_session

    async def override_httpx_client():
        yield None

    app.dependency_overrides[get_current_user] = override_current_user
    app.dependency_overrides[get_session] = override_session
    app.dependency_overrides[httpx_client] = override_httpx_client

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
