from typing import override

from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox_core.events.event_config import EventConfig


class EventSystem(System):
    _signature = EventConfig

    @override
    def update_single(self, db: DatabaseAPI, item: EventConfig, dt: float):
        for name, action in item.actions.items():
            if item.is_set(name):
                action(True)
            else:
                action(False)

        if hasattr(item, 'update'):
            item.update()
