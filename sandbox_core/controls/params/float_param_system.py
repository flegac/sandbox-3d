from typing import override

from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_core.controls.params.float_param import FloatParam


class ParamSystem(System):
    _signature = FloatParam

    @override
    def update_single(self, db: DatabaseAPI, item: FloatParam, dt: float):
        item.update()
