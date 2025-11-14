from fastapi import APIRouter, Depends, HTTPException, status

from task.apps.project.dependencies import get_service
from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)
from task.apps.project.services import ProjectService


project_router = APIRouter(prefix="/projects", tags=["Projects"])


@project_router.get("/all")
async def get_all(
    params: ProjectParams = Depends(), service: ProjectService = Depends(get_service)
) -> ProjectsWithParamsDTO:
    return await service.get_with_params(params)


@project_router.get("/{project_id}")
async def get_by_id(
    project_id: int, service: ProjectService = Depends(get_service)
) -> ProjectRelDto:
    try:
        project = await service.get_by_id(project_id)
        return project
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )


@project_router.post("/create")
async def create_project(
    project_data: ProjectAddDTO, service: ProjectService = Depends(get_service)
) -> ProjectDTO:
    try:
        new_project = await service.create(project_data)
        return new_project
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create project"
        )


@project_router.post("/create_many")
async def create_projects(
    project_data: list[ProjectAddDTO], service: ProjectService = Depends(get_service)
) -> list[ProjectDTO]:
    try:
        new_projects = await service.create_many(project_data)
        return new_projects
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create projects"
        )


@project_router.patch("/update/{project_id}")
async def update_project(
    project_id: int,
    project_data: ProjectUpdateDTO,
    service: ProjectService = Depends(get_service),
) -> ProjectDTO:
    try:
        updated = await service.update(project_id, project_data)
        return updated
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )


@project_router.delete("/delete/{project_id}")
async def delete_project(
    project_id: int, service: ProjectService = Depends(get_service)
) -> ProjectDTO:
    try:
        deleted = await service.delete(project_id)
        return deleted
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
