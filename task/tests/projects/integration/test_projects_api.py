from datetime import datetime, timezone
from unittest.mock import AsyncMock
from fastapi.encoders import jsonable_encoder
import pytest

from task.apps.project.models import ProjectStatus
from task.apps.project.schemas import (
    ProjectDTO,
    ProjectRelDto,
    ProjectsWithParamsDTO,
)


@pytest.mark.api
async def test_get_all(client, mocker):
    expected_project = ProjectsWithParamsDTO(
        projects=[
            ProjectRelDto(
                name="test",
                status=ProjectStatus.NEW,
                start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                description="test",
                person_in_charge=1,
                id=1,
                create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            )
        ],
        total_count=1,
        has_prev=False,
        has_next=False,
    )
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.get_with_params",
        AsyncMock(return_value=expected_project),
    )
    response = client.get("/api/projects/all")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(expected_project)
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_get_by_id(client, mocker):
    expected_project = ProjectRelDto(
        name="test",
        status=ProjectStatus.NEW,
        start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        description="test",
        person_in_charge=1,
        id=1,
        create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.get_by_id",
        AsyncMock(return_value=expected_project),
    )
    response = client.get("/api/projects/1")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(expected_project)
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_create_project(client, mocker):
    expected_project = ProjectDTO(
        name="test",
        status=ProjectStatus.NEW,
        start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        description="test",
        person_in_charge=1,
        id=1,
        create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.create",
        AsyncMock(return_value=expected_project),
    )
    responce = client.post(
        "/api/projects/create",
        json={
            "name": "test",
            "status": "NEW",
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T00:00:00Z",
            "description": "test",
            "person_in_charge": 1,
        },
    )
    assert responce.status_code == 200
    assert responce.json() == jsonable_encoder(expected_project)
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_create_projects(client, mocker):
    expected_projects = [
        ProjectDTO(
            name="test",
            status=ProjectStatus.NEW,
            start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            description="test",
            person_in_charge=1,
            id=1,
            create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ),
        ProjectDTO(
            name="test2",
            status=ProjectStatus.NEW,
            start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
            description="test2",
            person_in_charge=1,
            id=2,
            create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        ),
    ]
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.create_many",
        AsyncMock(return_value=expected_projects),
    )
    response = client.post(
        "/api/projects/create_many",
        json=[
            {
                "name": "test",
                "status": "NEW",
                "start_time": "2025-01-01T00:00:00Z",
                "end_time": "2025-01-01T00:00:00Z",
                "description": "test",
                "person_in_charge": 1,
            },
            {
                "name": "test2",
                "status": "NEW",
                "start_time": "2025-01-01T00:00:00Z",
                "end_time": "2025-01-01T00:00:00Z",
                "description": "test2",
                "person_in_charge": 1,
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(expected_projects)
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_update(client, mocker):
    expected_project = ProjectDTO(
        name="test",
        status=ProjectStatus.NEW,
        start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        description="test",
        person_in_charge=1,
        id=1,
        create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.update",
        return_value=expected_project,
    )
    response = client.patch(
        "/api/projects/update/1",
        json={
            "name": "test",
            "status": "NEW",
            "start_time": "2025-01-01T00:00:00Z",
            "end_time": "2025-01-01T00:00:00Z",
            "description": "test",
            "person_in_charge": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(expected_project)
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_delete(client, mocker):
    expected_project = ProjectDTO(
        name="test",
        status=ProjectStatus.NEW,
        start_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        end_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        description="test",
        person_in_charge=1,
        id=1,
        create_time=datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
    )
    mock_service = mocker.patch(
        "task.apps.project.routers.ProjectService.delete",
        return_value=expected_project,
    )
    response = client.delete("/api/projects/delete/1")
    assert response.status_code == 200
    assert response.json() == jsonable_encoder(expected_project)
    mock_service.assert_awaited_once()
