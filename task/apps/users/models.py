from sqlalchemy import Integer, String
from task.utils.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    projects: Mapped[list["Project"]] = relationship(  # noqa: F821 # type: ignore
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
