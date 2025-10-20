
""" Назначение: Фикстуры для пользователей """


import factory
from uuid import uuid4

from src.app.core.constants import Role
from src.app.models.users_models import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.LazyAttribute(lambda o: uuid4())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password_hash = factory.Faker('password', length=12)
    role = Role.USER
    active = True
