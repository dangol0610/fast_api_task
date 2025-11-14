from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from task.apps.auth.connector import Connector
from task.apps.auth.repository import AuthRepository
from task.apps.auth.services import AuthService
from task.apps.users.schemas import UserAddDTO


def get_repository():
    connector = Connector()
    return AuthRepository(connector)


def get_auth_service(repository: AuthRepository = Depends(get_repository)):
    return AuthService(repository)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    service: AuthService = Depends(get_auth_service),
    token: str = Depends(oauth2_scheme),
) -> UserAddDTO:
    try:
        payload = service.decode_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
            )
        username = payload["sub"]
        user = await service.repository.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
