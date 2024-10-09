from typing import override

import time

from python_ecs.component import Component
from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System


class Lifetime(Component):
    lifetime: float | None = None
    birth: float | None = None

    def reset(self):
        self.birth = time.time()

    @property
    def is_dead(self):
        if self.lifetime is None:
            return False
        if self.birth is None:
            self.reset()
        return time.time() > self.birth + self.lifetime


class LifeTimeSystem(System):
    _signature = Lifetime

    @override
    def update_single(self, db: DatabaseAPI, item: Lifetime, dt: float):
        if item.is_dead:
            db.destroy_all([item])
