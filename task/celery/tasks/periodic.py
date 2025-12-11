from datetime import UTC, datetime
import logging
from task.celery.celery_utils import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def weekly_report():
    now = datetime.now(UTC)
    logger.info(f"Доброе утро! Сейчас: {now}")
    return None
