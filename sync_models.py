from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    sessionmaker,
)

# SQLALCHEMY
engine = create_engine(
    "sqlite:///kpi-tracker-db.sqlite3",
    connect_args={"check_same_thread": False},
)
SessionLocal: Session = sessionmaker(engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class BaseMixin(object):
    __mapper_args__ = {"always_refresh": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int] = mapped_column(default=0)
    updated_by: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
