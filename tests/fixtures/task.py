
""" Назначение: Фабрики для создания экземпляров задач """


from factory import Factory, Faker, Sequence

from src.app.core.constants import TaskStatus
from src.app.models.tasks_models import Task


class TaskFactory(Factory):
    class Meta:
        model = Task

    title = Sequence(lambda n: f'Task {n}')
    description = Faker('paragraph', nb_sentences=3)
    status = Faker('random_element', elements=list(TaskStatus))
