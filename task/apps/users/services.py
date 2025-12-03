import json
from fastapi import HTTPException, status
from redis import Redis
from task.apps.auth.services import AuthService
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO, UserDTO, UserUpdateDTO, UserRelDto
from task.utils.dependencies import SessionDependency


class UserService:
    @classmethod
    async def get_all(
        cls,
        session: SessionDependency,
        redis: Redis,
        ttl_cache=300,
    ) -> list[UserRelDto]:
        cache_key = "users:all"
        cached_data = await redis.get(cache_key)
        if cached_data:
            users = json.loads(cached_data)
            return [UserRelDto.model_validate_json(user) for user in users]
        users = await UserRepository.get_all(session=session)
        users_dto = [UserRelDto.model_validate(user) for user in users]
        await redis.set(
            cache_key,
            json.dumps([user.model_dump_json() for user in users_dto]),
            ex=ttl_cache,
        )
        return users_dto

    @classmethod
    async def get_by_id(
        cls,
        user_id: int,
        session: SessionDependency,
        redis: Redis,
        ttl_cache=300,
    ) -> UserRelDto:
        cache_key = f"user:{user_id}"
        try:
            cached_data = await redis.get(cache_key)
            await redis.incr(f"stats:hits:user:{user_id}")
            if cached_data:
                return UserRelDto.model_validate_json(cached_data)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Redis error"
            )
        user = await UserRepository.get_by_id(id=user_id, session=session)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        user = UserRelDto.model_validate(user)
        if cached_data is None:
            try:
                await redis.set(cache_key, user.model_dump_json(), ex=ttl_cache)
                await redis.incr(f"stats:miss:user:{user_id}")
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Redis error",
                )
        return user

    @classmethod
    async def get_by_ids(
        cls,
        user_ids: list[int],
        session: SessionDependency,
    ) -> list[UserRelDto]:
        users = await UserRepository.get_by_ids(ids=user_ids, session=session)
        return [UserRelDto.model_validate(user) for user in users]

    @classmethod
    async def create_user(
        cls,
        user_data: UserAddDTO,
        session: SessionDependency,
        redis: Redis,
    ) -> UserDTO:
        hashed = AuthService.hash_password(user_data.hashed_password)
        user_data.hashed_password = hashed
        user = await UserRepository.create(user=user_data, session=session)
        if not user:
            raise ValueError("Can not create user")
        await redis.delete("users:all")
        return UserDTO.model_validate(user)

    @classmethod
    async def create_many(
        cls,
        users_data: list[UserAddDTO],
        session: SessionDependency,
        redis: Redis,
    ) -> list[UserDTO]:
        for user in users_data:
            user.hashed_password = AuthService.hash_password(user.hashed_password)
        users = await UserRepository.create_many(users=users_data, session=session)
        if not users:
            raise ValueError("Can not create users")
        await redis.delete("users:all")
        return [UserDTO.model_validate(user) for user in users]

    @classmethod
    async def update(
        cls,
        id: int,
        user_data: UserUpdateDTO,
        session: SessionDependency,
        redis: Redis,
    ) -> UserDTO:
        user = await UserRepository.update(
            user_id=id, new_user=user_data, session=session
        )
        if not user:
            raise ValueError(f"Can not update user on id {id}")
        await redis.delete(f"user:{id}")
        await redis.delete("users:all")
        return UserDTO.model_validate(user)

    @classmethod
    async def delete(
        cls,
        id: int,
        session: SessionDependency,
        redis: Redis,
    ) -> UserDTO:
        user = await UserRepository.delete(user_id=id, session=session)
        if not user:
            raise ValueError(f"Can not delete user on id {id}")
        await redis.delete(f"user:{id}")
        await redis.delete("users:all")
        return UserDTO.model_validate(user)
