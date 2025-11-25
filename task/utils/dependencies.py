from typing import Annotated
from fastapi import Depends
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from task.utils.database import get_session


SessionDependency = Annotated[AsyncSession, Depends(get_session)]


async def httpx_client():
    async with httpx.AsyncClient() as client:
        yield client
