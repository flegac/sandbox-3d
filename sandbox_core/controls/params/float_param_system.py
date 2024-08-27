from typing import override

from python_ecs.system import System
from sandbox_core.controls.params.float_param import FloatParam


class ParamSystem(System):
    _signature = FloatParam

    @override
    def update_single(self, item: FloatParam):
        item.update()
