from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock
import pytest

from task.apps.project.models import ProjectStatus
from task.apps.project.schemas import (
    ProjectAddDTO,
    ProjectDTO,
    ProjectParams,
    ProjectRelDto,
    ProjectUpdateDTO,
    ProjectsWithParamsDTO,
)
from task.apps.project.services import ProjectService


@pytest.mark.service
async def test_get_by_id(mocker):
    expected_obj = SimpleNamespace(
        id=1,
        name="test",
        status=ProjectStatus.NEW,
        create_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="",
        person_in_charge=1,
    )
    session = AsyncMock()
    mock_get_by_id = mocker.patch(
        "task.apps.project.services.ProjectRepository.get_by_id",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.get_by_id(project_id=1, session=session)
    assert isinstance(result, ProjectRelDto)
    assert result.name == expected_obj.name
    mock_get_by_id.assert_awaited_once_with(id=1, session=session)


@pytest.mark.service
async def test_get_with_params(mocker):
    params = ProjectParams(
        page=1,
        page_size=5,
        status=ProjectStatus.NEW,
    )
    expected_project = SimpleNamespace(
        id=1,
        name="test",
        status=ProjectStatus.NEW,
        create_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="",
        person_in_charge=1,
    )
    expected_obj = {
        "projects": [expected_project],
        "total_count": 1,
        "has_prev": False,
        "has_next": False,
    }

    session = AsyncMock()
    mock_get_with_params = mocker.patch(
        "task.apps.project.services.ProjectRepository.get_with_params",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.get_with_params(params=params, session=session)
    assert isinstance(result, ProjectsWithParamsDTO)
    assert result.projects[0].name == "test"
    assert result.total_count == 1
    assert result.has_prev is False
    assert result.has_next is False
    mock_get_with_params.assert_awaited_once_with(params=params, session=session)


@pytest.mark.service
async def test_create(mocker):
    project_data = ProjectAddDTO(
        name="test",
        status=ProjectStatus.NEW,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="",
        person_in_charge=1,
    )
    expected_obj = SimpleNamespace(
        id=1,
        name="test",
        status=ProjectStatus.NEW,
        create_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="",
        person_in_charge=1,
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    mock_create = mocker.patch(
        "task.apps.project.services.ProjectRepository.create",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.create(
        project_data=project_data, session=session, redis=fake_redis
    )
    assert isinstance(result, ProjectDTO)
    assert result.name == expected_obj.name
    mock_create.assert_awaited_once_with(project=project_data, session=session)


@pytest.mark.service
async def test_create_many(mocker):
    project_data = [
        ProjectAddDTO(
            name="test",
            status=ProjectStatus.NEW,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc),
            description="",
            person_in_charge=1,
        ),
        ProjectAddDTO(
            name="test2",
            status=ProjectStatus.NEW,
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc),
            description="",
            person_in_charge=1,
        ),
    ]
    expected_obj = [
        SimpleNamespace(
            id=1,
            name="test",
            status=ProjectStatus.NEW,
            create_time=datetime.now(timezone.utc),
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc),
            description="",
            person_in_charge=1,
        ),
        SimpleNamespace(
            id=2,
            name="test2",
            status=ProjectStatus.NEW,
            create_time=datetime.now(timezone.utc),
            start_time=datetime.now(timezone.utc),
            end_time=datetime.now(timezone.utc),
            description="",
            person_in_charge=1,
        ),
    ]
    session = AsyncMock()
    fake_redis = AsyncMock()
    mock_create_many = mocker.patch(
        "task.apps.project.services.ProjectRepository.create_many",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.create_many(
        projects_data=project_data,
        session=session,
        redis=fake_redis,
    )
    assert all(isinstance(project, ProjectDTO) for project in result)
    assert len(result) == 2
    assert result[0].name == "test"
    assert result[1].name == "test2"
    mock_create_many.assert_awaited_once_with(projects=project_data, session=session)


@pytest.mark.service
async def test_update(mocker):
    id = 1
    update_data = ProjectUpdateDTO(
        name="test_updated",
        status=ProjectStatus.NEW,
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="updated",
    )
    expected_obj = SimpleNamespace(
        id=1,
        name="test_updated",
        status=ProjectStatus.NEW,
        create_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="updated",
        person_in_charge=1,
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    mock_update = mocker.patch(
        "task.apps.project.services.ProjectRepository.update",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.update(
        project_id=id,
        project_data=update_data,
        session=session,
        redis=fake_redis,
    )
    assert isinstance(result, ProjectDTO)
    assert result.name == "test_updated"
    assert result.description == "updated"
    mock_update.assert_awaited_once_with(id=1, project=update_data, session=session)


@pytest.mark.service
async def test_delete(mocker):
    id = 1
    expected_obj = SimpleNamespace(
        id=1,
        name="test",
        status=ProjectStatus.NEW,
        create_time=datetime.now(timezone.utc),
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc),
        description="updated",
        person_in_charge=1,
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    mock_delete = mocker.patch(
        "task.apps.project.services.ProjectRepository.delete",
        AsyncMock(return_value=expected_obj),
    )
    result = await ProjectService.delete(
        project_id=id,
        session=session,
        redis=fake_redis,
    )
    assert isinstance(result, ProjectDTO)
    assert result.id == 1
    assert result.name == "test"
    mock_delete.assert_awaited_once_with(id=1, session=session)
