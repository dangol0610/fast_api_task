from task.apps.users.dependencies import get_repository
from task.apps.users.schemas import UserFullSchema


class Connector:
    def __init__(self):
        self.user_repository = get_repository()

    def get_by_username(self, username: str) -> UserFullSchema | None:
        with self.user_repository.connection as user_storage:
            for user in user_storage.get_users_storage():
                if user.username == username:
                    return user
            return None

    def get_by_email(self, email: str) -> UserFullSchema | None:
        with self.user_repository.connection as user_storage:
            for user in user_storage.get_users_storage():
                if user.email == email:
                    return user
            return None

    def create_user(self, user: UserFullSchema) -> UserFullSchema:
        return self.user_repository.create(user)
