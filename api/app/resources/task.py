# -*- coding: utf-8 -*-

from db import db
from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from models.task import TaskModel
from schemas.task import TaskSchema

# define namespaces
decorators = [cross_origin()]
task_ns = Namespace("task", decorators=decorators)
tasks_ns = Namespace("tasks", decorators=decorators)

# define schemas
schema = TaskSchema()
list_schema = TaskSchema(many=True)

# required by flask_restx for expect
task = task_ns.model("Task", {})


class Task(Resource):
    # get a single task per id
    def get(self, id):
        data = TaskModel.find_by_id(id)
        if data:
            return schema.dump(data)
        return {"message": "Task not found"}, 404

    # set a task
    @task_ns.expect(task)
    def post(self, id):
        json = request.get_json()
        data = schema.load(json, session=db.session)
        data.save_to_db()
        return schema.dump(data), 200


class Tasks(Resource):
    # get all tasks
    def get(self):
        return list_schema.dump(TaskModel.find_all()), 200
