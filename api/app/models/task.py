# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from db import db
from models.project import ProjectModel


class TaskModel(db.Model):
    # setup the name of the table in the database
    __tablename__ = "tasks"

    # setup the primary key of the table
    id = db.Column(db.Text, primary_key=True)

    # setup the columns / properties
    active_task_state = db.Column(db.Text)
    app_version_num = db.Column(db.Float)
    bytes_received = db.Column(db.Float)
    bytes_sent = db.Column(db.Float)
    checkpoint_cpu_time = db.Column(db.Float)
    completed_at = db.Column(db.DateTime)
    current_cpu_time = db.Column(db.Float)
    elapsed_time = db.Column(db.Float)
    estimated_cpu_time_remaining = db.Column(db.Float)
    exit_code = db.Column(db.Float)
    exit_statement = db.Column(db.Text)
    fraction_done = db.Column(db.Float)
    name = db.Column(db.Text)
    page_fault_rate = db.Column(db.Float)
    pid = db.Column(db.Float)
    plan_class = db.Column(db.Text)
    platform = db.Column(db.Text)
    progress_rate = db.Column(db.Float)
    project_url = db.Column(db.Text, db.ForeignKey("projects.url"))
    project_name = db.Column(db.Text)
    project_web_url = db.Column(db.Text)
    received_at = db.Column(db.DateTime)
    report_deadline_at = db.Column(db.DateTime)
    scheduler_state = db.Column(db.Text)
    set_size = db.Column(db.Float)
    slot = db.Column(db.Float)
    slot_path = db.Column(db.Text)
    state = db.Column(db.Text)
    swap_size = db.Column(db.Float)
    version_num = db.Column(db.Float)
    wu_name = db.Column(db.Text)

    # setup the pseudo-columns (metadata related to the record)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # setup relationship
    project = db.relationship(ProjectModel, backref="tasks", uselist=False)

    @classmethod
    def find_by_id(cls, _id) -> "TaskModel":
        """Find a Task by id.

        It is used to find a Task in the database by its id.

        Args:
          _id:
            The id of the Task to find.

        Returns:
          The Task with the corresponding id.
        """

        return db.session.query(TaskModel).filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["TaskModel"]:
        """Find all the Tasks.

        It is used to return all the Tasks available in the database.

        Returns:
          A list of all the Tasks available in the database.
        """

        rows = db.session.query(TaskModel, ProjectModel).join(ProjectModel).all()
        tasks = []
        for task, project in rows:
            task.project_name = project.name
            task.project_web_url = project.web_url
            tasks.append(task)
        return tasks

    def save_to_db(self) -> None:
        """Save to the database.

        It is used to commit all the changes to the database for persistence.
        """

        db.session.add(self)
        db.session.commit()
