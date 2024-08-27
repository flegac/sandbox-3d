from sandbox.my_base import base
from sandbox_core.transform import ETransform
from sandbox_lib.humanoid.humanoid import Humanoid
from sandbox_lib.rooms.floor import Floor
from procedural_gen.region.region import Region
from procedural_gen.region.vec import Vec


def make_world():
    floor = make_floor()
    # make_terrain()
    creature = Humanoid().create(origin=.9 * Vec.z_axis())

    return floor, creature


def make_floor():
    floor_region = Region.from_size(1_000, 1_000, 100)

    floor = Floor.create(floor_region.center_at(Vec()))
    base.task_mgr.add(lambda t: floor.new_floor(
        # room=Room.square(region=Region.from_size(500, 200, 3).center_at(Pos()), n=8),
        transform=ETransform()
    ))
    return floor
