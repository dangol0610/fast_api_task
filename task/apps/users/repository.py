from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload
from task.apps.users.models import User
from task.apps.users.schemas import UserAddDTO, UserUpdateDTO
from task.utils.dependencies import SessionDependency


class UserRepository:
    @classmethod
    async def get_all(cls, session: SessionDependency) -> list[User]:
        """
        SELECT * FROM users
        SELECT projects.* FROM projects WHERE projects.user_id IN (...)
        """
        query = select(User).options(selectinload(User.projects))
        result = await session.execute(query)
        users = result.scalars().all()
        return list(users)

    @classmethod
    async def get_by_id(cls, id: int, session: SessionDependency) -> User | None:
        """
        SELECT * FROM users
        WHERE id = :id
        SELECT projects.* FROM projects WHERE projects.user_id = :id
        """
        query = select(User).options(selectinload(User.projects)).where(User.id == id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return None
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
        result = await session.execute(query)
        users = result.scalars().all()
        return list(users)

    @classmethod
    async def create(cls, user: UserAddDTO, session: SessionDependency) -> User | None:
        """
        INSERT INTO users (...)
        VALUES(:user_data)
        RETURNING *
        """
        user_data = user.model_dump()
        stmt = insert(User).values(user_data).returning(User)
        result = await session.execute(stmt)
        await session.commit()
        user_res = result.scalar_one_or_none()
        if not user_res:
            return None
        return user_res

    @classmethod
    async def create_many(
        cls, users: list[UserAddDTO], session: SessionDependency
    ) -> list[User] | None:
        """
        INSERT INTO users (...)
        VALUES (:users_to_insert)
        RETURNING *
        """
        users_to_insert = [user.model_dump() for user in users]
        stmt = insert(User).values(users_to_insert).returning(User)
        result = await session.execute(stmt)
        await session.commit()
        user_res = result.scalars().all()
        if not user_res:
            return None
        return list(user_res)

    @classmethod
    async def update(
        cls, user_id: int, new_user: UserUpdateDTO, session: SessionDependency
    ) -> User | None:
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
        result = await session.execute(stmt)
        await session.commit()
        user_res = result.scalar_one_or_none()
        if not user_res:
            return None
        return user_res

    @classmethod
    async def delete(cls, user_id: int, session: SessionDependency) -> User | None:
        """
        DELETE FROM users WHERE id = :user_id RETURNING *
        """
        stmt = delete(User).where(User.id == user_id).returning(User)
        result = await session.execute(stmt)
        await session.commit()
        user_res = result.scalar_one_or_none()
        if not user_res:
            return None
        return user_res

    @classmethod
    async def get_by_username(
        cls, username: str, session: SessionDependency
    ) -> User | None:
        """
        SELECT * FROM users WHERE username = :username
        """
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user_res = result.scalar_one_or_none()
        if not user_res:
            return None
        return user_res

    @classmethod
    async def get_by_email(cls, email: str, session: SessionDependency) -> User | None:
        """
        SELECT * FROM users WHERE email = :email
        """
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user_res = result.scalar_one_or_none()
        if not user_res:
            return None
        return user_res
