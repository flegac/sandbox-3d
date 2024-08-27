from sandbox_core.transform import ETransform
from sandbox_lib.rooms.building import Building
from procedural_gen.region.vec import Vec
from procedural_gen.region.region import Region


class Pilar(Building):
    vec: Vec

    @staticmethod
    def at(x: float = 0, y: float = 0, z: float = 0):
        return Pilar(name='pilar', vec=Vec.at(x=x, y=y, z=z))

    @property
    def height(self):
        return self.vec.z

    @property
    def region(self):
        pos = self.vec.clone()
        pos.z = self.height * .5
        return Region.from_size(2 * self.thickness, 2 * self.thickness, self.height).center_at(pos)

    @property
    def entity(self):
        return self.make_entity(ETransform(
            position=self.region.center,
            scale=self.region.size,
        ))
