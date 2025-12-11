from unittest.mock import AsyncMock, Mock, call
import pytest
from task.apps.users.models import User
from task.apps.users.schemas import UserAddDTO, UserDTO, UserRelDto, UserUpdateDTO
from task.apps.users.services import UserService


@pytest.mark.service
async def test_get_all(mocker):
    expected_obj = [
        User(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
        ),
        User(
            id=2,
            username="testuser2",
            email="test2@example.com",
            hashed_password="hashed_password2",
        ),
    ]
    session = AsyncMock()
    fake_redis = AsyncMock()
    fake_redis.get = AsyncMock(return_value=None)
    fake_redis.set = AsyncMock()
    mock_get_all = mocker.patch(
        "task.apps.users.services.UserRepository.get_all",
        AsyncMock(return_value=expected_obj),
    )
    result = await UserService.get_all(session, redis=fake_redis)
    assert all(isinstance(user, UserRelDto) for user in result)
    assert result[0].username == "testuser"
    assert result[1].username == "testuser2"
    mock_get_all.assert_awaited_once_with(session=session)


@pytest.mark.service
async def test_get_by_id(mocker):
    expected_obj = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    fake_redis.get = AsyncMock(return_value=None)
    fake_redis.set = AsyncMock()
    mock_get_by_id = mocker.patch(
        "task.apps.users.services.UserRepository.get_by_id",
        AsyncMock(return_value=expected_obj),
    )
    result = await UserService.get_by_id(1, session, redis=fake_redis)
    assert isinstance(result, UserRelDto)
    assert result.username == "testuser"
    mock_get_by_id.assert_awaited_once_with(id=1, session=session)


@pytest.mark.service
async def test_get_by_ids(mocker):
    ids = [1, 2]
    expected_obj = [
        User(
            id=1,
            username="testuser",
            email="test@example.com",
            hashed_password="hashed_password",
        ),
        User(
            id=2,
            username="testuser2",
            email="test2@example.com",
            hashed_password="hashed_password2",
        ),
    ]
    session = AsyncMock()
    mock_get_by_ids = mocker.patch(
        "task.apps.users.services.UserRepository.get_by_ids",
        AsyncMock(return_value=expected_obj),
    )
    result = await UserService.get_by_ids(ids, session)
    assert all(isinstance(user, UserRelDto) for user in result)
    assert len(result) == 2
    assert result[0].username == "testuser"
    assert result[1].username == "testuser2"
    mock_get_by_ids.assert_awaited_once_with(ids=ids, session=session)


@pytest.mark.service
async def test_create_user(mocker):
    user_data = UserAddDTO(
        username="testuser",
        hashed_password="testpassword",
        email="test@example.com",
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    user_obj = User(
        id=1,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
    )
    mock_hash_password = mocker.patch(
        "task.apps.users.services.AuthService.hash_password",
        Mock(return_value="hashed_password"),
    )
    mock_create_user = mocker.patch(
        "task.apps.users.services.UserRepository.create",
        AsyncMock(return_value=user_obj),
    )
    result = await UserService.create_user(user_data, session, redis=fake_redis)
    assert isinstance(result, UserDTO)
    mock_hash_password.assert_called_once_with("testpassword")
    mock_create_user.assert_awaited_once_with(user=user_data, session=session)


@pytest.mark.service
async def test_create_user_invalid(mocker):
    user_data = UserAddDTO(
        username="testuser",
        hashed_password="testpassword",
        email="test@example.com",
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    mock_hash_password = mocker.patch(
        "task.apps.users.services.AuthService.hash_password",
        Mock(return_value="hashed_password"),
    )
    mock_create_user = mocker.patch(
        "task.apps.users.services.UserRepository.create",
        AsyncMock(return_value=None),
    )
    with pytest.raises(ValueError):
        await UserService.create_user(user_data, session, fake_redis)
    mock_hash_password.assert_called_once_with("testpassword")
    mock_create_user.assert_awaited_once_with(user=user_data, session=session)


@pytest.mark.service
async def test_create_many(mocker):
    users_data = [
        UserAddDTO(
            username="testuser1",
            hashed_password="testpassword1",
            email="test1@example.com",
        ),
        UserAddDTO(
            username="testuser2",
            hashed_password="testpassword2",
            email="test2@example.com",
        ),
    ]
    session = AsyncMock()
    expected_objs = [
        User(
            id=1,
            username="testuser1",
            email="test1@example.com",
            hashed_password="hashed_password1",
        ),
        User(
            id=2,
            username="testuser2",
            email="test2@example.com",
            hashed_password="hashed_password2",
        ),
    ]
    fake_redis = AsyncMock()
    mock_hash_password = mocker.patch(
        "task.apps.users.services.AuthService.hash_password",
        Mock(side_effect=["hashed_password1", "hashed_password2"]),
    )
    mock_create_many = mocker.patch(
        "task.apps.users.services.UserRepository.create_many",
        AsyncMock(return_value=expected_objs),
    )
    result = await UserService.create_many(users_data, session, fake_redis)
    assert all(isinstance(user, UserDTO) for user in result)
    mock_hash_password.assert_has_calls([call("testpassword1"), call("testpassword2")])
    mock_create_many.assert_called_once_with(users=users_data, session=session)


@pytest.mark.service
async def test_update(mocker):
    user_id = 1
    user_data = UserUpdateDTO(username="newname", email="new@mail.com")
    session = AsyncMock()
    expected_obj = User(
        id=1,
        username="newname",
        email="new@mail.com",
        hashed_password="hashed_password",
    )
    fake_redis = AsyncMock()
    mocked_update = mocker.patch(
        "task.apps.users.services.UserRepository.update",
        AsyncMock(return_value=expected_obj),
    )
    result = await UserService.update(user_id, user_data, session, fake_redis)
    assert isinstance(result, UserDTO)
    assert result.username == "newname"
    assert result.email == "new@mail.com"
    mocked_update.assert_awaited_once_with(
        user_id=1,
        new_user=user_data,
        session=session,
    )


@pytest.mark.service
async def test_delete(mocker):
    user_id = 1
    expected_obj = User(
        id=1,
        username="testname",
        email="test@mail.com",
        hashed_password="hashed_password",
    )
    session = AsyncMock()
    fake_redis = AsyncMock()
    mocked_delete = mocker.patch(
        "task.apps.users.services.UserRepository.delete",
        AsyncMock(return_value=expected_obj),
    )
    result = await UserService.delete(user_id, session, fake_redis)
    assert isinstance(result, UserDTO)
    assert result.username == "testname"
    assert result.email == "test@mail.com"
    mocked_delete.assert_awaited_once_with(user_id=user_id, session=session)


@pytest.mark.service
async def test_delete_not_found(mocker):
    user_id = 1
    session = AsyncMock()
    fake_redis = AsyncMock()
    mocked_delete = mocker.patch(
        "task.apps.users.services.UserRepository.delete",
        AsyncMock(return_value=None),
    )
    with pytest.raises(ValueError):
        await UserService.delete(user_id, session, fake_redis)
    mocked_delete.assert_awaited_once_with(user_id=user_id, session=session)
