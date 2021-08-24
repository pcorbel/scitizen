# -*- coding: utf-8 -*-

from ma import ma
from models.project import ProjectModel


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectModel
        load_instance = True
        include_fk = True
