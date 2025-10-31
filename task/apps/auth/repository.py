from fastapi import HTTPException, status
from task.apps.auth.connector import Connector
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.users.schemas import UserFullSchema


class AuthRepository:
    def __init__(self, connector: Connector):
        self.connector = connector

    def get_by_username(self, username: str) -> UserFullSchema | None:
        return self.connector.get_by_username(username)

    def register_user(self, data: AuthRegisterSchema) -> UserFullSchema:
        if self.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username exist"
            )
        if self.connector.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email exist"
            )
        users = self.connector.user_repository.get_all()
        new_id = max([user.id for user in users], default=0) + 1
        user = UserFullSchema(
            id=new_id,
            username=data.username,
            email=data.email,
            password=data.password,
        )
        return self.connector.create_user(user)
