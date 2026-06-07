"""Task CRUD and workflow endpoints."""

import uuid
from fastapi import APIRouter, Depends

from backend.src.app.api.dependencies.auth import CurrentUser
from backend.src.app.api.dependencies.services import get_task_service
from backend.src.app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from backend.src.app.services.tasks.service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskOut], summary="List all tasks")
async def list_tasks(
    _: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> list[TaskOut]:
    return await service.get_all()


@router.post("/", response_model=TaskOut, status_code=201, summary="Create a new task")
async def create_task(
    data: TaskCreate,
    current_user: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return await service.create(data, current_user)


@router.get("/{task_id}", response_model=TaskOut, summary="Get task by ID")
async def get_task(
    task_id: uuid.UUID,
    _: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return await service.get_by_id(task_id)


@router.patch("/{task_id}", response_model=TaskOut, summary="Update task fields")
async def update_task(
    task_id: uuid.UUID,
    data: TaskUpdate,
    current_user: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return await service.update(task_id, data, current_user)


@router.delete("/{task_id}", status_code=204, summary="Delete a task")
async def delete_task(
    task_id: uuid.UUID,
    current_user: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> None:
    await service.delete(task_id, current_user)


@router.post("/{task_id}/assign", response_model=TaskOut, summary="Assign task to a user")
async def assign_task(
    task_id: uuid.UUID,
    assignee_id: uuid.UUID,
    current_user: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return await service.assign(task_id, assignee_id, current_user)


@router.post("/{task_id}/complete", response_model=TaskOut, summary="Mark task as completed")
async def complete_task(
    task_id: uuid.UUID,
    current_user: CurrentUser,
    service: TaskService = Depends(get_task_service),
) -> TaskOut:
    return await service.complete(task_id, current_user)
