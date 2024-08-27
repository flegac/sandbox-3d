from sandbox_core.transform import ETransform
from sandbox_core._utils.coord_manager import compute_rotation
from sandbox_lib.rooms.building import Building
from sandbox_lib.rooms.pilar import Pilar
from procedural_gen.region.vec import Vec


class Wall(Building):
    p1: Vec
    p2: Vec

    @staticmethod
    def link(p1: Pilar | Vec, p2: Pilar | Vec):
        return Wall(
            name='wall',
            p1=p1 if isinstance(p1, Vec) else p1.vec,
            p2=p2 if isinstance(p2, Vec) else p2.vec
        )

    @property
    def height(self):
        return self.p1.z

    @property
    def entity(self):
        assert self.p1.z == self.p2.z

        direction = self.p2 - self.p1
        pos = self.p1 * Vec.at(1, 1, .5) + direction * .5

        return self.make_entity(
            ETransform(
                position=pos,
                rotation=compute_rotation(direction),
                scale=Vec.at(direction.length(), self.thickness, self.p1.z),
            ),
            # density=1
        )
