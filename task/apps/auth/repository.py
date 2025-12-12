from task.apps.auth.connector import Connector
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.users.schemas import UserAddDTO
from task.utils.dependencies import SessionDependency
from task.utils.exceptions import EmailExistException, UsernameExistException


class AuthRepository:
    @classmethod
    async def get_by_username(
        cls, username: str, session: SessionDependency
    ) -> UserAddDTO | None:
        return await Connector.get_by_username(username=username, session=session)

    @classmethod
    async def get_by_email(
        cls, email: str, session: SessionDependency
    ) -> UserAddDTO | None:
        return await Connector.get_by_email(email=email, session=session)

    @classmethod
    async def register_user(
        cls, data: AuthRegisterSchema, session: SessionDependency
    ) -> UserAddDTO:
        if (
            await cls.get_by_username(username=data.username, session=session)
            is not None
        ):
            raise UsernameExistException
        if await cls.get_by_email(email=data.email, session=session) is not None:
            raise EmailExistException
        user_dto = UserAddDTO(
            username=data.username, email=data.email, hashed_password=data.password
        )
        created_user = await Connector.create_user(user=user_dto, session=session)
        return created_user
