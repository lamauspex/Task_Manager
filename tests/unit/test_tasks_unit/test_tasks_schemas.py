
""" Назначение: Тесты схем Pydantic Tasks """


import json
import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime, timezone

from src.app.schemas.tasks_schemas import (
    TaskCreate, TaskUpdate, TaskOut, TaskStatus
)


def test_task_create_empty_object():
    """ Тестирует создание задачи с пустым объектом, ожидая ошибку """
    with pytest.raises(ValidationError):
        TaskCreate()


def test_task_create_unicode_characters():
    """ Тестирует использование Unicode символов в описании """
    unicode_desc = "😊🎉✨"
    task_data = {"title": "Unicode Test", "description": unicode_desc}
    TaskCreate(**task_data)


def test_task_create_valid():
    """ Тестирует создание задачи с валидными данными """
    task_data = {

        "title": "Test Task",
        "description": "This is a test task.",
    }
    task = TaskCreate(**task_data)
    assert task.title == task_data['title']
    assert task.description == task_data['description']


def test_task_create_missing_title():
    """ Тестирует создание задачи без заголовка,
    должно вызвать ошибку валидации """
    task_data = {
        "description": "This is a test task."
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
        TaskUpdate(**task_data)


def test_task_out():
    """ Тест модели вывода задач """
    task_uuid = uuid.uuid4()
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED,
        "id": str(task_uuid),
        "created_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "updated_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "assigned_to_id": str(uuid.UUID('123e4567-e89b-12d3-a456-426655440000')),
        "completed_by_id": None
    }

    task = TaskOut(**task_data)

    assert isinstance(task, TaskOut)

    assert task.title == task_data["title"]
    assert task.description == task_data["description"]
    assert task.status == task_data["status"]
    assert task.id == task_uuid
    assert task.created_at.isoformat() == "2023-01-01T00:00:00+00:00"
    assert task.updated_at.isoformat() == "2023-01-01T00:00:00+00:00"


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


def test_tasc_create_json_serialization():
    """ Тестирует сериализацию модели TaskOut в JSON """
    task_uuid = uuid.uuid4()
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED,
        "id": str(task_uuid),
        "created_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "updated_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "assigned_to_id": str(uuid.UUID('123e4567-e89b-12d3-a456-426655440000')),
        "completed_by_id": None
    }

    task = TaskOut(**task_data)
    json_data = task.model_dump(mode='json')
    assert isinstance(json_data.get('id'), str)


def custom_json_serializer(obj):
    """Обработчик сериализации для объектов datetime и UUID."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    raise TypeError(f"Type {obj.__class__.__name__} not serializable")


def test_task_out_deserialization_from_json():
    """ Тестирует дескериализацию из JSON """
    task_uuid = uuid.uuid4()
    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": TaskStatus.CREATED.value,
        "id": str(task_uuid),
        "created_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "updated_at": datetime.fromisoformat("2023-01-01T00:00:00").replace(tzinfo=timezone.utc),
        "assigned_to_id": str(uuid.UUID('123e4567-e89b-12d3-a456-426655440000')),
        "completed_by_id": None
    }

    # Используем собственный сериализатор для объектов datetime
    serialized_data = json.dumps(task_data, default=custom_json_serializer)
    deserialized_task = TaskOut.model_validate_json(serialized_data)
    assert isinstance(deserialized_task, TaskOut)
