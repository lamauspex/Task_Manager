
""" Назначение: Роуты задач """


from uuid import UUID
from fastapi import APIRouter, Depends

from src.app.core.utils import get_tasks_service
from src.app.exceptions.http import AppHttpNotFound
from src.app.schemas.tasks_schemas import TaskCreate, TaskUpdate, TaskOut
from src.app.services.tasks_service.tasks_service import TasksService
from src.app.exceptions.decorators import exception_handler

router = APIRouter(prefix="/tasks", tags=["Tasks"])


# Создание новой задачи
@router.post("/",
             response_model=TaskOut,
             summary="Создать новую задачу")
@exception_handler
async def create_task(
    task_in: TaskCreate,
    service: TasksService = Depends(get_tasks_service)
):

    new_task = await service.add(task_in)
    return new_task


# Получение задачи по id
@router.get("/{task_id}",
            response_model=TaskOut,
            summary="Получить задачу по ID")
@exception_handler
async def read_task(
    task_id: UUID,
    service: TasksService = Depends(get_tasks_service)
):

    task = await service.find_by_id(task_id)

    if task is None:
        raise AppHttpNotFound(resource_name="task")
    return task


# Получение всех задач
@router.get("/list/",
            response_model=list[TaskOut],
            summary="Получить список всех задач")
@exception_handler
async def get_tasks(
    service: TasksService = Depends(get_tasks_service)
) -> list[TaskOut]:
    return await service.all()


# Обновление задачи
@router.put("/{task_id}",
            response_model=TaskOut,
            summary="Обновить задачу")
@exception_handler
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    service: TasksService = Depends(get_tasks_service)
):

    updated_task = await service.update(task_id, task_data)

    if updated_task is None:
        raise AppHttpNotFound(resource_name="task")
    return updated_task


# Назначить ответственного
@router.put("/{task_id}/assign",
            response_model=TaskOut,
            summary="Назначить задачу пользователю")
@exception_handler
async def assign_task(
    task_id: UUID,
    user_id: UUID,
    service: TasksService = Depends(get_tasks_service)
):

    return await service.assign_task(task_id, user_id)


# Завершение задачи
@router.put("/{task_id}/complete",
            response_model=TaskOut,
            summary="Завершить задачу")
@exception_handler
async def complete_task(
        task_id: UUID,
        user_id: UUID,
        service: TasksService = Depends(get_tasks_service)
):

    completed_task = await service.complete_task(task_id, user_id)

    if completed_task is None:
        raise AppHttpNotFound(resource_name="task")
    return completed_task


# Удалить задачу
@router.delete("/{task_id}",
               summary="Удалить задачу")
@exception_handler
async def delete_task(
        task_id: UUID,
        service: TasksService = Depends(get_tasks_service)
):

    deleted = await service.delete(task_id)

    if not deleted:
        raise AppHttpNotFound(resource_name="task")
    return {"detail": f"Задача {task_id} успешно удалена!"}
