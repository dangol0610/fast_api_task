from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.orm import selectinload
from task.apps.project.models import Project
from task.apps.project.schemas import ProjectAddDTO, ProjectParams, ProjectUpdateDTO
from task.utils.dependencies import SessionDependency


class ProjectRepository:
    @classmethod
    async def get_by_id(cls, id: int, session: SessionDependency) -> Project | None:
        """
        SELECT *
        FROM projects
        WHERE projects.id = :id
        SELECT users WHERE users.id IN (projects.person_in_charge)
        """
        query = (
            select(Project).options(selectinload(Project.user)).where(Project.id == id)
        )
        result = await session.execute(query)
        project = result.scalar_one_or_none()
        if not project:
            return None
        return project

    @classmethod
    async def get_with_params(
        cls, params: ProjectParams, session: SessionDependency
    ) -> dict:
        """
        SELECT * FROM projects
        WHERE status = :status AND person_in_charge = :person_in_charge
        ORDER BY :sort_field ASC|DESC
        LIMIT :page_size OFFSET :offset
        SELECT users WHERE users.id IN (projects.person_in_charge)
        """
        query = select(Project).options(selectinload(Project.user))

        if params.status:
            query = query.where(Project.status == params.status)

        if params.person_in_charge:
            query = query.where(Project.person_in_charge == params.person_in_charge)

        if params.sort_field:
            column = getattr(Project, params.sort_field.value)
            query = query.order_by(column.desc() if params.sort_desc else column.asc())

        count_query = select(func.count()).select_from(query.subquery())
        total_count = await session.scalar(count_query)
        if not total_count:
            total_count = 0

        query = query.offset((params.page - 1) * params.page_size).limit(
            params.page_size
        )
        result = await session.execute(query)
        projects_res = result.scalars().all()
        return {
            "projects": projects_res,
            "total_count": total_count,
            "has_prev": params.page > 1,
            "has_next": params.page * params.page_size < total_count,
        }

    @classmethod
    async def create(
        cls, project: ProjectAddDTO, session: SessionDependency
    ) -> Project | None:
        """
        INSERT INTO projects (name, status, start_time, end_time, description, person_in_charge)
        VALUES (:name, :status, :start_time, :end_time, :description, :person_in_charge)
        RETURNING *
        """
        project_data = project.model_dump()
        stmt = insert(Project).values(project_data).returning(Project)
        result = await session.execute(stmt)
        await session.commit()
        project_res = result.scalar_one_or_none()
        if not project_res:
            return None
        return project_res

    @classmethod
    async def create_many(
        cls, projects: list[ProjectAddDTO], session: SessionDependency
    ) -> list[Project] | None:
        """
        INSERT INTO projects (name, status, start_time, end_time, description, person_in_charge)
        VALUES (:name, :status, :start_time, :end_time, :description, :person_in_charge), ...
        RETURNING *
        """
        projects_data = [project.model_dump() for project in projects]
        stmt = insert(Project).values(projects_data).returning(Project)
        result = await session.execute(stmt)
        await session.commit()
        projects_res = result.scalars().all()
        if not projects_res:
            return None
        return list(projects_res)

    @classmethod
    async def update(
        cls, id: int, project: ProjectUpdateDTO, session: SessionDependency
    ) -> Project | None:
        """
        UPDATE projects
        SET name = :name, status = :status, start_time = :start_time, end_time = :end_time, description = :description, person_in_charge = :person_in_charge
        WHERE id = :id
        RETURNING *
        """
        project_data = project.model_dump(exclude_unset=True)
        stmt = (
            update(Project)
            .where(Project.id == id)
            .values(project_data)
            .returning(Project)
        )
        result = await session.execute(stmt)
        await session.commit()
        project_res = result.scalar_one_or_none()
        if not project_res:
            return None
        return project_res

    @classmethod
    async def delete(cls, id: int, session: SessionDependency) -> Project | None:
        """
        DELETE FROM projects
        WHERE id = :id
        RETURNING *
        """
        stmt = delete(Project).where(Project.id == id).returning(Project)
        result = await session.execute(stmt)
        await session.commit()
        project_res = result.scalar_one_or_none()
        if not project_res:
            return None
        return project_res
