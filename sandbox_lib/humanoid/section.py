from easy_config.my_model import MyModel
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec


class Section(MyModel):
    region: Region
    offset: float

    @staticmethod
    def from_size(width: float, depth: float, offset: float):
        return Section(
            region=Region.from_size(width=width, height=depth),
            offset=offset
        )

    @property
    def size(self):
        return Vec.at(self.region.size.x, self.region.size.y, 0)
