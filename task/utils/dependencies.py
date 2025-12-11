from typing import Annotated
from fastapi import Depends
from redis.asyncio import Redis
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from task.settings.settings import settings
from task.utils.database import get_session


redis_client: Redis = Redis.from_url(
    url=settings.redis_cache_url,
    decode_responses=True,
)


async def httpx_client():
    async with httpx.AsyncClient() as client:
        yield client


async def get_redis():
    try:
        yield redis_client
    finally:
        pass


SessionDependency = Annotated[AsyncSession, Depends(get_session)]
RedisDependency = Annotated[Redis, Depends(get_redis)]
HttpClientDependency = Annotated[httpx.AsyncClient, Depends(httpx_client)]
