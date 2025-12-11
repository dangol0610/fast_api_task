import json
from fastapi import HTTPException, status
import httpx
from redis import Redis


class APIService:
    @classmethod
    async def get_posts(
        cls, client: httpx.AsyncClient, redis: Redis, ttl_cache: int = 300
    ):
        cache_key = "posts"
        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not get data from API",
            )
        data = response.json()
        await redis.set(cache_key, json.dumps(data), ex=ttl_cache)
        return data
