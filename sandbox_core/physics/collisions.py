import random
from functools import cached_property
from typing import override

from loguru import logger

from easy_kit.timing import time_func, timing
from python_ecs.ecs import sim
from python_ecs.signature import Signature
from python_ecs.storage.database_api import DatabaseAPI
from python_ecs.system import System
from sandbox.my_base import base
from sandbox_core.entity.health import Health
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_gui.features.panels.sound_panel import MUSIC_ROOT


class Collision(Signature):
    phys: RigidBody
    health: Health

    @property
    def is_destructible(self):
        if self.health is None:
            return False
        return self.health.is_destructible()


class CollisionSystem(System):
    _signature = Collision

    damage_multiplier: float = 1e-3

    @cached_property
    def physics(self):
        from sandbox_core.physics.phys_system import PhysSystem
        return sim.find(PhysSystem)

    @override
    def update_single(self, db: DatabaseAPI, item: Collision, dt: float):
        if item.health.hit_damage > 0:
            self.on_hit(item)

    @time_func
    def on_hit(self, projectile: Collision):
        with timing('physics.world.contact_test'):
            result = self.physics.world.contact_test(projectile.phys.body)
            contacts = result.getContacts()

        for contact in contacts:
            node1 = contact.getNode1()
            target: RigidBody = node1.getPythonTag('entity')
            if target is None:
                logger.warning(f'collision: unhandled object: {node1}')
                continue
            self.on_hit_damage(projectile, target)

    @time_func
    def on_hit_damage(self, projectile: Collision, target: RigidBody):
        health = target.get(Health)
        if not health or not health.is_destructible():
            return
        damage = self.damage_multiplier * projectile.phys.kinetic_energy * projectile.health.hit_damage
        if damage < .1:
            return

        health.health -= damage
        item = random.choice('ABCDE')
        with timing('base.audio.play_at'):
            base.audio.play_sfx(
                sound=f'{MUSIC_ROOT}/Cool/FX/Hollywood Action/Hollywood Action/Weapon/Misc/Bullet Impact {item}.wav',
                target=projectile.phys.node
            )
