from typing import override

from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_creature.behavior.behavior import Behavior


class BehaviorSystem(System):
    _signature = Behavior

    @override
    def update_single(self, db: DatabaseAPI, item: Behavior, dt: float):
        item.update()
