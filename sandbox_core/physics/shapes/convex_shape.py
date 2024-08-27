from panda3d.bullet import BulletConvexHullShape, BulletBodyNode
from panda3d.core import Point3

from sandbox_core.physics.shapes.abstract_shape import AbstractShape
from procedural_gen.region.vec import Vec


class ConvexShape(AbstractShape):
    name: str = 'hull'
    points: list[Vec]

    def create(self, body: BulletBodyNode):
        shape = BulletConvexHullShape()
        for _ in self.points:
            shape.add_point(Point3(*_.vec))
        body.add_shape(shape)

    def volume(self):
        raise NotImplementedError
