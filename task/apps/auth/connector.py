from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO
from task.utils.dependencies import SessionDependency


class Connector:
    @classmethod
    async def get_by_username(
        cls, username: str, session: SessionDependency
    ) -> UserAddDTO | None:
        user = await UserRepository.get_by_username(username=username, session=session)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    @classmethod
    async def get_by_email(
        cls, email: str, session: SessionDependency
    ) -> UserAddDTO | None:
        user = await UserRepository.get_by_email(email=email, session=session)
        if not user:
            return None
        return UserAddDTO.model_validate(user)

    @classmethod
    async def create_user(
        cls, user: UserAddDTO, session: SessionDependency
    ) -> UserAddDTO | None:
        created = await UserRepository.create(user=user, session=session)
        if not created:
            return None
        return UserAddDTO.model_validate(created)
