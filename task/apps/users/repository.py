from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from task.apps.users.models import User
from task.apps.users.schemas import UserAddDTO, UserUpdateDTO
from task.utils.dependencies import SessionDependency
from task.utils.exceptions import DatabaseException, ItemNotFoundException


class UserRepository:
    @classmethod
    async def get_all(cls, session: SessionDependency) -> list[User]:
        """
        SELECT * FROM users
        SELECT projects.* FROM projects WHERE projects.user_id IN (...)
        """
        query = select(User).options(selectinload(User.projects))
        try:
            result = await session.execute(query)
            users = result.scalars().all()
        except SQLAlchemyError:
            raise DatabaseException
        return list(users)

    @classmethod
    async def get_by_id(cls, id: int, session: SessionDependency) -> User:
        """
        SELECT * FROM users
        WHERE id = :id
        SELECT projects.* FROM projects WHERE projects.user_id = :id
        """
        query = select(User).options(selectinload(User.projects)).where(User.id == id)
        try:
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                raise ItemNotFoundException
        except SQLAlchemyError:
            raise DatabaseException
        return user

    @classmethod
    async def get_by_ids(cls, ids: list[int], session: SessionDependency) -> list[User]:
        """
        SELECT * FROM users
        WHERE id IN :ids
        SELECT projects.* FROM projects WHERE projects.user_id IN (:ids)
        """
        query = (
            select(User).options(selectinload(User.projects)).where(User.id.in_(ids))
        )
        try:
            result = await session.execute(query)
            users = result.scalars().all()
        except SQLAlchemyError:
            raise DatabaseException
        return list(users)

    @classmethod
    async def create(cls, user: UserAddDTO, session: SessionDependency) -> User:
        """
        INSERT INTO users (...)
        VALUES(:user_data)
        RETURNING *
        """
        user_data = user.model_dump()
        stmt = insert(User).values(user_data).returning(User)
        try:
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalar_one()
        except SQLAlchemyError:
            raise DatabaseException
        return user_res

    @classmethod
    async def create_many(
        cls, users: list[UserAddDTO], session: SessionDependency
    ) -> list[User]:
        """
        INSERT INTO users (...)
        VALUES (:users_to_insert)
        RETURNING *
        """
        users_to_insert = [user.model_dump() for user in users]
        stmt = insert(User).values(users_to_insert).returning(User)
        try:
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalars().all()
        except SQLAlchemyError:
            raise DatabaseException
        return list(user_res)

    @classmethod
    async def update(
        cls, user_id: int, new_user: UserUpdateDTO, session: SessionDependency
    ) -> User:
        """
        UPDATE users SET ... WHERE id = :user_id RETURNING *
        """
        user_to_update = new_user.model_dump(exclude_unset=True)
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(user_to_update)
            .returning(User)
        )
        try:
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalar_one_or_none()
            if not user_res:
                raise ItemNotFoundException
        except SQLAlchemyError:
            raise DatabaseException
        return user_res

    @classmethod
    async def delete(cls, user_id: int, session: SessionDependency) -> User:
        """
        DELETE FROM users WHERE id = :user_id RETURNING *
        """
        stmt = delete(User).where(User.id == user_id).returning(User)
        try:
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalar_one_or_none()
            if not user_res:
                raise ItemNotFoundException
        except SQLAlchemyError:
            raise DatabaseException
        return user_res

    @classmethod
    async def get_by_username(
        cls, username: str, session: SessionDependency
    ) -> User | None:
        """
        SELECT * FROM users WHERE username = :username
        """
        stmt = select(User).where(User.username == username)
        try:
            result = await session.execute(stmt)
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
        except SQLAlchemyError:
            raise DatabaseException
        return user_res

    @classmethod
    async def get_by_email(cls, email: str, session: SessionDependency) -> User | None:
        """
        SELECT * FROM users WHERE email = :email
        """
        stmt = select(User).where(User.email == email)
        try:
            result = await session.execute(stmt)
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
        except SQLAlchemyError:
            raise DatabaseException
        return user_res
