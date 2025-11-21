from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from task.apps.auth.dependencies import get_current_user
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.auth.services import AuthService
from task.apps.users.schemas import UserAddDTO


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register_user(data: AuthRegisterSchema):
    return await AuthService.register(data)


@auth_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    return await AuthService.login(form_data.username, form_data.password)


@auth_router.get("/me")
async def get_me(current_user: UserAddDTO = Depends(get_current_user)):
    return {"user": current_user}
