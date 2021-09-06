# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Optional

from sqlmodel import Column, DateTime, Field, Relationship, SQLModel


class Device(SQLModel, table=True):  # type: ignore
    """The Device model.

    It is used to model a device.
    """

    # setup the primary key of the table
    uuid: str = Field(primary_key=True)

    # setup the columns / properties
    name: Optional[str]
    type: Optional[str]
    arch: Optional[str]
    cpid: Optional[str]
    cpu_type: Optional[str]
    cpu_architecture: Optional[str]
    cpu_features: Optional[str]
    processor_count: Optional[int]
    coprocessor_count: Optional[int]
    product_name: Optional[str]
    floating_point_speed: Optional[float]
    integer_speed: Optional[float]
    total_disk_space: Optional[float]
    free_disk_space: Optional[float]
    swap_space: Optional[float]
    domain_name: Optional[str]
    operating_system_version: Optional[str]
    boinc_version: Optional[str]
    scitizen_version: Optional[str]

    # setup the pseudo-columns (metadata related to the record)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), default=datetime.utcnow, name="_created_at")
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=datetime.utcnow, name="_updated_at")
    )


class Project(SQLModel, table=True):  # type: ignore
    """The Project model.

    It is used to model a project.
    """

    # setup the primary key of the table
    uuid: str = Field(primary_key=True)

    # setup the columns / properties
    name: Optional[str]
    avatar: Optional[str]
    description: Optional[str]
    general_area: Optional[str]
    home: Optional[str]
    image: Optional[str]
    is_active: Optional[bool] = True
    keywords: Optional[str]
    name: Optional[str]  # type: ignore
    platforms: Optional[str]
    specific_area: Optional[str]
    summary: Optional[str]
    url: Optional[str]
    web_url: Optional[str]
    weak_authenticator: Optional[str]

    # setup the pseudo-columns (metadata related to the record)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), default=datetime.utcnow, name="_created_at")
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=datetime.utcnow, name="_updated_at")
    )

    # setup the relationship
    task: Optional["Task"] = Relationship(back_populates="project_rel")


class Task(SQLModel, table=True):  # type: ignore
    """The Task model.

    It is used to model a task.
    """

    # setup the primary key of the table
    uuid: str = Field(primary_key=True)

    # setup the columns / properties
    active_task_state: Optional[str]
    app_version_num: Optional[float]
    bytes_received: Optional[float]
    bytes_sent: Optional[float]
    checkpoint_cpu_time: Optional[float]
    completed_at: Optional[datetime]
    current_cpu_time: Optional[float]
    elapsed_time: Optional[float]
    estimated_cpu_time_remaining: Optional[float]
    exit_code: Optional[float]
    exit_statement: Optional[str]
    fraction_done: Optional[float]
    name: Optional[str]
    page_fault_rate: Optional[float]
    pid: Optional[float]
    plan_class: Optional[str]
    platform: Optional[str]
    progress_rate: Optional[float]
    received_at: Optional[datetime]
    report_deadline_at: Optional[datetime]
    scheduler_state: Optional[str]
    set_size: Optional[float]
    slot: Optional[float]
    slot_path: Optional[str]
    state: Optional[str]
    swap_size: Optional[float]
    version_num: Optional[float]
    wu_name: Optional[str]

    # setup the pseudo-columns (metadata related to the record)
    created_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), default=datetime.utcnow, name="_created_at")
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(DateTime(), onupdate=datetime.utcnow, name="_updated_at")
    )

    # setup the relationship
    project_url: Optional[str] = Field(foreign_key="project.url")
    project_rel: Optional[Project] = Relationship(back_populates="task")


class TaskWithProject(Task):
    """The TaskWithProject model.

    It is used to model a task linked to a project,
    so the API will be able in one GET to fetch a task with the linked project.
    """

    # setup the columns / properties
    project: Optional[Project]
