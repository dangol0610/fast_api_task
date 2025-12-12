import json
import httpx
from redis import Redis

from task.utils.exceptions import ApiIntegrationException


class APIService:
    @classmethod
    async def get_posts(
        cls, client: httpx.AsyncClient, redis: Redis, ttl_cache: int = 300
    ):
        cache_key = "posts"
        cached_data = await redis.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        try:
            response = await client.get("https://jsonplaceholder.typicode.com/posts")
        except Exception:
            raise ApiIntegrationException
        data = response.json()
        await redis.set(cache_key, json.dumps(data), ex=ttl_cache)
        return data
