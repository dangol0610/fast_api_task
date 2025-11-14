from fastapi import HTTPException, status
from task.apps.auth.connector import Connector
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.users.schemas import UserAddDTO


class AuthRepository:
    def __init__(self, connector: Connector):
        self.connector = connector

    async def get_by_username(self, username: str) -> UserAddDTO | None:
        return await self.connector.get_by_username(username)

    async def get_by_email(self, email: str) -> UserAddDTO | None:
        return await self.connector.get_by_email(email)

    async def register_user(self, data: AuthRegisterSchema) -> UserAddDTO:
        if await self.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username exist"
            )
        if await self.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email exist"
            )
        user_dto = UserAddDTO(
            username=data.username, email=data.email, hashed_password=data.password
        )
        created_user = await self.connector.create_user(user_dto)
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create user"
            )
        return created_user
