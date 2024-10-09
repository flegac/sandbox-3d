import math

from panda3d.bullet import BulletSphereShape, BulletBodyNode
from pydantic import model_validator

from sandbox_core.physics.shapes.abstract_shape import AbstractShape
from procedural_gen.region.vec import Vec


class SphereShape(AbstractShape):
    name: str = 'sphere'
    radius: float = 1

    def create(self, body: BulletBodyNode):
        self.size = Vec.cast(self.radius)
        body.add_shape(BulletSphereShape(self.radius))

    def volume(self):
        return 4 / 3 * math.pi * self.radius ** 3

    @model_validator(mode='after')
    def post_init(self):
        self.size = Vec.cast(self.radius)
        return self