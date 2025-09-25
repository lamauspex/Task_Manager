
""" Назначение: Фикстуры для пользователей """


from factory import Factory, Faker

from src.app.core.constants import Role
from src.app.schemas.users_schemas import UserCreate


class UserFactory(Factory):
    class Meta:
        model = UserCreate

    name = Faker('first_name')
    email = Faker('email')
    password = Faker('password')
    role = Faker('random_element', elements=list(Role))
