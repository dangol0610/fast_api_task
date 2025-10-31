from fastapi import HTTPException, status
from task.apps.users.repository import UserRepository
from task.apps.users.schemas import (
    UserCreateSchema,
    UserFullSchema,
    UserReadSchema,
    UserUpdateSchema,
)


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all(self) -> list[UserReadSchema]:
        users = self.repository.get_all()
        return [UserReadSchema.model_validate(user.model_dump()) for user in users]

    def get_by_id(self, id: int) -> UserReadSchema:
        user = self.repository.get_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserReadSchema.model_validate(user.model_dump())

    def get_by_id_list(self, list_id: list[int]) -> list[UserReadSchema]:
        users = self.repository.get_by_ids(list_id)
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
            )
        return [UserReadSchema.model_validate(user.model_dump()) for user in users]

    def create(self, data: UserCreateSchema) -> UserReadSchema:
        existing = self.repository.get_all()
        new_id = max([u.id for u in existing], default=0) + 1
        new_user = UserFullSchema(id=new_id, **data.model_dump())
        created = self.repository.create(new_user)
        return UserReadSchema.model_validate(created.model_dump())

    def create_many(self, users_data: list[UserCreateSchema]) -> list[UserReadSchema]:
        existing = self.repository.get_all()
        start_new_id = max([u.id for u in existing], default=0) + 1
        new_users = []
        for i, user in enumerate(users_data):
            new_user = UserFullSchema(id=start_new_id + i, **user.model_dump())
            new_users.append(new_user)
        created = self.repository.create_many(new_users)
        return [UserReadSchema.model_validate(user.model_dump()) for user in created]

    def update(self, id: int, update_data: UserUpdateSchema) -> UserReadSchema:
        user = self.repository.get_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user_data = user.model_dump()
        updated_fields = update_data.model_dump(exclude_unset=True)
        user_data.update(updated_fields)
        updated_user = UserFullSchema(**user_data)
        self.repository.update(id, updated_user)
        return UserReadSchema.model_validate(updated_user.model_dump())

    def delete(self, id: int) -> UserReadSchema:
        deleted = self.repository.delete(id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserReadSchema.model_validate(deleted.model_dump())
