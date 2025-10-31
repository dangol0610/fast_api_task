from fastapi import APIRouter, Depends, Query

from task.apps.users.dependencies import get_service
from task.apps.users.schemas import UserCreateSchema, UserReadSchema, UserUpdateSchema
from task.apps.users.services import UserService
from task.apps.auth.dependencies import oauth2_scheme


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/all")
async def read_all(service: UserService = Depends(get_service)) -> list[UserReadSchema]:
    return service.get_all()


"""
GET-запросы ниже защищены через middleware
"""


@user_router.get("/by_ids")
async def read_by_ids(
    list_ids: list[int] = Query(), service: UserService = Depends(get_service)
) -> list[UserReadSchema]:
    return service.get_by_id_list(list_ids)


@user_router.get("/by_id/{user_id}")
async def read_by_id(
    user_id: int, service: UserService = Depends(get_service)
) -> UserReadSchema:
    return service.get_by_id(user_id)


"""
Запросы ниже защищены OAuth2
"""


@user_router.post("/create_one")
async def create_user(
    user: UserCreateSchema,
    service: UserService = Depends(get_service),
    token: str = Depends(oauth2_scheme),
) -> UserReadSchema:
    return service.create(user)


@user_router.post("/create_many")
async def create_users(
    users: list[UserCreateSchema],
    service: UserService = Depends(get_service),
    token: str = Depends(oauth2_scheme),
) -> list[UserReadSchema]:
    return service.create_many(users)


@user_router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateSchema,
    service: UserService = Depends(get_service),
    token: str = Depends(oauth2_scheme),
) -> UserReadSchema:
    return service.update(user_id, data)


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_service),
    token: str = Depends(oauth2_scheme),
) -> UserReadSchema:
    return service.delete(user_id)
