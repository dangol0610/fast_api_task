from datetime import datetime
from enum import Enum as Enumeration
from sqlalchemy import DateTime, ForeignKey, Integer, String, Enum, Text, func
from task.utils.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ProjectStatus(str, Enumeration):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.NEW, nullable=False
    )
    create_time: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp()
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(Text)
    person_in_charge: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["User"] = relationship("User", back_populates="projects")  # type: ignore # noqa: F821
