from fastapi import APIRouter
from sqlalchemy import text

from task.utils.dependencies import SessionDependency


healthcheck_router = APIRouter(prefix="/healthcheck", tags=["healthcheck"])


@healthcheck_router.get("/healthcheck-db", tags=["healthcheck"])
async def healthcheck_db(session: SessionDependency):
    try:
        result = await session.execute(statement=text("SELECT VERSION()"))
        return {
            "status": "success",
            "version": result.scalar(),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
