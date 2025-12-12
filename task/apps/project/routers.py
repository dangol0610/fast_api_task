from typing import Annotated
from fastapi import APIRouter, Depends

from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)
from task.apps.project.services import ProjectService
from task.apps.auth.dependencies import get_current_by_session, get_current_user
from task.utils.dependencies import RedisDependency, SessionDependency


project_router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@project_router.get("/all")
async def get_all(
    session: SessionDependency,
    params: ProjectParams = Depends(),
) -> ProjectsWithParamsDTO:
    return await ProjectService.get_with_params(params=params, session=session)


@project_router.get("/{project_id}")
async def get_by_id(session: SessionDependency, project_id: int) -> ProjectRelDto:
    return await ProjectService.get_by_id(project_id=project_id, session=session)


@project_router.post("/create")
async def create_project(
    project_data: ProjectAddDTO,
    session: SessionDependency,
    redis: RedisDependency,
    session_header: Annotated[str, Depends(get_current_by_session)],
    token: Annotated[str, Depends(get_current_user)],
) -> ProjectDTO:
    new_project = await ProjectService.create(
        project_data=project_data,
        session=session,
        redis=redis,
    )
    return new_project


@project_router.post("/create_many")
async def create_projects(
    project_data: list[ProjectAddDTO],
    session: SessionDependency,
    redis: RedisDependency,
    session_header: Annotated[str, Depends(get_current_by_session)],
    token: Annotated[str, Depends(get_current_user)],
) -> list[ProjectDTO]:
    new_projects = await ProjectService.create_many(
        projects_data=project_data,
        session=session,
        redis=redis,
    )
    return new_projects


@project_router.patch("/update/{project_id}")
async def update_project(
    project_id: int,
    project_data: ProjectUpdateDTO,
    session: SessionDependency,
    redis: RedisDependency,
    session_header: Annotated[str, Depends(get_current_by_session)],
    token: Annotated[str, Depends(get_current_user)],
) -> ProjectDTO:
    updated = await ProjectService.update(
        project_id=project_id,
        project_data=project_data,
        session=session,
        redis=redis,
    )
    return updated


@project_router.delete("/delete/{project_id}")
async def delete_project(
    project_id: int,
    session: SessionDependency,
    redis: RedisDependency,
    session_header: Annotated[str, Depends(get_current_by_session)],
    token: Annotated[str, Depends(get_current_user)],
) -> ProjectDTO:
    deleted = await ProjectService.delete(
        project_id=project_id,
        session=session,
        redis=redis,
    )
    return deleted
