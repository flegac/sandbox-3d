from functools import cached_property
from pathlib import Path

import numpy as np
from panda3d.bullet import BulletBodyNode, BulletHeightfieldShape, ZUp
from panda3d.core import PNMImage, Filename
from pydantic import Field

from image_io.image_io import ImageIO
from sandbox_core.physics.shapes.abstract_shape import AbstractShape

ROOT = Path.home() / '.sandbox'


class HeightfieldShape(AbstractShape):
    name: str = 'heightmap'
    elevation_path: Path = Field(default=None)
    height_max: float = 1

    @staticmethod
    def from_resolution(x: int, y: int):
        shape = HeightfieldShape()
        path = shape.elevation_path

        ImageIO.write(path, np.zeros(shape=(y, x)))

        return shape

    def create(self, body: BulletBodyNode):
        shape = BulletHeightfieldShape(self.heightmap_image, self.height_max, ZUp)
        shape.set_use_diamond_subdivision(True)
        body.add_shape(shape)

    def volume(self):
        return 8 * self.size.x * self.size.y * self.size.z

    @cached_property
    def heightmap_image(self):
        return PNMImage(Filename(self.elevation_path))
