from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError

from task.apps.auth.repository import AuthRepository
from task.apps.auth.services import AuthService
from task.utils.database import local_session

include_paths = []


async def auth_middleware(request: Request, call_next):
    if any(
        request.url.path.startswith(endpoint_path) for endpoint_path in include_paths
    ):
        async with local_session() as session:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Authorization header missing or invalid"},
                )
            token = auth_header.split()[1]
            try:
                payload = AuthService.decode_token(token)
                username = payload.get("sub")
                if not username:
                    raise JWTError("Invalid token payload")
                user = await AuthRepository.get_by_username(
                    username=username, session=session
                )
                if not user:
                    return JSONResponse(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"detail": "User not found"},
                    )
                request.state.user = user
            except JWTError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Invalid token"},
                )
    response = await call_next(request)
    return response
