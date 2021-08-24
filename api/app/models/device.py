# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List

from db import db
from sqlalchemy.dialects.postgresql import ARRAY


class DeviceModel(db.Model):
    # the name of the table in the database
    __tablename__ = "devices"

    # setup the primary key of the table
    id = db.Column(db.Text, primary_key=True)

    # setup the columns / properties
    name = db.Column(db.Text)
    type = db.Column(db.Text)
    arch = db.Column(db.Text)
    cpid = db.Column(db.Text)
    cpu_type = db.Column(db.Text)
    cpu_architecture = db.Column(db.Text)
    cpu_features = db.Column(ARRAY(db.Text))
    processor_count = db.Column(db.Integer)
    coprocessor_count = db.Column(db.Integer)
    product_name = db.Column(db.Text)
    floating_point_speed = db.Column(db.Float)
    integer_speed = db.Column(db.Float)
    total_disk_space = db.Column(db.Float)
    free_disk_space = db.Column(db.Float)
    swap_space = db.Column(db.Float)
    domain_name = db.Column(db.Text)
    operating_system_version = db.Column(db.Text)
    boinc_version = db.Column(db.Text)
    scitizen_version = db.Column(db.Text)

    # setup the pseudo-columns (metadata related to the record)
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    @classmethod
    def find_by_id(cls, _id) -> "DeviceModel":
        """Find a Device by id

        It is used to find a Device in the database by its id.

        Args:
          _id:
            The id of the Device to find.

        Returns:
          The Device with the corresponding id.
        """

        return db.session.query(DeviceModel).filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["DeviceModel"]:
        """Find all the Devices.

        It is used to return all the Devices available in the database.

        Returns:
          A list of all the Devices available in the database.
        """

        return db.session.query(DeviceModel).all()

    def save_to_db(self) -> None:
        """Save to the database.

        It is used to commit all the changes to the database for persistence.
        """

        db.session.add(self)
        db.session.commit()
