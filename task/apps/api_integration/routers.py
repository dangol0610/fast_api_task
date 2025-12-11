from fastapi import APIRouter

from task.apps.api_integration.service import APIService
from task.utils.dependencies import HttpClientDependency, RedisDependency


integration_router = APIRouter(prefix="/other", tags=["Other API"])


@integration_router.get("/posts")
async def get_posts(client: HttpClientDependency, redis: RedisDependency):
    return await APIService.get_posts(client=client, redis=redis)
