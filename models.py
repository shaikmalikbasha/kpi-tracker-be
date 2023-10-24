from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

# SQLALCHEMY
engine = create_async_engine(
    "sqlite+aiosqlite:///kpi-tracker-db.sqlite3",
    connect_args={"check_same_thread": False},
)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class BaseMixin(object):
    __mapper_args__ = {"always_refresh": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(default=0)
    updated_by: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(BaseMixin, Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)


class ProjectType(BaseMixin, Base):
    __tablename__ = "project_type"

    name: Mapped[str] = mapped_column(nullable=False)

    ## Relationship Attributes
    projects: Mapped[List["Project"]] = relationship(
        back_populates="project_type", lazy="selectin"
    )


class Project(BaseMixin, Base):
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    project_type_id: Mapped[int] = mapped_column(ForeignKey("project_type.id"))

    project_type: Mapped["ProjectType"] = relationship(
        back_populates="projects", lazy="selectin"
    )


# class Indicator(BaseMixin, Base):
#     __tablename__ = "indicators"

#     name: Mapped[str] = mapped_column(nullable=False)
#     description: Mapped[str] = mapped_column(nullable=True)


async def get_db_async():
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
