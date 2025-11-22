from task.apps.auth.services import AuthService
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO, UserDTO, UserUpdateDTO, UserRelDto
from task.utils.dependencies import SessionDependency


class UserService:
    @classmethod
    async def get_all(cls, session: SessionDependency) -> list[UserRelDto]:
        users = await UserRepository.get_all(session=session)
        return [UserRelDto.model_validate(user) for user in users]

    @classmethod
    async def get_by_id(cls, user_id: int, session: SessionDependency) -> UserRelDto:
        user = await UserRepository.get_by_id(id=user_id, session=session)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return UserRelDto.model_validate(user)

    @classmethod
    async def get_by_ids(
        cls, user_ids: list[int], session: SessionDependency
    ) -> list[UserRelDto]:
        users = await UserRepository.get_by_ids(ids=user_ids, session=session)
        return [UserRelDto.model_validate(user) for user in users]

    @classmethod
    async def create_user(
        cls, user_data: UserAddDTO, session: SessionDependency
    ) -> UserDTO:
        hashed = AuthService.hash_password(user_data.hashed_password)
        user_data.hashed_password = hashed
        user = await UserRepository.create(user=user_data, session=session)
        if not user:
            raise ValueError("Can not create user")
        return UserDTO.model_validate(user)

    @classmethod
    async def create_many(
        cls, users_data: list[UserAddDTO], session: SessionDependency
    ) -> list[UserDTO]:
        for user in users_data:
            user.hashed_password = AuthService.hash_password(user.hashed_password)
        users = await UserRepository.create_many(users=users_data, session=session)
        if not users:
            raise ValueError("Can not create users")
        return [UserDTO.model_validate(user) for user in users]

    @classmethod
    async def update(
        cls, id: int, user_data: UserUpdateDTO, session: SessionDependency
    ) -> UserDTO:
        user = await UserRepository.update(
            user_id=id, new_user=user_data, session=session
        )
        if not user:
            raise ValueError(f"Can not update user on id {id}")
        return UserDTO.model_validate(user)

    @classmethod
    async def delete(cls, id: int, session: SessionDependency) -> UserDTO:
        user = await UserRepository.delete(user_id=id, session=session)
        if not user:
            raise ValueError(f"Can not delete user on id {id}")
        return UserDTO.model_validate(user)
