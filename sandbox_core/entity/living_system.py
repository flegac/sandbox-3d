from typing import override

from python_ecs.component import Signature
from python_ecs.entity_filter import EntityFilter
from python_ecs.system import System
from python_ecs.update_status import Demography
from sandbox_core.entity.health import Health
from sandbox_core.entity.lifetime import Lifetime


class Living(Signature):
    lifetime: Lifetime
    health: Health

    def is_dead(self):
        if self.lifetime and self.lifetime.is_dead:
            return True
        if self.health and self.health.is_dead:
            return True
        return False


class LivingSystem(System):
    _signature = Living
    _filter_strategy = EntityFilter.requires_any

    @override
    def update_single(self, item: Living):
        if item.is_dead():
            return Demography.remove(item.lifetime.eid)
