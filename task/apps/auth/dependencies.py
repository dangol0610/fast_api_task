from fastapi import Header
from jose import JWTError
from task.apps.auth.repository import AuthRepository
from task.apps.users.schemas import UserAddDTO
from task.utils.dependencies import RedisDependency, SessionDependency
from task.utils.exceptions import (
    InvalidTokenException,
    InvalidTokenPayloadException,
    ItemNotFoundException,
    JWTTokenMissingException,
    SessionMissingException,
)
from task.utils.token_utils import TokenUtils


async def get_current_user(
    session: SessionDependency,
    x_jwt_token: str = Header(..., alias="X-JWT-Token"),
) -> UserAddDTO:
    if not x_jwt_token:
        raise JWTTokenMissingException
    token = x_jwt_token
    try:
        payload = TokenUtils.decode_token(token)
        if not payload:
            raise InvalidTokenPayloadException
        username = payload.get("sub")
        if not username:
            raise InvalidTokenPayloadException
        user = await AuthRepository.get_by_username(username=username, session=session)
        if not user:
            raise ItemNotFoundException
        return user
    except JWTError:
        raise InvalidTokenException


async def get_current_by_session(
    session: SessionDependency,
    redis: RedisDependency,
    x_session: str = Header(..., alias="X-Session"),
):
    username = await redis.get(f"session:{x_session}")
    if not username:
        raise SessionMissingException
    user = await AuthRepository.get_by_username(username=username, session=session)
    if not user:
        raise ItemNotFoundException
    return user
