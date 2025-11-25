from unittest.mock import AsyncMock
import pytest

from task.apps.users.schemas import UserDTO, UserRelDto


@pytest.mark.api
async def test_get_all(client, mocker):
    expected_user = UserRelDto(
        id=1,
        username="test",
        email="test@test.com",
        projects=[],
    )
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.get_all",
        AsyncMock(return_value=[expected_user]),
    )
    response = client.get("/api/users/all")
    assert response.status_code == 200
    assert response.json() == [expected_user.model_dump()]
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_get_by_ids(client, mocker):
    expected_users = [
        UserRelDto(
            id=1,
            username="test",
            email="test@test.com",
            projects=[],
        ),
        UserRelDto(
            id=2,
            username="test2",
            email="test2@test.com",
            projects=[],
        ),
    ]
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.get_by_ids",
        AsyncMock(return_value=expected_users),
    )
    response = client.get("/api/users/by_ids?list_ids=1&list_ids=2")
    assert response.status_code == 200
    assert response.json() == [user.model_dump() for user in expected_users]
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_get_by_id(client, mocker):
    expected_user = UserRelDto(
        id=1,
        username="test",
        email="test@test.com",
        projects=[],
    )
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.get_by_id",
        AsyncMock(return_value=expected_user),
    )
    response = client.get("/api/users/by_id/1")
    assert response.status_code == 200
    assert response.json() == expected_user.model_dump()
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_create(client, mocker):
    expected_user = UserDTO(
        id=1,
        username="test",
        email="test@test.com",
    )
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.create_user",
        AsyncMock(return_value=expected_user),
    )
    response = client.post(
        "/api/users/create_one",
        json={
            "username": "test",
            "email": "test@test.com",
            "hashed_password": "test",
        },
    )
    assert response.status_code == 200
    assert response.json() == expected_user.model_dump()
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_create_many(client, mocker):
    expected_users = [
        UserDTO(
            id=1,
            username="test",
            email="test@test.com",
        ),
        UserDTO(
            id=2,
            username="test2",
            email="test2@test.com",
        ),
    ]
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.create_many",
        AsyncMock(return_value=expected_users),
    )
    response = client.post(
        "/api/users/create_many",
        json=[
            {
                "username": "test",
                "email": "test@test.com",
                "hashed_password": "test",
            },
            {
                "username": "test2",
                "email": "test2@test.com",
                "hashed_password": "test2",
            },
        ],
    )
    assert response.status_code == 200
    assert response.json() == [user.model_dump() for user in expected_users]
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_update(client, mocker):
    expected_user = UserDTO(
        id=1,
        username="updated_test",
        email="updated@test.com",
    )
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.update",
        AsyncMock(return_value=expected_user),
    )
    response = client.patch(
        "/api/users/1",
        json={
            "username": "updated_test",
            "email": "updated@test.com",
        },
    )
    assert response.status_code == 200
    assert response.json() == expected_user.model_dump()
    mock_service.assert_awaited_once()


@pytest.mark.api
async def test_delete(client, mocker):
    expected_user = UserDTO(
        id=1,
        username="test",
        email="test@test.com",
    )
    mock_service = mocker.patch(
        "task.apps.users.routers.UserService.delete",
        AsyncMock(return_value=expected_user),
    )
    response = client.delete("/api/users/1")
    assert response.status_code == 200
    assert response.json() == expected_user.model_dump()
    mock_service.assert_awaited_once()
