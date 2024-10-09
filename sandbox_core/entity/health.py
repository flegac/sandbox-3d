from typing import override

from python_ecs.component import Component
from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System


class Health(Component):
    health: float | None = None
    hit_damage: float = 0.0

    def is_destructible(self):
        return self.health is not None

    @property
    def is_dead(self):
        if self.health is None:
            return False
        return self.health < 0


class HealthSystem(System):
    _signature = Health

    @override
    def update_single(self, db: DatabaseAPI, item: Health, dt: float):
        if item.is_dead:
            db.destroy_all([item])
