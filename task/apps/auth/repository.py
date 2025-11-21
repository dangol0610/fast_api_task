from fastapi import HTTPException, status
from task.apps.auth.connector import Connector
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.users.schemas import UserAddDTO


class AuthRepository:
    @classmethod
    async def get_by_username(cls, username: str) -> UserAddDTO | None:
        return await Connector.get_by_username(username)

    @classmethod
    async def get_by_email(cls, email: str) -> UserAddDTO | None:
        return await Connector.get_by_email(email)

    @classmethod
    async def register_user(cls, data: AuthRegisterSchema) -> UserAddDTO:
        if await cls.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username exist"
            )
        if await cls.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email exist"
            )
        user_dto = UserAddDTO(
            username=data.username, email=data.email, hashed_password=data.password
        )
        created_user = await Connector.create_user(user_dto)
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create user"
            )
        return created_user
