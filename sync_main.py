from typing import Any, List, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from sync_models import Base, Project, ProjectType, engine, get_db


# PYDANTIC
class MixinBase(BaseModel):
    id: Optional[str] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserBase(BaseModel):
    username: str


class CreateProjectType(MixinBase):
    name: str

    class Config:
        from_attributes = True


class CreateProject(BaseModel):
    name: str
    code: str
    description: str
    project_type_id: int


class ProjectTypeOut(CreateProjectType):
    projects: Optional[List[Any]] = []

    class Config:
        from_attributes = True


class CreateProject(BaseModel):
    name: str
    code: str
    description: str
    project_type_id: int


# FASTAPI
app = FastAPI()


@app.on_event("startup")
def initialize_db():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database has been successfully initialized!")


@app.post("/project-types")
async def index(type: CreateProjectType, db: Session = Depends(get_db)):
    type = ProjectType(name=type.name)
    db.add(type)
    db.commit()
    db.refresh(type)
    return {"created_project_type": type}


@app.get("/project-types")
def get_projects(db: Session = Depends(get_db)):
    project_types = db.execute(select(ProjectType)).scalars().all()
    return {"project_types": project_types}


@app.post("/projects")
async def index(project: CreateProject, db: Session = Depends(get_db)):
    project = Project(
        name=project.name,
        code=project.code,
        description=project.description,
        project_type_id=project.project_type_id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"created_project": project}


@app.get("/projects")
async def get_projects(db: Session = Depends(get_db)):
    projects = db.execute(select(Project)).scalars().all()
    return {"projects": projects}
