
""" Назначение: Интеграция с Celery """


import asyncio

from src.app.core.celery_config import app
from src.app.services.tasks_service.notifications import send_email
from src.app.models.email_models import EmailLog
from src.app.core.database import get_db


@app.task(name="send_notification")
def send_notification_task(to_address: str, subject: str, message_body: str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # Выполняем асинхронную операцию в синхроничном контексте Celery
        loop.run_until_complete(send_email(to_address, subject, message_body))

        # Логируем успешную отправку
        log_entry = EmailLog(
            recipient=to_address,
            subject=subject,
            body=message_body,
            status='sent'
        )
        get_db.add(log_entry)
        get_db.commit()
    except Exception as e:
        # Логируем ошибку
        log_entry = EmailLog(
            recipient=to_address,
            subject=subject,
            body=message_body,
            status='failed',
            error_message=str(e)
        )
        get_db.add(log_entry)
        get_db.commit()
        raise
