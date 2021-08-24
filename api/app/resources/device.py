# -*- coding: utf-8 -*-

from db import db
from flask import request
from flask_cors import cross_origin
from flask_restx import Namespace, Resource
from models.device import DeviceModel
from schemas.device import DeviceSchema

# define namespaces
decorators = [cross_origin()]
device_ns = Namespace("device", decorators=decorators)
devices_ns = Namespace("devices", decorators=decorators)

# define schemas
schema = DeviceSchema()
list_schema = DeviceSchema(many=True)

# required by flask_restx for expect
device = device_ns.model("Device", {})


class Device(Resource):
    # get a single device per id
    def get(self, id):
        data = DeviceModel.find_by_id(id)
        if data:
            return schema.dump(data)
        return {"message": "Device not found"}, 404

    # set a device
    @device_ns.expect(device)
    def post(self, id):
        json = request.get_json()
        data = schema.load(json, session=db.session)
        data.save_to_db()
        return schema.dump(data), 200


class Devices(Resource):
    # get all devices
    def get(self):
        return list_schema.dump(DeviceModel.find_all()), 200
