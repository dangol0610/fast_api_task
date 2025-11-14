from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from task.apps.project.schemas import ProjectRelDto


class UserUpdateDTO(BaseModel):
    username: Optional[str] = Field(min_length=3, max_length=50)
    email: Optional[EmailStr]

    model_config = ConfigDict(from_attributes=True)


class UserAddDTO(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserDTO(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserRelDto(UserDTO):
    projects: List["ProjectRelDto"] = []
