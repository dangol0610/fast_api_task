import asyncio
from email.message import EmailMessage
import aiosmtplib
from pydantic import EmailStr
from task.celery.celery_utils import celery_app
from task.settings.settings import settings


@celery_app.task
def send_email(email: EmailStr) -> str:
    message = EmailMessage()
    message["From"] = settings.SMTP_FROM
    message["To"] = email
    message["Subject"] = "Тестовое письмо"
    message.set_content(settings.MESSAGE)

    async def send():
        try:
            server = aiosmtplib.SMTP(
                hostname=settings.SMTP_HOST, port=settings.SMTP_PORT
            )
            await server.connect()
            await server.login(settings.SMTP_USER, settings.GMAIL_PASS)
            await server.sendmail(
                settings.SMTP_FROM,
                [email],
                message.as_string(),
            )
            await server.quit()
            return {
                "email": email,
                "message": settings.MESSAGE,
            }
        except Exception as e:
            return {
                "email": email,
                "message": f"Ошибка при отправке письма: {e}",
            }

    return asyncio.run(send())
