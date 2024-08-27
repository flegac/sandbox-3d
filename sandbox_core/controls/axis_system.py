from typing import override

from direct.showbase.InputStateGlobal import inputState

from python_ecs.component import Signature
from python_ecs.system import System
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.axis_config import AxisConfig


class AxisSign(Signature):
    param: FloatParam
    axis: AxisConfig


class AxisSystem(System):
    _signature = AxisSign

    @override
    def update_single(self, item: AxisSign):
        axis = item.axis
        param = item.param

        axis.init_events(param)

        param.accel = 0
        if inputState.isSet(f'{axis.name}+'):
            param.accel = axis.power
        elif inputState.isSet(f'{axis.name}-'):
            param.accel = -axis.power
