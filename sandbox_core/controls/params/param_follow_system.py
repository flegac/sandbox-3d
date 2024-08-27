from typing import override

from python_ecs.component import Signature
from python_ecs.system import System
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.params.param_updater import ParamUpdater


class ParamFollow(Signature):
    param: FloatParam
    updater: ParamUpdater


class ParamFollowSystem(System):
    _signature = ParamFollow

    @override
    def update_single(self, item: ParamFollow):
        item.updater(item.param.current)
