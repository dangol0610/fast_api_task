from fastapi import Request, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt

from task.settings.settings import settings

include_paths = ["/api/users/by_ids", "/api/users/by_id"]


async def auth_middleware(request: Request, call_next):
    if any(
        request.url.path.startswith(endpoint_path) for endpoint_path in include_paths
    ):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Authorization header missing or invalid"},
            )
        token = auth_header.split()[1]
        try:
            payload = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=settings.ALG
            )
            request.state.user = payload
        except JWTError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"},
            )
    response = await call_next(request)
    return response
