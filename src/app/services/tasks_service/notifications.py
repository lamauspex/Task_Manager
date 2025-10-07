
""" Назначение: Отправка письма """


from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader
from aiosmtplib import SMTP

from src.app.core.config import app_settings


async def send_email(
    to_address: str,
    subject: str,
    message_body: str
):
    # Загружаем шаблон письма
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('notification_email.html')
    html_content = template.render(body=message_body)

    # Формируем электронное письмо
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = app_settings.EMAIL_USER
    msg["To"] = to_address
    # Устанавливаем контент письма как HTML
    msg.set_content(html_content, subtype="html")

    # Отправляем письмо
    async with SMTP(
        hostname=app_settings.EMAIL_HOST,
        port=app_settings.EMAIL_PORT,
        use_tls=True
    ) as smtp:
        await smtp.login(
            app_settings.EMAIL_USER,
            app_settings.EMAIL_PASSWORD
        )
        await smtp.send_message(msg)
