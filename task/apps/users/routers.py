from fastapi import APIRouter, Depends, HTTPException, Query

from task.apps.users.services import UserService
from task.apps.auth.dependencies import get_current_user
from task.apps.users.schemas import UserAddDTO, UserDTO, UserRelDto, UserUpdateDTO
from task.utils.dependencies import SessionDependency

user_router = APIRouter(
    prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)]
)


@user_router.get("/all")
async def read_all(session: SessionDependency) -> list[UserRelDto]:
    return await UserService.get_all(session=session)


@user_router.get("/by_ids")
async def read_by_ids(
    session: SessionDependency,
    list_ids: list[int] = Query(),
) -> list[UserRelDto]:
    return await UserService.get_by_ids(user_ids=list_ids, session=session)


@user_router.get("/by_id/{user_id}")
async def read_by_id(
    user_id: int,
    session: SessionDependency,
) -> UserRelDto:
    return await UserService.get_by_id(user_id=user_id, session=session)


@user_router.post("/create_one")
async def create_user(
    user: UserAddDTO,
    session: SessionDependency,
) -> UserDTO:
    try:
        created = await UserService.create_user(user_data=user, session=session)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.post("/create_many")
async def create_users(
    users: list[UserAddDTO],
    session: SessionDependency,
) -> list[UserDTO]:
    try:
        created = await UserService.create_many(users_data=users, session=session)
        return created
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.patch("/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateDTO,
    session: SessionDependency,
) -> UserDTO:
    try:
        updated = await UserService.update(id=user_id, user_data=data, session=session)
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: SessionDependency,
) -> UserDTO:
    try:
        deleted = await UserService.delete(id=user_id, session=session)
        return deleted
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
