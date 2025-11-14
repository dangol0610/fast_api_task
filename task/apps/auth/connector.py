from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO


class Connector:
    def __init__(self):
        self.user_repository = UserRepository()

    async def get_by_username(self, username: str) -> UserAddDTO | None:
        user = await self.user_repository.get_by_username(username)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    async def get_by_email(self, email: str) -> UserAddDTO | None:
        user = await self.user_repository.get_by_email(email)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    async def create_user(self, user: UserAddDTO) -> UserAddDTO | None:
        created = await self.user_repository.create(user)
        if not created:
            return None
        return UserAddDTO.model_validate(created)
