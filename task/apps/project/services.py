from task.apps.project.repository import ProjectRepository
from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)


class ProjectService:
    @classmethod
    async def get_by_id(cls, project_id: int) -> ProjectRelDto:
        project = await ProjectRepository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectRelDto.model_validate(project)

    @classmethod
    async def get_with_params(cls, params: ProjectParams) -> ProjectsWithParamsDTO:
        projects_data = await ProjectRepository.get_with_params(params)
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
    async def create(cls, project_data: ProjectAddDTO) -> ProjectDTO:
        project = await ProjectRepository.create(project_data)
        if not project:
            raise ValueError("Can not create project")
        return ProjectDTO.model_validate(project)

    @classmethod
    async def create_many(cls, projects_data: list[ProjectAddDTO]) -> list[ProjectDTO]:
        projects = await ProjectRepository.create_many(projects_data)
        if not projects:
            raise ValueError("Can not create projects")
        return [ProjectDTO.model_validate(project) for project in projects]

    @classmethod
    async def update(
        cls, project_id: int, project_data: ProjectUpdateDTO
    ) -> ProjectDTO:
        project = await ProjectRepository.update(project_id, project_data)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectDTO.model_validate(project)

    @classmethod
    async def delete(cls, project_id: int) -> ProjectDTO:
        project = await ProjectRepository.delete(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectDTO.model_validate(project)
