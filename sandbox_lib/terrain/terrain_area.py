import uuid
from functools import cached_property
from pathlib import Path

import math
from panda3d.core import PNMImage, Filename
from pydantic import Field

from easy_kit.timing import time_func
from easy_raster.model.resolution import Resolution
from easy_raster.raster_io import RasterIO
from easy_raster.transform.buffer_util import BufferUtil
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec
from python_ecs.component import Component
from sandbox_core.display.display import Display
from sandbox_core.display.terrain_model import TerrainModel
from sandbox_core.entity.entity import EntityNode
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.physics.shapes.heightfield_shape import HeightfieldShape
from sandbox_core.transform import ETransform
from sandbox_lib.terrain.model_queries import TREES, GRASS, ROCKS


class TerrainArea(Component):
    path: Path
    transform: ETransform = Field(default_factory=ETransform)

    @property
    def resolution(self):
        return Resolution.from_raw(1 + self.transform.scale.y, 1 + self.transform.scale.x)

    @property
    def eid(self):
        return self.entity.phys.eid

    @cached_property
    def entity(self):
        width, height = self.texture_size

        buffer = RasterIO.read(self.height_path, 0)
        buffer = BufferUtil.resize(buffer, *self.resolution.raw(), seamless=True)
        buffer = buffer.astype('uint8')
        path = Path.home() / f'.tmp/{uuid.uuid4()}.png'
        path.parent.mkdir(parents=True, exist_ok=True)

        RasterIO.write(path, buffer)

        model = TerrainModel(
            height_path=path,
            color_path=self.path / 'color.png',
            color_scale=25,
            normal_path=self.path / 'normal.png',
        )
        ETransform(
            position=self.display_offset,
            scale=Vec.at(1, 1, self.transform.scale.z)
        ).apply(model.model_node())
        return EntityNode(
            phys=RigidBody(
                transform=ETransform(
                    position=self.transform.position,
                    rotation=self.transform.rotation,
                ),
                shape=HeightfieldShape(
                    elevation_path=path,
                    height_max=self.transform.scale.z,
                ),
                density=0
            ),
            display=Display(model=model)
        )

    @cached_property
    @time_func
    def vegetation(self) -> list[EntityNode]:

        TREES.reset()

        region = Region.from_size(*self.transform.scale.vec).center_at(self.transform.position)
        # return []
        return [
            *TREES.create_all(n=10, radius=3, region=region),
            *GRASS.create_all(n=5, radius=2.5, region=region),
            *ROCKS.create_all(n=5, radius=3, region=region)
        ]

    @property
    def texture_size(self):
        heightmap = self.heightmap_image
        return heightmap.getXSize(), heightmap.getYSize()

    @property
    def display_offset(self):
        return -.5 * Vec.at(
            self.transform.scale.x,
            self.transform.scale.y,
            self.transform.scale.z
        )

    @property
    def height_path(self):
        return self.path / 'height.png'

    @cached_property
    def heightmap_image(self):
        return PNMImage(Filename(self.height_path))

    @time_func
    def get_elevation(self, pos: Vec):
        width, height = self.texture_size
        size_x = self.transform.scale.x
        size_y = self.transform.scale.y

        x = math.fmod(pos.x, size_x)
        if x < 0:
            x += size_x
        x *= width / size_x
        y = math.fmod(pos.y, size_y)
        if y < 0:
            y += size_y
        y *= height / size_y

        terrain = self.entity.display.model.terrain
        z = terrain.getElevation(x, y) * terrain.get_root().getSz() + self.display_offset.z
        return z
