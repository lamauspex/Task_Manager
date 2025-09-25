
""" Назначение: Интерфейс репозитория """


from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Generic
from uuid import UUID

T = TypeVar('T')


class IUserRepository(ABC):
    """ Для работы с пользователями """

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[Any]: ...

    @abstractmethod
    async def find_all(self) -> List[Any]: ...

    @abstractmethod
    async def add(self, obj: Any) -> Any: ...

    @abstractmethod
    async def update(self, entity_id: UUID, data: dict) -> Optional[Any]: ...

    @abstractmethod
    async def remove(self, entity_id: UUID) -> bool: ...


class ITaskRepository(ABC, Generic[T]):
    """ Для работы с задачами """

    @abstractmethod
    async def find_all(self) -> List[Any]:
        """ Возвращает список всех задач """
        pass

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[Any]:
        """ Возвращает задачу по её идентификатору """
        pass

    @abstractmethod
    async def add(self, obj: Any) -> Any:
        """ Сохраняет новую задачу """
        pass

    @abstractmethod
    async def update(self, entity_id: UUID, data: dict) -> Optional[Any]:
        """ Обновляет существующий объект задачи """
        pass

    @abstractmethod
    async def remove(self, entity_id: UUID) -> bool:
        """ Удаляет задачу по её идентификатору """
        pass
