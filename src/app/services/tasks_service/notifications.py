
""" Назначение: Отправка письма """


# import aiohttp
# from jinja2 import Environment, FileSystemLoader
# from aiosmtplib import send_mail

# from src.app.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD


# async def send_email(to_address: str, subject: str, message_body: str):
#     async with aiohttp.ClientSession() as session:

#         # Загрузка шаблона
#         env = Environment(loader=FileSystemLoader('templates'))
#         template = env.get_template('notification_email.html')
#         # Генерация HTML-содержимого
#         html_content = template.render(message=message_body)

#         # Подготовка сообщения
#         msg = {
#             'Subject': subject,
#             'From': EMAIL_USER,
#             'To': to_address,
#             'Content-Type': 'text/html',
#             'Body': html_content
#         }

#         # Отправка почты
#         server = await send_mail.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
#         await server.starttls()
#         await server.login(EMAIL_USER, EMAIL_PASSWORD)
#         await server.send_message(msg)
