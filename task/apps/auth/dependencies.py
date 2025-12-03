from fastapi import HTTPException, Header, status
from jose import JWTError
from task.apps.auth.repository import AuthRepository
from task.apps.auth.services import AuthService
from task.apps.users.schemas import UserAddDTO
from task.utils.dependencies import RedisDependency, SessionDependency


async def get_current_user(
    session: SessionDependency,
    x_jwt_token: str = Header(..., alias="X-JWT-Token"),
) -> UserAddDTO:
    if not x_jwt_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    token = x_jwt_token
    try:
        payload = AuthService.decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        user = await AuthRepository.get_by_username(username=username, session=session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


async def get_current_by_session(
    session: SessionDependency,
    redis: RedisDependency,
    x_session: str = Header(..., alias="X-Session"),
):
    username = await redis.get(f"session:{x_session}")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid session"
        )
    user = await AuthRepository.get_by_username(username=username, session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
