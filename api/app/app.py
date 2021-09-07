# -*- coding: utf-8 -*-

from typing import List

from database import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Device, Project, Task, TaskWithProject
from sqlmodel import Session, SQLModel, select

# init fastapi
app: FastAPI = FastAPI()

# init CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# mount api endpoint
api: FastAPI = FastAPI(title="Scitizen")
app.mount("/api", api)


@app.on_event("startup")
def on_startup() -> None:
    """Setup event on app.

    It is used to create the database and the tables.
    """

    SQLModel.metadata.create_all(engine)


@api.post("/devices/{device_uuid}", response_model=Device)
def upsert_device(device_uuid: str, device: Device) -> Device:
    """Upsert a device.

    It is used to create a device in the database if it does not already exists,
    else it is used to update the existing one.

    Args:
      device_uuid:
        The uuid of the device to upsert.
      device:
        The device data.

    Returns:
      The upserted device.
    """

    with Session(engine) as session:
        # check if the device exists
        statement = select(Device).where(Device.uuid == device_uuid)
        result = session.exec(statement).first()

        # if not, create it
        if result is None:
            result = device

        # sync the data
        for key, value in device.dict(exclude_unset=True).items():
            setattr(result, key, value)

        # persist the data to the database
        session.add(result)
        session.commit()
        session.refresh(result)

        return result


@api.get("/devices/{device_uuid}", response_model=Device)
def select_device(device_uuid: str):
    """Select a device.

    It is used to get a device data from the database.

    Args:
      device_uuid:
        The uuid of the device to get the data from.

    Returns:
      The device data.
    """

    with Session(engine) as session:
        statement = select(Device).where(Device.uuid == device_uuid)
        result = session.exec(statement).first()
        return result


@api.get("/devices", response_model=List[Device])
def select_devices():
    """Select all devices.

    It is used to get all devices data from the database.

    Returns:
      All devices data.
    """

    with Session(engine) as session:
        statement = select(Device)
        results = session.exec(statement).all()
        return results


@api.post("/projects/{project_uuid}", response_model=Project)
def upsert_project(project_uuid: str, project: Project) -> Project:
    """Upsert a project.

    It is used to create a project in the database if it does not already exists,
    else it is used to update the existing one.

    Args:
      project_uuid:
        The uuid of the project to upsert.
      project:
        The project data.

    Returns:
      The upserted project.
    """

    with Session(engine) as session:
        # check if the project exists
        statement = select(Project).where(Project.uuid == project_uuid)
        result = session.exec(statement).first()

        # if not, create it
        if result is None:
            result = project

        # sync the data
        for key, value in project.dict(exclude_unset=True).items():
            setattr(result, key, value)

        # persist the data to the database
        session.add(result)
        session.commit()
        session.refresh(result)

        return result


@api.get("/projects/{project_uuid}", response_model=Project)
def select_project(project_uuid: str):
    """Select a project.

    It is used to get a project data from the database.

    Args:
      project_uuid:
        The uuid of the project to get the data from.

    Returns:
      The project data.
    """

    with Session(engine) as session:
        statement = select(Project).where(Project.uuid == project_uuid)
        result = session.exec(statement).first()
        return result


@api.get("/projects", response_model=List[Project])
def select_projects():
    """Select all projects.

    It is used to get all projects data from the database.

    Returns:
      All projects data.
    """

    with Session(engine) as session:
        statement = select(Project)
        results = session.exec(statement).all()
        return results


@api.post("/tasks/{task_uuid}", response_model=Task)
def upsert_task(task_uuid: str, task: Task) -> Task:
    """Upsert a task.

    It is used to create a task in the database if it does not already exists,
    else it is used to update the existing one.

    Args:
      task_uuid:
        The uuid of the task to upsert.
      task:
        The task data.

    Returns:
      The upserted task.
    """

    with Session(engine) as session:
        # check if the task exists
        statement = select(Task).where(Task.uuid == task_uuid)
        result = session.exec(statement).first()

        # if not, create it
        if result is None:
            result = task

        # sync the data
        for key, value in task.dict(exclude_unset=True).items():
            setattr(result, key, value)

        # persist the data to the database
        session.add(result)
        session.commit()
        session.refresh(result)

        return result


@api.get("/tasks/{task_uuid}", response_model=TaskWithProject)
def select_task(task_uuid: str):
    """Select a task.

    It is used to get a task data from the database.

    Args:
      task_uuid:
        The uuid of the task to get the data from.

    Returns:
      The task data.
    """

    with Session(engine) as session:
        statement = select(Task, Project).join(Project).where(Task.uuid == task_uuid)
        task, project = session.exec(statement).first()  # type: ignore
        result = TaskWithProject()
        for key, value in task.dict().items():
            setattr(result, key, value)
        result.project = project
        return result


@api.get("/tasks", response_model=List[TaskWithProject])
def select_tasks():
    """Select all tasks.

    It is used to get all tasks data from the database.

    Returns:
      All tasks data.
    """

    with Session(engine) as session:
        statement = select(Task, Project).join(Project)
        results = session.exec(statement).all()
        tasks = []
        for task, project in results:
            result = TaskWithProject()
            for key, value in task.dict().items():
                setattr(result, key, value)
            result.project = project
            tasks.append(result)
        return tasks


@api.put("/tasks/clean")
def clean_tasks():
    """Clean all tasks.

    It is used to run maintenance queries on the database in order to keep
    consistent data on tasks.
    """

    with Session(engine) as session:
        with open("./data/clean_failed_tasks.sql", "r", encoding="utf-8") as stream:
            statement = stream.read()
        session.exec(statement)

        with open("./data/clean_succeeded_tasks.sql", "r", encoding="utf-8") as stream:
            statement = stream.read()
        session.exec(statement)

        session.commit()
