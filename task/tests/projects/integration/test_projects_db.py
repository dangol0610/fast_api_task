import pytest
from sqlalchemy import select
from task.apps.project.models import Project, ProjectStatus
from task.apps.project.repository import ProjectRepository
from task.apps.project.schemas import ProjectAddDTO, ProjectParams, ProjectUpdateDTO
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO


test_user = UserAddDTO(
    username="test_user",
    email="test_user@mail.ru",
    hashed_password="test_password",
)


@pytest.mark.db
async def test_get_by_id(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    project_dto = ProjectAddDTO(
        name="test_project",
        status=ProjectStatus.NEW,
        description="",
        person_in_charge=user.id,
    )
    project = await ProjectRepository.create(project_dto, setup_db)
    assert project is not None
    project_from_db = await ProjectRepository.get_by_id(project.id, setup_db)
    assert project_from_db is not None
    assert project_from_db.name == project_dto.name


@pytest.mark.db
async def test_get_with_params(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    project_dto = ProjectAddDTO(
        name="test_project",
        status=ProjectStatus.NEW,
        description="",
        person_in_charge=user.id,
    )
    project = await ProjectRepository.create(project_dto, setup_db)
    assert project is not None
    params = ProjectParams(status=ProjectStatus.NEW, person_in_charge=user.id)
    projects = await ProjectRepository.get_with_params(params, setup_db)
    assert projects is not None
    assert projects["total_count"] == 1
    assert projects["projects"][0].name == project_dto.name


@pytest.mark.db
async def test_create(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    project_dto = ProjectAddDTO(
        name="test_project",
        status=ProjectStatus.NEW,
        description="",
        person_in_charge=user.id,
    )
    project = await ProjectRepository.create(project_dto, setup_db)
    assert project is not None
    assert isinstance(project, Project)
    query = select(Project).where(Project.name == project.name)
    result = await setup_db.execute(query)
    project_from_db = result.scalar_one_or_none()
    assert project_from_db is not None
    assert project_from_db.name == project_dto.name


@pytest.mark.db
async def test_create_many(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    projects_dto = [
        ProjectAddDTO(
            name="test_project1",
            status=ProjectStatus.NEW,
            description="",
            person_in_charge=user.id,
        ),
        ProjectAddDTO(
            name="test_project2",
            status=ProjectStatus.NEW,
            description="",
            person_in_charge=user.id,
        ),
    ]
    projects = await ProjectRepository.create_many(projects_dto, setup_db)
    assert projects is not None
    assert len(projects) == len(projects_dto)
    assert all(isinstance(project, Project) for project in projects)

    query = select(Project).where(
        Project.name.in_([project.name for project in projects_dto])
    )
    result = await setup_db.execute(query)
    projects_from_db = result.scalars().all()
    assert len(projects_from_db) == len(projects_dto)
    assert projects_from_db[0].name == projects_dto[0].name
    assert projects_from_db[1].name == projects_dto[1].name


@pytest.mark.db
async def test_update(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    project_dto = ProjectAddDTO(
        name="test_project",
        status=ProjectStatus.NEW,
        description="",
        person_in_charge=user.id,
    )
    project = await ProjectRepository.create(project_dto, setup_db)
    assert project is not None
    project_update_dto = ProjectUpdateDTO(
        name="updated_project",
        status=ProjectStatus.IN_PROGRESS,
        description="updated_description",
    )
    updated_project = await ProjectRepository.update(
        project.id, project_update_dto, setup_db
    )
    assert updated_project is not None
    assert updated_project.name == project_update_dto.name
    assert updated_project.status == project_update_dto.status
    assert updated_project.description == project_update_dto.description


@pytest.mark.db
async def test_delete(setup_db):
    user = await UserRepository.create(test_user, setup_db)
    assert user is not None
    project_dto = ProjectAddDTO(
        name="test_project",
        status=ProjectStatus.NEW,
        description="",
        person_in_charge=user.id,
    )
    project = await ProjectRepository.create(project_dto, setup_db)
    assert project is not None
    await ProjectRepository.delete(project.id, setup_db)
    deleted_project = await ProjectRepository.get_by_id(project.id, setup_db)
    assert deleted_project is None
