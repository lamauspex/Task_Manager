
""" Назначение: Базовые модели """


from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from datetime import datetime


class TimestampMixin:
    """ Миксин для общих временных меток """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True
    )


class PrimaryKeyMixin:
    """ Миксин для основного ключа """

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        primary_key=True
    )


class BaseModel(TimestampMixin, PrimaryKeyMixin):
    """ Базовая модель с временными метками и ID """

    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'
