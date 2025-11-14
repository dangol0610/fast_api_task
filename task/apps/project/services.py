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
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def get_by_id(self, project_id: int) -> ProjectRelDto:
        project = await self.repository.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectRelDto.model_validate(project)

    async def get_with_params(self, params: ProjectParams) -> ProjectsWithParamsDTO:
        projects_data = await self.repository.get_with_params(params)
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

    async def create(self, project_data: ProjectAddDTO) -> ProjectDTO:
        project = await self.repository.create(project_data)
        if not project:
            raise ValueError("Can not create project")
        return ProjectDTO.model_validate(project)

    async def create_many(self, projects_data: list[ProjectAddDTO]) -> list[ProjectDTO]:
        projects = await self.repository.create_many(projects_data)
        if not projects:
            raise ValueError("Can not create projects")
        return [ProjectDTO.model_validate(project) for project in projects]

    async def update(
        self, project_id: int, project_data: ProjectUpdateDTO
    ) -> ProjectDTO:
        project = await self.repository.update(project_id, project_data)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectDTO.model_validate(project)

    async def delete(self, project_id: int) -> ProjectDTO:
        project = await self.repository.delete(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} not found")
        return ProjectDTO.model_validate(project)
