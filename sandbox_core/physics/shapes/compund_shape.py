from panda3d.bullet import BulletBodyNode
from pydantic import Field

from sandbox_core.physics.shapes.abstract_shape import AbstractShape
from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_core.physics.shapes.convex_shape import ConvexShape
from sandbox_core.physics.shapes.heightfield_shape import HeightfieldShape
from sandbox_core.physics.shapes.mesh_shape import MeshShape
from sandbox_core.physics.shapes.sphere_shape import SphereShape

type PrimitiveShape = SphereShape | BoxShape | CapsuleShape | MeshShape | ConvexShape | HeightfieldShape
type AnyShape = PrimitiveShape | CompoundShape


class CompoundShape(AbstractShape):
    name: str = 'compound'
    shapes: list[PrimitiveShape] = Field(default_factory=list)

    def create(self, body: BulletBodyNode):
        for _ in self.shapes:
            _.create(body)
        return body

    def volume(self) -> float:
        return sum([_.volume() for _ in self.shapes])
