# -*- coding: utf-8 -*-

from db import db
from flask import Blueprint, Flask, jsonify
from flask_restx import Api
from ma import ma
from marshmallow import ValidationError
from resources.device import Device, Devices, device_ns, devices_ns
from resources.project import Project, Projects, project_ns, projects_ns
from resources.task import Task, Tasks, task_ns, tasks_ns

# init Flask app
app = Flask(__name__)
blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint, doc="/doc", title="Scitizen API")
app.register_blueprint(blueprint)

# add namespaces to app
api.add_namespace(device_ns)
api.add_namespace(devices_ns)
api.add_namespace(project_ns)
api.add_namespace(projects_ns)
api.add_namespace(task_ns)
api.add_namespace(tasks_ns)

# add resources to namespaces
device_ns.add_resource(Device, "/<string:id>")
devices_ns.add_resource(Devices, "")
project_ns.add_resource(Project, "/<string:id>")
projects_ns.add_resource(Projects, "")
task_ns.add_resource(Task, "/<string:id>")
tasks_ns.add_resource(Tasks, "")

# config SQLAlchemy
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://scitizen:scitizen@localhost:5432/scitizen"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
ma.init_app(app)


# init database
@app.before_first_request
def init_db():
    db.create_all()
    with open("./init.sql") as stream:
        query = stream.read()
    with db.engine.connect() as connection:
        transaction = connection.begin()
        connection.execute(query)
        transaction.commit()


# init error handling
@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400
