from fastapi import Body, FastAPI
from pydantic import EmailStr
from task.apps.auth.middleware import auth_middleware
from task.celery.tasks.tasks import send_email as send
from task.celery.celery_utils import celery_app
from task.routers.api_router import api_router


from task.utils.rate_limiter import rate_limiter_middleware


app = FastAPI()
app.middleware("http")(auth_middleware)
app.middleware("http")(rate_limiter_middleware)
app.include_router(api_router)


@app.post("/send-email", tags=["Tasks"])
async def send_email(email: EmailStr = Body()):
    task = send.delay(email)
    return {
        "task_id": task.id,
        "message": f"Письмо отправлено на {email}",
    }


@app.get("/status/{task_id}", tags=["Tasks"])
async def get_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task.status,
        "result": task.result,
    }
