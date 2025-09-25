
""" Назначение: Тесты схем Pydantic Tasks """


import uuid
import pytest
from pydantic import ValidationError

from src.app.schemas.tasks_schemas import (
    TaskCreate, TaskUpdate, TaskOut, TaskStatus
)


def test_task_create_valid():
    """ Тестирует создание задачи с валидными данными """
    task_data = {

        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED
    }
    task = TaskCreate(**task_data)
    assert task.title == task_data['title']
    assert task.status == task_data['status']


def test_task_create_missing_title():
    """ Тестирует создание задачи без заголовка,
    должно вызвать ошибку валидации """
    task_data = {
        "description": "This is a test task."
    }
    with pytest.raises(ValidationError):
        TaskCreate(**task_data)


def test_task_create_invalid_status():
    """ Тестирует создание задачи с недопустимым статусом,
    должно вызвать ошибку валидации """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "invalid_status"
    }
    with pytest.raises(ValidationError):
        TaskCreate(**task_data)


def test_task_update_with_extra_fields():
    """ Тестирует обновление задачи с дополнительными полями,
    которые допускаются """
    task_data = {
        "title": "Task Update",
        "description": "Updating the task.",
        "status": TaskStatus.IN_PROGRESS,
        "extra_field": "extra_value"
    }

    with pytest.raises(ValidationError):
        TaskCreate(**task_data)


def test_task_out():
    """ Тест модели вывода задача """
    task_data = {
        # "number": 0,
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED,
        "id": str(uuid.uuid4()),
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }

    task = TaskOut(**task_data)
    assert isinstance(task, TaskOut)


def test_task_create_without_optional_fields():
    """ Тестирует создание задачи без передачи необязательных полей """
    task_data = {

        "title": "aaaa",
        "description": "aaaaaa",
        "status": TaskStatus.CREATED
    }

    task = TaskCreate(**task_data)

    assert task.description == task_data['description']
    assert task.status == TaskStatus.CREATED


def test_task_create_min_max():
    """ Тестирует минимально и максимально допустимую длину полей """
    min_title = "a" * 1
    max_title = "a" * 100
    min_description = "S" * 1
    max_description = "S" * 300

    task_data = {

        "title": min_title,
        "description": min_description,
        "status": TaskStatus.CREATED
    }
    TaskCreate(**task_data)

    task_data.update({"title": max_title, "description": max_description})
    TaskCreate(**task_data)


def test_task_update_change_status():
    """ Тестирует изменение статуса задачи при обновлении """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.COMPLETED
    }
    task = TaskUpdate(**task_data)
    assert task.status == TaskStatus.COMPLETED


def test_update_partial_fields():
    """ Тестирует частичное обновление задачи (без описания) """
    task_data = {
        "title": "Update title",
        "status": TaskStatus.IN_PROGRESS
    }
    task = TaskUpdate(**task_data)
    assert task.description is None


def test_tasc_create_json_serialization():
    """ Тестирует сериализацию модели TaskOut в JSON """
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED,
        "id": str(uuid.uuid4()),
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }
    task = TaskOut(**task_data)
    json_data = task.model_dump(mode='json')
    assert isinstance(json_data.get('id'), str)
