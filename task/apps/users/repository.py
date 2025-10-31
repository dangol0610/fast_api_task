from task.apps.users.models import ConnectionManager, UsersStorage
from task.apps.users.schemas import UserFullSchema


class UserRepository:
    def __init__(self, model: UsersStorage, connection: ConnectionManager):
        self._model = model
        self.connection = connection

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        if hasattr(self, "_model"):
            raise AttributeError("Нельзя заменить имеющееся хранилище")
        self._model = value

    @model.deleter
    def model(self):
        del self._model

    def get_all(self) -> list[UserFullSchema]:
        with self.connection as storage:
            return storage.get_users_storage()

    def get_by_id(self, id: int) -> UserFullSchema | None:
        with self.connection as storage:
            for user in storage.get_users_storage():
                if user.id == id:
                    return user
            return None

    def get_by_ids(self, ids: list[int]) -> list[UserFullSchema] | None:
        with self.connection as storage:
            users = [user for user in storage.get_users_storage() if user.id in ids]
            if not users:
                return None
            return users

    def create(self, user: UserFullSchema) -> UserFullSchema:
        with self.connection as storage:
            users = storage.get_users_storage()
            users.append(user)
            storage.set_users_storage(users)
            return user

    def create_many(self, users: list[UserFullSchema]) -> list[UserFullSchema]:
        with self.connection as storage:
            users_storage = storage.get_users_storage()
            users_storage.extend(users)
            storage.set_users_storage(users_storage)
            return users

    def update(self, user_id: int, new_user: UserFullSchema) -> UserFullSchema | None:
        with self.connection as storage:
            users_storage = storage.get_users_storage()
            for i, user in enumerate(users_storage):
                if user.id == user_id:
                    users_storage[i] = new_user
                    storage.set_users_storage(users_storage)
                    return new_user
            return None

    def delete(self, user_id: int) -> UserFullSchema | None:
        with self.connection as storage:
            users_storage = storage.get_users_storage()
            for i, user in enumerate(users_storage):
                if user.id == user_id:
                    removed_user = users_storage.pop(i)
                    storage.set_users_storage(users_storage)
                    return removed_user
            return None
