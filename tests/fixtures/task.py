
""" Назначение: Фабрики для создания экземпляров задач """


from factory import Factory, Faker

from src.app.core.constants import TaskStatus
from src.app.models.tasks_models import Task


class TaskFactory(Factory):
    class Meta:
        model = Task

    title = Faker('sentence', nb_words=5)
    description = Faker('paragraph', nb_sentences=3)
    status = Faker('random_element', elements=list(TaskStatus))
