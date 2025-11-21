from fastapi import APIRouter, Depends, HTTPException, status

from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)
from task.apps.project.services import ProjectService
from task.apps.auth.dependencies import get_current_user


project_router = APIRouter(
    prefix="/projects", tags=["Projects"], dependencies=[Depends(get_current_user)]
)


@project_router.get("/all")
async def get_all(params: ProjectParams = Depends()) -> ProjectsWithParamsDTO:
    return await ProjectService.get_with_params(params)


@project_router.get("/{project_id}")
async def get_by_id(project_id: int) -> ProjectRelDto:
    try:
        project = await ProjectService.get_by_id(project_id)
        return project
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )


@project_router.post("/create")
async def create_project(project_data: ProjectAddDTO) -> ProjectDTO:
    try:
        new_project = await ProjectService.create(project_data)
        return new_project
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create project"
        )


@project_router.post("/create_many")
async def create_projects(project_data: list[ProjectAddDTO]) -> list[ProjectDTO]:
    try:
        new_projects = await ProjectService.create_many(project_data)
        return new_projects
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can not create projects"
        )


@project_router.patch("/update/{project_id}")
async def update_project(
    project_id: int,
    project_data: ProjectUpdateDTO,
) -> ProjectDTO:
    try:
        updated = await ProjectService.update(project_id, project_data)
        return updated
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )


@project_router.delete("/delete/{project_id}")
async def delete_project(project_id: int) -> ProjectDTO:
    try:
        deleted = await ProjectService.delete(project_id)
        return deleted
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
