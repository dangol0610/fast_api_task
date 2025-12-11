from fastapi import APIRouter
from task.apps.users.routers import user_router
from task.apps.auth.routers import auth_router
from task.apps.project.routers import project_router
from task.apps.api_integration.routers import integration_router
from task.utils.healthcheck import healthcheck_router

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(project_router)
api_router.include_router(integration_router)
api_router.include_router(healthcheck_router)
