from typing import override

from python_ecs.system import System
from sandbox_creature.behavior.behavior import Behavior


class BehaviorSystem(System):
    _signature = Behavior

    @override
    def update_single(self, item: Behavior):
        if item.is_active:
            item.update()
