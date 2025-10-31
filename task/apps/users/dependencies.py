from fastapi import Depends
from task.apps.users.models import ConnectionManager, UsersStorage
from task.apps.users.repository import UserRepository
from task.apps.users.services import UserService


def get_repository():
    model = UsersStorage()
    connection = ConnectionManager()
    return UserRepository(model, connection)


def get_service(repository: UserRepository = Depends(get_repository)):
    return UserService(repository)
