import pytest
from sqlalchemy import select
from task.apps.users.models import User
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import UserAddDTO, UserUpdateDTO


@pytest.mark.db
async def test_get_all(setup_db):
    users_dto = [
        UserAddDTO(
            username="test_user1",
            email="test_user1@mail.ru",
            hashed_password="test_password1",
        ),
        UserAddDTO(
            username="test_user2",
            email="test_user2@mail.ru",
            hashed_password="test_password2",
        ),
    ]

    await UserRepository.create_many(users_dto, setup_db)
    users = await UserRepository.get_all(setup_db)

    assert len(users) == 2
    assert all(isinstance(user, User) for user in users)

    assert users[0].username == users_dto[0].username
    assert users[1].username == users_dto[1].username


@pytest.mark.db
async def test_get_by_id(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )
    user = await UserRepository.create(user_dto, setup_db)
    assert user is not None
    user_from_db = await UserRepository.get_by_id(user.id, setup_db)
    assert user_from_db is not None
    assert user_from_db.username == user_dto.username


@pytest.mark.db
async def test_get_by_ids(setup_db):
    users_dto = [
        UserAddDTO(
            username="test_user1",
            email="test_user1@mail.ru",
            hashed_password="test_password1",
        ),
        UserAddDTO(
            username="test_user2",
            email="test_user2@mail.ru",
            hashed_password="test_password2",
        ),
    ]
    users = await UserRepository.create_many(users_dto, setup_db)
    assert users is not None
    user_ids = [user.id for user in users]
    users_from_db = await UserRepository.get_by_ids(user_ids, setup_db)
    assert len(users_from_db) == len(users_dto)
    assert users_from_db[0].username == users_dto[0].username
    assert users_from_db[1].username == users_dto[1].username


@pytest.mark.db
async def test_create(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )

    user = await UserRepository.create(user_dto, setup_db)

    assert user is not None
    assert isinstance(user, User)
    assert user.username == user_dto.username
    assert user.email == user_dto.email

    query = select(User).where(User.id == user.id)
    result = await setup_db.execute(query)
    user_in_db = result.scalar_one_or_none()

    assert user_in_db.username == user_dto.username


@pytest.mark.db
async def test_create_many(setup_db):
    users_dto = [
        UserAddDTO(
            username="test_user1",
            email="test_user1@mail.ru",
            hashed_password="test_password1",
        ),
        UserAddDTO(
            username="test_user2",
            email="test_user2@mail.ru",
            hashed_password="test_password2",
        ),
    ]

    users = await UserRepository.create_many(users_dto, setup_db)

    assert users is not None
    assert len(users) == len(users_dto)
    assert all(isinstance(user, User) for user in users)

    query = select(User).where(User.id.in_([user.id for user in users]))
    result = await setup_db.execute(query)
    users_in_db = result.scalars().all()

    assert len(users_in_db) == len(users_dto)
    assert users_in_db[0].username == users_dto[0].username
    assert users_in_db[1].username == users_dto[1].username


@pytest.mark.db
async def test_update(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )
    user = await UserRepository.create(user_dto, setup_db)
    assert user is not None
    user_update_dto = UserUpdateDTO(
        username="updated_user",
        email="updated_user@mail.ru",
    )
    updated_user = await UserRepository.update(user.id, user_update_dto, setup_db)
    assert updated_user is not None
    assert updated_user.username == user_update_dto.username
    assert updated_user.email == user_update_dto.email


@pytest.mark.db
async def test_delete(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )
    user = await UserRepository.create(user_dto, setup_db)
    assert user is not None

    query = select(User).where(User.username == user_dto.username)
    result = await setup_db.execute(query)
    user_in_db = result.scalar_one_or_none()
    assert user_in_db is not None

    await UserRepository.delete(user_in_db.id, setup_db)
    query = select(User).where(User.username == user_dto.username)
    result = await setup_db.execute(query)
    user_in_db = result.scalar_one_or_none()

    assert user_in_db is None


@pytest.mark.db
async def test_get_by_username(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )
    user = await UserRepository.create(user_dto, setup_db)
    assert user is not None
    user_from_db = await UserRepository.get_by_username(user.username, setup_db)
    assert user_from_db is not None
    assert user_from_db.username == user.username


@pytest.mark.db
async def test_get_by_email(setup_db):
    user_dto = UserAddDTO(
        username="test_user",
        email="test_user@mail.ru",
        hashed_password="test_password",
    )
    user = await UserRepository.create(user_dto, setup_db)
    assert user is not None
    user_from_db = await UserRepository.get_by_email(user.email, setup_db)
    assert user_from_db is not None
    assert user_from_db.email == user.email
