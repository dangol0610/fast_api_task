from task.apps.auth.services import AuthService
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO, UserDTO, UserUpdateDTO, UserRelDto


class UserService:
    def __init__(self, repository: UserRepository, auth_service: AuthService):
        self.repository = repository
        self.auth_service = auth_service

    async def get_all(self) -> list[UserRelDto]:
        users = await self.repository.get_all()
        return [UserRelDto.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserRelDto:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return UserRelDto.model_validate(user)

    async def get_by_ids(self, user_ids: list[int]) -> list[UserRelDto]:
        users = await self.repository.get_by_ids(user_ids)
        return [UserRelDto.model_validate(user) for user in users]

    async def create_user(self, user_data: UserAddDTO) -> UserDTO:
        hashed = self.auth_service.hash_password(user_data.hashed_password)
        user_data.hashed_password = hashed
        user = await self.repository.create(user_data)
        if not user:
            raise ValueError("Can not create user")
        return UserDTO.model_validate(user)

    async def create_many(self, users_data: list[UserAddDTO]) -> list[UserDTO]:
        for user in users_data:
            user.hashed_password = self.auth_service.hash_password(user.hashed_password)
        users = await self.repository.create_many(users_data)
        if not users:
            raise ValueError("Can not create users")
        return [UserDTO.model_validate(user) for user in users]

    async def update(self, id: int, user_data: UserUpdateDTO) -> UserDTO:
        user = await self.repository.update(id, user_data)
        if not user:
            raise ValueError(f"Can not update user on id {id}")
        return UserDTO.model_validate(user)

    async def delete(self, id: int) -> UserDTO:
        user = await self.repository.delete(id)
        if not user:
            raise ValueError(f"Can not delete user on id {id}")
        return UserDTO.model_validate(user)
