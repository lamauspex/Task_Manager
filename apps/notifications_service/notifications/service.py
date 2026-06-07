"""
Notification service.

Uses background tasks (FastAPI BackgroundTasks or Celery) to send emails.
Fully synchronous SMTP wrapper — no asyncio-in-celery hacks.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.src.app.core.config import settings
from backend.src.app.models.task import Task
from backend.src.app.models.user import User

logger = logging.getLogger("task_manager.notifications")


class NotificationService:
    """Sends email notifications. Gracefully skips if EMAIL_ENABLED=false."""

    async def notify_task_assigned(self, task: Task, assignee: User) -> None:
        """Notify *assignee* that they have been assigned *task*."""
        subject = f"[Task Manager] New task assigned: {task.title}"
        body = (
            f"Hello, {assignee.full_name}!\n\n"
            f"You have been assigned a new task:\n"
            f"  Title: {task.title}\n"
            f"  Description: {task.description or 'No description'}\n\n"
            f"Log in to manage your tasks.\n\n"
            f"— Task Manager Pro"
        )
        await self._send(to=assignee.email, subject=subject, body=body)

    async def _send(self, *, to: str, subject: str, body: str) -> None:
        if not settings.EMAIL_ENABLED:
            logger.debug("Email disabled. Would send '%s' to %s", subject, to)
            return

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_USER}>"
            msg["To"] = to
            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=10) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                smtp.sendmail(settings.EMAIL_USER, to, msg.as_string())

            logger.info("Email sent to %s: %s", to, subject)
        except Exception as exc:
            # Notifications must never break the main flow
            logger.error("Failed to send email to %s: %s", to, exc)
