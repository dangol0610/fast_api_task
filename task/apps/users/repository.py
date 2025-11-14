from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import selectinload
from task.apps.users.models import User
from task.apps.users.schemas import UserAddDTO, UserUpdateDTO
from task.utils.database import local_session


class UserRepository:
    async def get_all(self) -> list[User]:
        """
        SELECT * FROM users
        SELECT projects.* FROM projects WHERE projects.user_id IN (...)
        """
        async with local_session() as session:
            query = select(User).options(selectinload(User.projects))
            result = await session.execute(query)
            users = result.scalars().all()
            return list(users)

    async def get_by_id(self, id: int) -> User | None:
        """
        SELECT * FROM users
        WHERE id = :id
        SELECT projects.* FROM projects WHERE projects.user_id = :id
        """
        async with local_session() as session:
            query = (
                select(User).options(selectinload(User.projects)).where(User.id == id)
            )
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            if not user:
                return None
            return user

    async def get_by_ids(self, ids: list[int]) -> list[User]:
        """
        SELECT * FROM users
        WHERE id IN :ids
        SELECT projects.* FROM projects WHERE projects.user_id IN (:ids)
        """
        async with local_session() as session:
            query = (
                select(User)
                .options(selectinload(User.projects))
                .where(User.id.in_(ids))
            )
            result = await session.execute(query)
            users = result.scalars().all()
            return list(users)

    async def create(self, user: UserAddDTO) -> User | None:
        """
        INSERT INTO users (...)
        VALUES(:user_data)
        RETURNING *
        """
        async with local_session() as session:
            user_data = user.model_dump()
            stmt = insert(User).values(user_data).returning(User)
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
            return user_res

    async def create_many(self, users: list[UserAddDTO]) -> list[User] | None:
        """
        INSERT INTO users (...)
        VALUES (:users_to_insert)
        RETURNING *
        """
        async with local_session() as session:
            users_to_insert = [user.model_dump() for user in users]
            stmt = insert(User).values(users_to_insert).returning(User)
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalars().all()
            if not user_res:
                return None
            return list(user_res)

    async def update(self, user_id: int, new_user: UserUpdateDTO) -> User | None:
        """
        UPDATE users SET ... WHERE id = :user_id RETURNING *
        """
        async with local_session() as session:
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

    async def delete(self, user_id: int) -> User | None:
        """
        DELETE FROM users WHERE id = :user_id RETURNING *
        """
        async with local_session() as session:
            stmt = delete(User).where(User.id == user_id).returning(User)
            result = await session.execute(stmt)
            await session.commit()
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
            return user_res

    async def get_by_username(self, username: str) -> User | None:
        """
        SELECT * FROM users WHERE username = :username
        """
        async with local_session() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
            return user_res

    async def get_by_email(self, email: str) -> User | None:
        """
        SELECT * FROM users WHERE email = :email
        """
        async with local_session() as session:
            stmt = select(User).where(User.email == email)
            result = await session.execute(stmt)
            user_res = result.scalar_one_or_none()
            if not user_res:
                return None
            return user_res
