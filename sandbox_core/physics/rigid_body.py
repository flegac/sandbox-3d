from functools import cached_property
from typing import Iterable

from loguru import logger
from panda3d.bullet import BulletRigidBodyNode, BulletBodyNode, BulletGhostNode, BulletShape
from panda3d.core import NodePath, Vec3
from pydantic import Field

from easy_kit.timing import time_func
from python_ecs.component import Component
from sandbox.my_base import base
from sandbox_core.transform import ETransform
from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_core.physics.shapes.compund_shape import AnyShape
from sandbox_core.unique_id import UniqueId
from procedural_gen.region.vec import Vec


class RigidBody(Component):
    shape: AnyShape = Field(default_factory=BoxShape)
    transform: ETransform = Field(default_factory=ETransform)
    density: float = 0
    friction: float = 1
    restitution: float = 0
    angular_damping: float = .0
    linear_damping: float = .0
    is_ghost: bool = False
    only_static_collision: bool = False

    @staticmethod
    def mass_center(items: Iterable['RigidBody']):
        pos = Vec()
        mass = 0
        for phys in items:
            pos += phys.pos * phys.mass
            mass += phys.mass
        return pos / mass

    @cached_property
    def body(self) -> BulletBodyNode:
        if self.is_ghost:
            body = BulletGhostNode(f'body-{UniqueId.next()}')
        else:
            body = BulletRigidBodyNode(f'body-{UniqueId.next()}')
            body.set_angular_damping(self.angular_damping)
            body.set_linear_damping(self.linear_damping)
            body.set_mass(self.density * self.shape.volume())
        body.friction = self.friction
        body.restitution = self.restitution
        return body

    @cached_property
    @time_func
    def node(self) -> NodePath:
        warnings = self.get_warnings()
        if warnings:
            logger.warning(f'rigidBody: {warnings}')

        node: NodePath = base.render.attach_new_node(self.body)
        node.set_python_tag('entity', self)
        self.shape.create(self.body)
        self.transform.apply(node)

        return node

    @property
    def pos(self):
        return Vec.cast(self.body.transform.get_pos())

    @pos.setter
    def pos(self, value: Vec):
        self.body.set_transform(
            self.body.transform.set_pos(Vec3(*value.vec))
        )

    @property
    def hpr(self):
        return Vec.cast(self.body.transform.get_hpr())

    @hpr.setter
    def hpr(self, value: Vec):
        self.body.set_transform(
            self.body.transform.set_hpr(Vec3(*value.vec))
        )

    @property
    def linear_velocity(self):
        return Vec.cast(self.body.linear_velocity)

    @linear_velocity.setter
    def linear_velocity(self, value: Vec):
        self.body.set_linear_velocity(Vec3(*value.vec))

    @property
    def angular_velocity(self):
        return Vec.cast(self.body.angular_velocity)

    @angular_velocity.setter
    def angular_velocity(self, value: Vec):
        self.body.set_angular_velocity(Vec3(*value.vec))

    def apply_central_force(self, value: Vec):
        self.body.apply_central_force(Vec3(*value.vec))

    def apply_torque(self, value: Vec):
        self.body.apply_torque(Vec3(*value.vec))

    @property
    def mass(self) -> float:
        return self.body.mass

    @mass.setter
    def mass(self, value: Vec):
        self.body.set_mass(value)

    @property
    def kinetic_energy(self):
        speed = self.linear_velocity.length()
        return .5 * self.mass * speed * speed

    def get_warnings(self):
        warnings = {}
        if self.linear_damping > 0 or self.angular_damping > 0:
            warnings['damping'] = f'{self.angular_damping} {self.linear_damping}'
        if self.transform.scale.dist(Vec.cast(1)) > .01:
            warnings['scale'] = f'{self.transform.scale}'
        return warnings

    @property
    def bullet_shape(self) -> BulletShape:
        return self.node.node().shapes[0]
