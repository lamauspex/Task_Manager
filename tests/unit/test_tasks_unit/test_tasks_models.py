
""" Назначение: Тесты моделей TASK """


from sqlalchemy import select
import pytest
import sqlalchemy

from src.app.core.constants import TaskStatus
from src.app.models.tasks_models import Task
from tests.fixtures.task import TaskFactory


@pytest.mark.asyncio
async def test_task_creation(db_session):
    """ Проверяет процесс создания и сохранения задачи в базе данных. """
    new_task = TaskFactory.build()
    db_session.add(new_task)
    await db_session.commit()
    retrieved_task = await db_session.get(Task, new_task.id)

    assert retrieved_task.title == new_task.title
    assert retrieved_task.description == new_task.description
    assert retrieved_task.status == new_task.status


@pytest.mark.asyncio
async def test_task_attributes():
    """ Проверяет наличие нужных атрибутов у задачи """
    task = TaskFactory.build()
    assert hasattr(task, 'id')
    assert hasattr(task, 'title')
    assert hasattr(task, 'description')
    assert hasattr(task, 'status')


@pytest.mark.asyncio
async def test_delete_task(db_session):
    """ Тестирует удаление задачи """
    new_task = TaskFactory.build()
    db_session.add(new_task)

    await db_session.flush()
    await db_session.refresh(new_task)

    await db_session.delete(new_task)
    await db_session.commit()

    retrieved_task = await db_session.get(Task, new_task.id)
    assert retrieved_task is None


@pytest.mark.asyncio
async def test_repeated_id(db_session):
    """ Повторное использование ID """
    existing_task = TaskFactory.build()
    db_session.add(existing_task)
    await db_session.commit()

    duplicate_task = Task(id=existing_task.id, title="Duplicate Title")
    db_session.add(duplicate_task)

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        await db_session.flush()
        await db_session.commit()


@pytest.mark.asyncio
async def test_max_field(db_session):
    """ Проверка ограничений полей """
    long_title = "a" * 101
    task = Task(title=long_title, description="Valid_Description")
    db_session.add(task)

    try:
        await db_session.flush()
        await db_session.commit()
    except Exception as e:
        print(e)
        raise


@pytest.mark.asyncio
async def test_status_update(db_session):
    """ Создание и обновление статуса задачи """
    task = TaskFactory.create(status=TaskStatus.CREATED)
    task.status = TaskStatus.IN_PROGRESS

    db_session.add(task)
    await db_session.flush()
    await db_session.commit()

    assert task.id is not None
    retrived_task = await db_session.get(Task, task.id)

    assert retrived_task is not None
    assert retrived_task.status == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_filter_task_by_status(db_session):
    """ Фильтрация задач по статусу """

    # Создаем две задачи с разными статусами
    tasks = [
        Task(title="Задача в процессе", description="Описание задачи",
             status=TaskStatus.IN_PROGRESS),
        Task(title="Созданная задача", description="Новая задача",
             status=TaskStatus.CREATED)
    ]

    # Сохраняем обе задачи в базе данных
    db_session.add_all(tasks)
    await db_session.commit()

    # Получаем задачи, соответствующие состоянию IN_PROGRESS
    stmt = select(Task).where(Task.status == TaskStatus.IN_PROGRESS)
    result = await db_session.execute(stmt)
    filtered_tasks = result.scalars().all()

    # Проверяем количество полученных задач
    assert len(filtered_tasks) == 1
    assert filtered_tasks[0].title == "Задача в процессе"
    assert filtered_tasks[0].status == TaskStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_bulk_insert_tasks(db_session):
    """Массовая вставка задач."""
    tasks = [TaskFactory.build() for _ in range(10)]
    db_session.add_all(tasks)
    await db_session.commit()

    results = await db_session.execute(select(Task))
    fetched_tasks = results.scalars().all()

    assert len(fetched_tasks) >= 10


# @pytest.mark.asyncio
# async def test_unique_number_violation(db_session):
#     """Проверка соблюдения уникальности номера задачи."""
#     first_task = TaskFactory.create(number=1)
#     second_task = TaskFactory.build(number=first_task.number)
#     db_session.add(first_task)
#     await db_session.commit()

#     db_session.add(second_task)

#     with pytest.raises(Exception):
#         await db_session.commit()
