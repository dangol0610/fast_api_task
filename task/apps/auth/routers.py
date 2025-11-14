from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from task.apps.auth.dependencies import get_current_user, get_auth_service
from task.apps.auth.schemas import AuthRegisterSchema
from task.apps.auth.services import AuthService
from task.apps.users.schemas import UserAddDTO


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
async def register_user(
    data: AuthRegisterSchema, service: AuthService = Depends(get_auth_service)
):
    return await service.register(data)


@auth_router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service),
):
    return await service.login(form_data.username, form_data.password)


@auth_router.get("/me")
async def get_me(current_user: UserAddDTO = Depends(get_current_user)):
    return {"user": current_user}
