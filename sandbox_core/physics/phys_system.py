from functools import cached_property
from typing import override

from direct.showbase.ShowBaseGlobal import globalClock
from loguru import logger
from panda3d.bullet import BulletWorld, BulletDebugNode
from panda3d.core import Vec3, NodePath, BitMask32

from easy_kit.timing import time_func
from python_ecs.entity_filter import EntityFilter
from python_ecs.id_generator import IdGenerator
from python_ecs.storage.database import Database
from python_ecs.system import System
from sandbox.my_base import base
from sandbox_core.physics.ray_collision import RayCollision
from sandbox_core.physics.rigid_body import RigidBody
from procedural_gen.region.vec import Vec


class GroupPool:
    def __init__(self):
        self.id_gen = IdGenerator()
        self.static = self.id_gen.new_id()
        self.dynamic = self.id_gen.new_id()

        # self.static_ground = self.id_gen.new_id()
        # self.static_building = self.id_gen.new_id()
        self.static_ghost = self.id_gen.new_id()
        # self.dynamic_ghost = self.id_gen.new_id()

    def set_group(self, node: NodePath, value: int):
        node.set_collide_mask(BitMask32.bit(value))

    def update(self, item: RigidBody):
        group = self.static
        if item.density > 0:
            group = self.dynamic
        if item.only_static_collision:
            group = self.static_ghost
        self.set_group(item.node, group)


class PhysSystem(System):
    _signature = RigidBody
    _filter_strategy = EntityFilter.match_none

    freeze_sim: bool = True
    sim_speed: int = 0

    phys_max_steps: int = 10
    phys_update_rate_hertz: float = 200
    phys_gravity: float = 9.80665

    @cached_property
    def groups(self):
        return GroupPool()

    @cached_property
    def world(self):
        world = BulletWorld()

        world.set_gravity(Vec3(0, 0, -self.phys_gravity))
        world.setGroupCollisionFlag(self.groups.static, self.groups.static, False)
        world.setGroupCollisionFlag(self.groups.static, self.groups.dynamic, True)
        world.setGroupCollisionFlag(self.groups.static, self.groups.static_ghost, True)
        world.setGroupCollisionFlag(self.groups.static_ghost, self.groups.static_ghost, False)
        world.setGroupCollisionFlag(self.groups.static_ghost, self.groups.dynamic, False)

        return world

    @override
    def update_before(self, db: Database):
        dt = globalClock.getDt()
        self.world.do_physics(
            dt * 2 ** self.sim_speed,
            self.phys_max_steps,
            1 / self.phys_update_rate_hertz
        )

    @override
    def update(self, db: Database):
        if self.freeze_sim:
            return
        status = super().update(db)
        return status

    @time_func
    @override
    def register(self, item: RigidBody):
        self.groups.update(item)
        self.world.attach(item.body)

    @override
    def unregister(self, phys: RigidBody):
        try:
            self.world.remove(phys.body)
            phys.node.detach_node()
        except Exception as e:
            logger.warning(f'{e}')

    @cached_property
    def debug(self):
        parent = base.render
        debug = BulletDebugNode(f'{parent}')
        debug.showWireframe(True)
        debug.showConstraints(True)
        debug.showBoundingBoxes(False)
        debug.showNormals(False)
        self.world.clear_debug_node()
        self.world.setDebugNode(debug)
        node: NodePath = parent.attach_new_node(debug)
        return node

    def switch_play(self, status: bool = None):
        if not status:
            self.freeze_sim = not self.freeze_sim
        else:
            self.freeze_sim = status

    def change_speed(self, delta: float):
        def func():
            self.sim_speed += delta
            logger.info(f'speed={self.sim_speed}')

        return func

    def set_speed(self, value: float):
        value -= .5
        value *= 10
        value = int(value)
        self.sim_speed = value
        logger.info(f'speed={self.sim_speed}')

    def toggle_debug(self):
        if self.debug.isHidden():
            self.debug.show()
        else:
            self.debug.hide()

    def get_collision(self, origin: Vec, target: Vec):
        from sandbox_core.entity.entity import EntityNode

        result = self.world.rayTestClosest(Vec3(*origin.vec), Vec3(*target.vec))
        body_node = result.getNode()
        pos = result.getHitPos()
        normal = result.getHitNormal()
        entity: EntityNode = None
        node: NodePath = None
        if body_node:
            try:
                node = base.render.find(f'**/{body_node.getName()}')
                entity = node.get_python_tag('entity')
            except Exception as e:
                logger.error(f'{e}')
        else:
            pos = target
        return RayCollision(
            entity=entity,
            node=node,
            pos=Vec.cast(pos),
            normal=Vec.cast(normal)
        )
