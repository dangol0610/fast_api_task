from fastapi import APIRouter, Depends
import httpx

from task.apps.api_integration.service import APIService
from task.utils.dependencies import httpx_client


integration_router = APIRouter(prefix="/other", tags=["Other API"])


@integration_router.get("/posts")
async def get_posts(client: httpx.AsyncClient = Depends(httpx_client)):
    return await APIService.get_posts(client=client)
