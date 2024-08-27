from panda3d.core import NodePath

from sandbox_core.transform import ETransform
from sandbox_core.entity.entity import complex_node
from sandbox_lib.rooms.building import Building
from sandbox_lib.rooms.room import Room
from procedural_gen.region.region import Region


class Floor(Building):
    region: Region
    _node: NodePath | None = None

    @staticmethod
    def create(region: Region):
        return Floor(name='floor', region=region)

    @property
    def entity(self):
        self.health = None
        pos = self.region.center
        pos.z = -self.thickness
        scale = self.region.size
        scale.z = self.thickness
        return self.make_entity(
            ETransform(
                position=pos,
                scale=scale,
            )
        )

    def new_floor(self, transform: ETransform):
        complex_node(
            transform=transform,
            entities=[self.entity],
        )
        self._node = transform.node

    def new_room(self, room: Room, transform: ETransform):
        complex_node(
            transform=transform,
            entities=[
                _.entity
                for _ in [
                    *room.pilars,
                    *room.walls,
                ]
            ],
        )
        # room.reparent_to(self._node)
