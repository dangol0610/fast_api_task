from fastapi import APIRouter, Depends, HTTPException, status, Query, Request

from task.apps.users.dependencies import get_service
from task.apps.users.services import UserService
from task.apps.auth.dependencies import get_current_user
from task.apps.users.schemas import UserAddDTO, UserDTO, UserRelDto, UserUpdateDTO

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/all")
async def read_all(service: UserService = Depends(get_service)) -> list[UserRelDto]:
    return await service.get_all()


"""
GET-запросы ниже защищены через middleware
их не проверить в Swagger :(
"""


@user_router.get("/by_ids")
async def read_by_ids(
    request: Request,
    list_ids: list[int] = Query(),
    service: UserService = Depends(get_service),
) -> list[UserRelDto]:
    current_user = request.state.user
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return await service.get_by_ids(list_ids)


@user_router.get("/by_id/{user_id}")
async def read_by_id(
    user_id: int, request: Request, service: UserService = Depends(get_service)
) -> UserRelDto:
    current_user = request.state.user
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )
    return await service.get_by_id(user_id)


"""
Запросы ниже защищены OAuth2
"""


@user_router.post("/create_one")
async def create_user(
    user: UserAddDTO,
    service: UserService = Depends(get_service),
    current_user: UserDTO = Depends(get_current_user),
) -> UserDTO:
    try:
        created = await service.create_user(user)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/create_many")
async def create_users(
    users: list[UserAddDTO],
    service: UserService = Depends(get_service),
    current_user: UserDTO = Depends(get_current_user),
) -> list[UserDTO]:
    try:
        created = await service.create_many(users)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateDTO,
    service: UserService = Depends(get_service),
    current_user: UserDTO = Depends(get_current_user),
) -> UserDTO:
    try:
        updated = await service.update(user_id, data)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service),
    current_user: UserDTO = Depends(get_current_user),
) -> UserDTO:
    try:
        deleted = await service.delete(user_id)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
