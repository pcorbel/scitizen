# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from db import db
from sqlalchemy.dialects.postgresql import ARRAY


class ProjectModel(db.Model):
    # the name of the table in the database
    __tablename__ = "projects"

    # setup the primary key of the table
    id = db.Column(db.Text, primary_key=True)

    # setup the columns / properties
    avatar = db.Column(db.Text)
    description = db.Column(db.Text)
    general_area = db.Column(db.Text)
    home = db.Column(db.Text)
    image = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    keywords = db.Column(db.Text)
    name = db.Column(db.Text)
    platforms = db.Column(ARRAY(db.Text))
    specific_area = db.Column(db.Text)
    summary = db.Column(db.Text)
    url = db.Column(db.Text, unique=True)
    web_url = db.Column(db.Text)
    weak_authenticator = db.Column(db.Text)

    # setup the pseudo-columns (metadata related to the record)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id) -> "ProjectModel":
        """Find a Project by id

        It is used to find a Project in the database by its id.

        Args:
          _id:
            The id of the Project to find.

        Returns:
          The Project with the corresponding id.
        """

        return db.session.query(ProjectModel).filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["ProjectModel"]:
        """Find all the Projects.

        It is used to return all the Projects available in the database.

        Returns:
          A list of all the Projects available in the database.
        """
        return db.session.query(ProjectModel).all()

    def save_to_db(self) -> None:
        """Save to the database.

        It is used to commit all the changes to the database for persistence.
        """

        db.session.add(self)
        db.session.commit()
