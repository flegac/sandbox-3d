from functools import cached_property
from pathlib import Path

from panda3d.core import PNMImage, Filename, GeoMipTerrain

from easy_kit.timing import time_func
from sandbox.my_base import base
from sandbox_core.display.model_provider import ModelProvider


class TerrainModel(ModelProvider):
    height_path: Path

    @cached_property
    def heightmap_image(self):
        return PNMImage(Filename(self.height_path))

    @cached_property
    def terrain(self):
        terrain = GeoMipTerrain("Terrain")
        terrain.setBlockSize(8)
        terrain.setNear(8)
        terrain.setFar(64)
        terrain.setMinLevel(0)
        terrain.setFocalPoint(base.cam)
        # terrain.setBruteforce(True)
        terrain.setHeightfield(self.height_path)

        return terrain

    @time_func
    def model_node(self):
        return self.terrain.getRoot()
