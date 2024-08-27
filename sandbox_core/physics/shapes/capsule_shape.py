import math

from panda3d.bullet import BulletCapsuleShape, BulletBodyNode

from sandbox_core.physics.shapes.abstract_shape import AbstractShape
from sandbox_core.physics.shapes.axis import Axis
from procedural_gen.region.vec import Vec


class CapsuleShape(AbstractShape):
    name: str = 'capsule'
    radius: float = 1
    height: float = 1
    axis: Axis = Axis.z

    @staticmethod
    def from_points(points: list[Vec]):
        _, size = Vec.bbox(points)
        return CapsuleShape.from_size(size)

    @staticmethod
    def from_size(size: Vec):
        major = Axis.major(size)
        radius = Axis.minor(size).get_value(size) * .5
        height = major.get_value(size) - 2 * radius

        return CapsuleShape(height=height, radius=radius, axis=major, size=.5 * size)

    def create(self, body: BulletBodyNode):
        self.size = Vec.cast(self.radius)
        self.axis.set_value(self.size, .5 * self.height + self.radius)

        body.add_shape(BulletCapsuleShape(self.radius, self.height, self.axis.value))

    def volume(self):
        r = self.radius
        h = self.height
        return math.pi * r * r * (h + 4 * r / 3)
