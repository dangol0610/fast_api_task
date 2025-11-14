from fastapi import Depends
from task.apps.project.repository import ProjectRepository
from task.apps.project.services import ProjectService


def get_repository() -> ProjectRepository:
    return ProjectRepository()


def get_service(
    repository: ProjectRepository = Depends(get_repository),
) -> ProjectService:
    return ProjectService(repository)
