# -*- coding: utf-8 -*-

from db import db
from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from models.project import ProjectModel
from schemas.project import ProjectSchema

# define namespaces
decorators = [cross_origin()]
project_ns = Namespace("project", decorators=decorators)
projects_ns = Namespace("projects", decorators=decorators)

# define schemas
schema = ProjectSchema()
list_schema = ProjectSchema(many=True)

# required by flask_restx for expect
project = project_ns.model("Project", {})


class Project(Resource):
    # get a single project per id
    def get(self, id):
        data = ProjectModel.find_by_id(id)
        if data:
            return schema.dump(data)
        return {"message": "Project not found"}, 404

    # set a project
    @project_ns.expect(project)
    def post(self, id):
        json = request.get_json()
        data = schema.load(json, session=db.session)
        data.save_to_db()
        return schema.dump(data), 200


class Projects(Resource):
    # get all projects
    def get(self):
        return list_schema.dump(ProjectModel.find_all()), 200
