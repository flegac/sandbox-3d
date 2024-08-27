import random

from sandbox_core.transform import ETransform
from sandbox_lib.rooms.floor import Floor
from sandbox_lib.rooms.room import Room
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec


class FloorBuilder:
    def __init__(self, floor: Floor):
        self.floor = floor

    def build_room(self, pos: Vec):
        self.floor.new_room(
            transform=ETransform(
                position=pos,
                rotation=Vec.at(random.random() * 360, 0, 0)
            ),
            room=Room.square(region=Region.from_size(40, 40, 3).center_at(Vec()), n=5),
        )
