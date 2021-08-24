# -*- coding: utf-8 -*-

from ma import ma
from models.device import DeviceModel


class DeviceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DeviceModel
        load_instance = True
        include_fk = True
