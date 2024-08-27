from panda3d.bullet import BulletBoxShape, BulletBodyNode
from panda3d.core import Vec3

from sandbox_core.physics.shapes.abstract_shape import AbstractShape
from procedural_gen.region.vec import Vec


class BoxShape(AbstractShape):
    name: str = 'box'

    @staticmethod
    def from_points(points: list[Vec]):
        center, size = Vec.bbox(points)
        return BoxShape(size=.5 * size)

    @staticmethod
    def from_size(size: Vec):
        return BoxShape(size=.5 * size)

    def create(self, body: BulletBodyNode):
        size = self.size
        body.add_shape(BulletBoxShape(Vec3(*size.vec)))

    def volume(self):
        return 8 * self.size.x * self.size.y * self.size.z
