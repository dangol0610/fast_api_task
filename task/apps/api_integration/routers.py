from fastapi import APIRouter

from task.apps.api_integration.service import APIService
from task.utils.dependencies import HttpClientDependency, RedisDependency


integration_router = APIRouter(prefix="/other", tags=["Other API"])


@integration_router.get("/posts")
async def get_posts(client: HttpClientDependency, redis: RedisDependency):
    """
    Делает запрос к внешнему API 'https://jsonplaceholder.typicode.com/posts' и возвращает список постов.
    """
    return await APIService.get_posts(client=client, redis=redis)
