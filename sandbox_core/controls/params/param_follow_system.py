from typing import override

from python_ecs.signature import Signature
from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.params.param_updater import ParamUpdater


class ParamFollow(Signature):
    param: FloatParam
    updater: ParamUpdater


class ParamFollowSystem(System):
    _signature = ParamFollow

    @override
    def update_single(self, db: DatabaseAPI, item: ParamFollow, dt: float):
        item.updater(item.param.current)
