from task.apps.project.repository import ProjectRepository
from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)
from task.utils.dependencies import RedisDependency, SessionDependency


class ProjectService:
    @classmethod
    async def get_by_id(
        cls,
        project_id: int,
        session: SessionDependency,
    ) -> ProjectRelDto:
        project = await ProjectRepository.get_by_id(id=project_id, session=session)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectRelDto.model_validate(project)

    @classmethod
    async def get_with_params(
        cls, params: ProjectParams, session: SessionDependency
    ) -> ProjectsWithParamsDTO:
        projects_data = await ProjectRepository.get_with_params(
            params=params, session=session
        )
        projects = [
            ProjectRelDto.model_validate(project)
            for project in projects_data["projects"]
        ]
        result = {
            "projects": projects,
            "total_count": projects_data["total_count"],
            "has_prev": projects_data["has_prev"],
            "has_next": projects_data["has_next"],
        }
        return ProjectsWithParamsDTO.model_validate(result)

    @classmethod
    async def create(
        cls,
        project_data: ProjectAddDTO,
        session: SessionDependency,
        redis: RedisDependency,
    ) -> ProjectDTO:
        project = await ProjectRepository.create(project=project_data, session=session)
        if not project:
            raise ValueError("Can not create project")
        await redis.delete("users:all")
        await redis.delete(f"user:{project.person_in_charge}")
        return ProjectDTO.model_validate(project)

    @classmethod
    async def create_many(
        cls,
        projects_data: list[ProjectAddDTO],
        session: SessionDependency,
        redis: RedisDependency,
    ) -> list[ProjectDTO]:
        projects = await ProjectRepository.create_many(
            projects=projects_data, session=session
        )
        if not projects:
            raise ValueError("Can not create projects")
        await redis.delete("users:all")
        return [ProjectDTO.model_validate(project) for project in projects]

    @classmethod
    async def update(
        cls,
        project_id: int,
        project_data: ProjectUpdateDTO,
        session: SessionDependency,
        redis: RedisDependency,
    ) -> ProjectDTO:
        project = await ProjectRepository.update(
            id=project_id,
            project=project_data,
            session=session,
        )
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        await redis.delete("users:all")
        await redis.delete(f"user:{project.person_in_charge}")
        return ProjectDTO.model_validate(project)

    @classmethod
    async def delete(
        cls,
        project_id: int,
        session: SessionDependency,
        redis: RedisDependency,
    ) -> ProjectDTO:
        project = await ProjectRepository.delete(id=project_id, session=session)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        await redis.delete("users:all")
        await redis.delete(f"user:{project.person_in_charge}")
        return ProjectDTO.model_validate(project)
