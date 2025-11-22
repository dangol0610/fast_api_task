from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from task.apps.auth.dependencies import get_current_user
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.auth.services import AuthService
from task.apps.users.schemas import UserAddDTO
from task.utils.dependencies import SessionDependency


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register_user(data: AuthRegisterSchema, session: SessionDependency):
    return await AuthService.register(data=data, session=session)


@auth_router.post("/login")
async def login_user(
    session: SessionDependency, form_data: OAuth2PasswordRequestForm = Depends()
):
    return await AuthService.login(
        username=form_data.username, password=form_data.password, session=session
    )


@auth_router.get("/me")
async def get_me(current_user: UserAddDTO = Depends(get_current_user)):
    return {"user": current_user}
