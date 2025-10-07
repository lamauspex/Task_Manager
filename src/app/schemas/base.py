
""" Назначение: Базовый класс контроллера """


from pydantic import Field
import uuid
from datetime import datetime
from pydantic import BaseModel


class Notification(BaseModel):
    recipient: str
    subject: str
    body: str


class CreateBase(BaseModel):
    """Базовая модель для всех схем создания"""
    pass


class UpdateBase(BaseModel):
    """Базовая модель для всех схем обновления"""
    pass


class OutputBase(BaseModel):
    """Базовая модель вывода сущности"""

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Идентификатор сущности."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Время создания."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Последнее обновление."
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
