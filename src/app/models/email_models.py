
""" Назначение: Таблица для хранения логов отправки писем """


from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from src.app.core.database import Base
from src.app.models.base import BaseModel


class EmailLog(Base, BaseModel):
    # Адресат
    recipient: Mapped[str] = mapped_column(
        String(length=100)
    )
    # Тема письма
    subject: Mapped[str] = mapped_column(
        String(length=200)
    )
    # Содержимое письма
    body: Mapped[str] = mapped_column(
        String(length=500)
    )
    # Статус отправки ('sent', 'failed')
    status: Mapped[str] = mapped_column(
        String(length=50)
    )
    # Ошибка (если была)
    error_message: Mapped[Optional[str]] = mapped_column(
        String(length=200)
    )
