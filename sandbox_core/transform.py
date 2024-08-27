from functools import cached_property

from panda3d.core import NodePath, Vec3, Point3, TransformState
from pydantic import Field

from python_ecs.component import Component
from sandbox.my_base import base
from sandbox_core.unique_id import UniqueId
from procedural_gen.region.vec import Vec


class ETransform(Component):
    position: Vec = Field(default_factory=lambda: Vec.cast(0))
    rotation: Vec = Field(default_factory=lambda: Vec.cast(0))
    scale: Vec = Field(default_factory=lambda: Vec.cast(1))

    @cached_property
    def node(self):
        node = base.render.attach_new_node(f'tranform-{UniqueId.next()}')
        self.apply(node)
        return node

    @property
    def radius(self) -> float:
        return .5 * max(self.scale.vec)

    def apply(self, node: NodePath):
        node.set_pos_hpr_scale(
            Vec3(*self.position.vec),
            Vec3(*self.rotation.vec),
            Vec3(*self.scale.vec)
        )

    def transform_state(self):
        return TransformState.make_pos_hpr_scale(
            Point3(*self.position.vec),
            Vec3(*self.rotation.vec),
            Vec3(*self.scale.vec)
        )
