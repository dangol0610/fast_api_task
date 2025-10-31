from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr


class UserCreateSchema(UserBaseSchema):
    password: str | None = Field(min_length=6)


class UserReadSchema(UserBaseSchema):
    id: int


class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserFullSchema(UserBaseSchema):
    id: int
    password: str = Field(min_length=6)
