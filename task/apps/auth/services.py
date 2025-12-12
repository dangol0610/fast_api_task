import uuid

from task.apps.auth.repository import AuthRepository
from task.apps.auth.schemas import AuthRegisterSchema

from task.utils.dependencies import RedisDependency, SessionDependency
from task.utils.exceptions import InvalidCredentialsException
from task.utils.password_utils import PasswordUtils
from task.utils.token_utils import TokenUtils


class AuthService:
    @classmethod
    async def register(cls, data: AuthRegisterSchema, session: SessionDependency):
        data.password = PasswordUtils.hash_password(data.password)
        return await AuthRepository.register_user(data=data, session=session)

    @classmethod
    async def login(
        cls,
        username: str,
        password: str,
        session: SessionDependency,
        redis: RedisDependency,
    ):
        user = await AuthRepository.get_by_username(username=username, session=session)
        if not PasswordUtils.verify_password(password, user.hashed_password):
            raise InvalidCredentialsException
        session_id = str(uuid.uuid4())
        await redis.set(f"session:{session_id}", user.username, ex=600)

        payload = {"sub": user.username, "email": user.email}
        access_token = TokenUtils.create_access_token(payload)
        refresh_token = TokenUtils.create_refresh_token(payload)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "session": session_id,
        }
