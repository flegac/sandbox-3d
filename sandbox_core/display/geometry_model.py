from functools import cache
from pathlib import Path

from easy_kit.timing import time_func
from sandbox.my_base import base
from sandbox_core.display.model_provider import ModelProvider
from procedural_gen.region.vec import Vec


class GeometryModel(ModelProvider):
    geometry_path: Path

    @time_func
    @cache
    def model_node(self):
        return base.loader.loadModel(self.geometry_path)

    def bound_size(self):
        start, end = self.bbox()
        return end - start

    def bbox(self):
        start, end = self.model_node().get_tight_bounds()
        return Vec.cast(start), Vec.cast(end)

    def get_scaling(self, size: float):
        bbox = self.bound_size()
        bbox.z = 0
        scaling = max(bbox.vec)
        return size / scaling

    def rescale(self, size: float):
        self.model_node().set_scale(self.get_scaling(size))
        return self
