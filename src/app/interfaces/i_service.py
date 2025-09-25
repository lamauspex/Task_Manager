
""" Назначение: Интерфейс сервиса """


from abc import ABC, abstractmethod
from typing import Any, List, Optional
from uuid import UUID


class IUserService(ABC):
    """ Для работы с пользователями """

    @abstractmethod
    async def get_by_id(self, entity_id: UUID) -> Optional[Any]: ...

    @abstractmethod
    async def get_all(self) -> List[Any]: ...

    @abstractmethod
    async def create(self, data: dict) -> Any: ...

    @abstractmethod
    async def update(self, entity_id: UUID, data: dict) -> Optional[Any]: ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool: ...


class ITaskService(ABC):
    """ Для работы с задачами """

    @abstractmethod
    async def add(self, data: dict) -> Any: ...

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[Any]: ...

    @abstractmethod
    async def all(self) -> List[Any]: ...

    @abstractmethod
    async def update(self, entity_id: UUID, data: dict) -> Optional[Any]: ...

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:  ...
