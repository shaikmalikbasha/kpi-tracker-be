from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base, Project, ProjectType, User, engine, get_db_async


# PYDANTIC
class UserBase(BaseModel):
    username: str


class CreateProjectType(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CreateProject(BaseModel):
    name: str
    code: str
    description: str
    project_type_id: int


# FASTAPI
app = FastAPI()


@app.on_event("startup")
async def initialize_db():
    async with engine.begin() as conn:
        print("Initializing database...")
        await conn.run_sync(Base.metadata.create_all)
        print("Database has been successfully initialized!")


@app.post("/project-types")
async def index(p_type: CreateProjectType, db: AsyncSession = Depends(get_db_async)):
    p_type_obj = ProjectType(name=p_type.name)
    db.add(p_type_obj)
    await db.commit()
    await db.refresh(p_type_obj)
    return {"created_project_type": p_type_obj}


@app.get("/project-types")
async def get_projects(db: AsyncSession = Depends(get_db_async)):
    results = await db.execute(select(ProjectType))
    project_types = results.scalars().all()
    return {"project_types": project_types}


@app.post("/users")
async def index(user: UserBase, db: AsyncSession = Depends(get_db_async)):
    db_user = User(username=user.username)
    db.add(db_user)
    print("User has added successfully, now committing the changes...")
    await db.commit()
    print("Commited, Refreshing...")
    await db.refresh(db_user)
    print(f"Added User: {db_user}")
    return db_user


@app.get("/users")
async def get_users(db: AsyncSession = Depends(get_db_async)):
    print("Fething the data from the database...")
    results = await db.execute(select(User))
    print("Results fetched!")
    users = results.scalars().all()
    print(f"Users: {users}")
    return {"users": users}


@app.post("/projects", status_code=202)
async def index(project: CreateProject, db: AsyncSession = Depends(get_db_async)):
    project = Project(
        name=project.name,
        code=project.code,
        description=project.description,
        project_type_id=project.project_type_id,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return {"created_project": project}


@app.get("/projects")
async def get_projects(db: AsyncSession = Depends(get_db_async)):
    results = await db.execute(select(Project))
    projects = results.scalars().all()
    return {"projects": projects}
