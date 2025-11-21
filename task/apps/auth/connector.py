from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO


class Connector:
    @classmethod
    async def get_by_username(cls, username: str) -> UserAddDTO | None:
        user = await UserRepository.get_by_username(username)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    @classmethod
    async def get_by_email(cls, email: str) -> UserAddDTO | None:
        user = await UserRepository.get_by_email(email)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    @classmethod
    async def create_user(cls, user: UserAddDTO) -> UserAddDTO | None:
        created = await UserRepository.create(user)
        if not created:
            return None
        return UserAddDTO.model_validate(created)
