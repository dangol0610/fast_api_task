from fastapi import Depends, FastAPI
from sqlalchemy import text
from task.apps.auth.middleware import auth_middleware
from task.routers.api_router import api_router
from task.utils.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()
app.middleware("http")(auth_middleware)
app.include_router(api_router)


@app.get("/healthcheck-db", tags=["healthcheck"])
async def healthcheck_db(session: AsyncSession = Depends(get_session)):
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
