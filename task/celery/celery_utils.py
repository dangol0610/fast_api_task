from celery import Celery
from celery.schedules import crontab
from task.settings.settings import settings


def make_celery():
    broker_url = settings.redis_broker_url
    result_backend = settings.redis_result_url
    celery = Celery(
        "tasks",
        broker=broker_url,
        backend=result_backend,
    )
    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
        beat_schedule={
            "minute_report": {
                "task": "task.celery.tasks.periodic.weekly_report",
                "schedule": crontab(minute="*/1"),
            },
        },
    )
    return celery


celery_app = make_celery()
celery_app.autodiscover_tasks(["task.celery.tasks"])
