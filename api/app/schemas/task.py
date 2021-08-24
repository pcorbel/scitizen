# -*- coding: utf-8 -*-

from ma import ma
from models.task import TaskModel


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskModel
        load_instance = True
        include_fk = True
