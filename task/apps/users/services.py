from task.apps.auth.services import AuthService
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO, UserDTO, UserUpdateDTO, UserRelDto


class UserService:
    @classmethod
    async def get_all(cls) -> list[UserRelDto]:
        users = await UserRepository.get_all()
        return [UserRelDto.model_validate(user) for user in users]

    @classmethod
    async def get_by_id(cls, user_id: int) -> UserRelDto:
        user = await UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return UserRelDto.model_validate(user)

    @classmethod
    async def get_by_ids(cls, user_ids: list[int]) -> list[UserRelDto]:
        users = await UserRepository.get_by_ids(user_ids)
        return [UserRelDto.model_validate(user) for user in users]

    @classmethod
    async def create_user(cls, user_data: UserAddDTO) -> UserDTO:
        hashed = AuthService.hash_password(user_data.hashed_password)
        user_data.hashed_password = hashed
        user = await UserRepository.create(user_data)
        if not user:
            raise ValueError("Can not create user")
        return UserDTO.model_validate(user)

    @classmethod
    async def create_many(cls, users_data: list[UserAddDTO]) -> list[UserDTO]:
        for user in users_data:
            user.hashed_password = AuthService.hash_password(user.hashed_password)
        users = await UserRepository.create_many(users_data)
        if not users:
            raise ValueError("Can not create users")
        return [UserDTO.model_validate(user) for user in users]

    @classmethod
    async def update(cls, id: int, user_data: UserUpdateDTO) -> UserDTO:
        user = await UserRepository.update(id, user_data)
        if not user:
            raise ValueError(f"Can not update user on id {id}")
        return UserDTO.model_validate(user)

    @classmethod
    async def delete(cls, id: int) -> UserDTO:
        user = await UserRepository.delete(id)
        if not user:
            raise ValueError(f"Can not delete user on id {id}")
        return UserDTO.model_validate(user)
