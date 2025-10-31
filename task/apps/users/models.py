from task.apps.users.schemas import UserFullSchema
from task.settings.settings import settings


class UserDescriptor:
    def __get__(self, instance, owner):
        return instance._users

    def __set__(self, instance, value):
        if not isinstance(value, list):
            raise ValueError("Должен быть список")
        if not all(isinstance(item, UserFullSchema) for item in value):
            raise ValueError("Все элементы должны быть User")
        instance._users = value

    def __delete__(self, instance):
        instance._users = []


class UsersStorage:
    _instance = None
    users = UserDescriptor()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self._users = []

    def get_users_storage(self):
        return self.users

    def set_users_storage(self, users: list[UserFullSchema]):
        self.users = users


class ConnectionManager:
    def __enter__(self):
        print(f"Подключение к хранилищу по адресу: {settings.db_url}")
        return UsersStorage()

    def __exit__(self, exc_type, exc_val, traceback):
        print(f"Отключение от хранилища по адресу: {settings.db_url}")
