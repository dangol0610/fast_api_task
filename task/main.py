from fastapi import FastAPI
from task.apps.auth.middleware import auth_middleware
from task.routers.api_router import api_router


app = FastAPI()
app.middleware("http")(auth_middleware)
app.include_router(api_router)
