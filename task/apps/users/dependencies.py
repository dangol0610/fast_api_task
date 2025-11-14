from fastapi import Depends
from task.apps.auth.services import AuthService
from task.apps.users.repository import UserRepository
from task.apps.users.services import UserService
from task.apps.auth.dependencies import get_auth_service


def get_repository() -> UserRepository:
    return UserRepository()


def get_service(
    repository: UserRepository = Depends(get_repository),
    auth_service: AuthService = Depends(get_auth_service),
):
    return UserService(repository=repository, auth_service=auth_service)
