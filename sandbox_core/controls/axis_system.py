from typing import override

from direct.showbase.InputStateGlobal import inputState

from python_ecs.signature import Signature
from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_core.controls.axis_config import AxisConfig
from sandbox_core.controls.params.float_param import FloatParam


class AxisSign(Signature):
    param: FloatParam
    axis: AxisConfig


class AxisSystem(System):
    _signature = AxisSign

    @override
    def update_single(self, db: DatabaseAPI, item: AxisSign, dt: float):
        axis = item.axis
        param = item.param

        axis.init_events(param)

        param.accel = 0
        if inputState.isSet(f'{axis.name}+'):
            param.accel = axis.power
        elif inputState.isSet(f'{axis.name}-'):
            param.accel = -axis.power
