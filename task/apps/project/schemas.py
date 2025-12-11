from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from task.apps.project.models import ProjectStatus


class ProjectAddDTO(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    status: ProjectStatus
    start_time: datetime = Field(default=datetime.now(timezone.utc))
    end_time: datetime = Field(default=datetime.now(timezone.utc))
    description: Optional[str] = Field(max_length=1000)
    person_in_charge: int

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdateDTO(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=30, default=None)
    status: Optional[ProjectStatus] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: Optional[str] = Field(max_length=1000, default=None)


class ProjectDTO(ProjectAddDTO):
    id: int
    create_time: datetime


class ProjectRelDto(ProjectDTO):
    pass


class ProjectsWithParamsDTO(BaseModel):
    projects: list[ProjectRelDto]
    total_count: int
    has_prev: bool
    has_next: bool

    model_config = ConfigDict(from_attributes=True)


class ProjectSortField(Enum):
    CREATE_TIME = "create_time"
    START_TIME = "start_time"
    END_TIME = "end_time"


class ProjectParams(BaseModel):
    page: int = 1
    page_size: int = 10
    status: Optional[ProjectStatus] = None
    person_in_charge: Optional[int] = None
    sort_field: Optional[ProjectSortField] = None
    sort_desc: bool = False
