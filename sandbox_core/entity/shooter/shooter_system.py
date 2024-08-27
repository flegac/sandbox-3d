from functools import cached_property
from typing import override

from python_ecs.system import System
from sandbox_core._utils.ray.physic_ray import PhysicRay
from sandbox_core.entity.shooter.shooter_config import ShooterConfig


class ShooterSystem(System):
    _signature = ShooterConfig

    @cached_property
    def caster(self):
        return PhysicRay()

    @override
    def update_single(self, item: ShooterConfig):
        if item.is_firing and not item.is_unavailable():
            item.shoot_at(self.caster.mouse_ray())
