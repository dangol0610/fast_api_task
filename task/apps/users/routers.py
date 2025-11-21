from fastapi import APIRouter, Depends, HTTPException, Query

from task.apps.users.services import UserService
from task.apps.auth.dependencies import get_current_user
from task.apps.users.schemas import UserAddDTO, UserDTO, UserRelDto, UserUpdateDTO

user_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@user_router.get("/all")
async def read_all() -> list[UserRelDto]:
    return await UserService.get_all()


@user_router.get("/by_ids")
async def read_by_ids(list_ids: list[int] = Query()) -> list[UserRelDto]:
    return await UserService.get_by_ids(list_ids)


@user_router.get("/by_id/{user_id}")
async def read_by_id(user_id: int) -> UserRelDto:
    return await UserService.get_by_id(user_id)


@user_router.post("/create_one")
async def create_user(
    user: UserAddDTO,
) -> UserDTO:
    try:
        created = await UserService.create_user(user)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/create_many")
async def create_users(
    users: list[UserAddDTO],
) -> list[UserDTO]:
    try:
        created = await UserService.create_many(users)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateDTO,
) -> UserDTO:
    try:
        updated = await UserService.update(user_id, data)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
) -> UserDTO:
    try:
        deleted = await UserService.delete(user_id)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
