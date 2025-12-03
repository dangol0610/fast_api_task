from contextlib import asynccontextmanager
from fastapi import FastAPI
from task.apps.auth.middleware import auth_middleware
from task.routers.api_router import api_router
from task.utils.dependencies import redis_client
from redis.exceptions import RedisError
from task.utils.database import engine
from sqlalchemy import text

from task.utils.rate_limiter import rate_limiter_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await redis_client.ping()
    except Exception:
        raise RedisError("Redis connection failed")
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        raise ConnectionError("Database connection failed")

    app.state.redis = redis_client

    yield

    await redis_client.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)
app.middleware("http")(auth_middleware)
app.middleware("http")(rate_limiter_middleware)
app.include_router(api_router)
