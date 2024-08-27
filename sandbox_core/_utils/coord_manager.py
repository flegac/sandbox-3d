from panda3d.core import NodePath, Vec3

from sandbox.my_base import base
from procedural_gen.region.vec import Vec


class CoordManager:
    def __init__(self, target: NodePath):
        self.target = target

    @staticmethod
    def from_right(right: Vec):
        right = right.normalized()
        up = Vec.z_axis()
        forward = up.cross(right).normalized()
        return forward, up, right

    def get_local(self):
        quat = self.target.get_quat(base.render)

        up = Vec.z_axis()
        right = Vec.cast(quat.get_right()).normalized()
        forward = up.cross(right).normalized()

        # forward = Vec.cast(quat.get_forward())
        # if forward.x == 0 and forward.y == 0:
        #     forward += Vec.cast(quat.get_up())
        # forward.z = 0
        # up = Vec.at(0, 0, 1)
        # right = Vec.cast(quat.get_right())

        return forward, up, right


def compute_rotation(direction: Vec):
    direction = Vec3(*direction.vec).normalized()
    rx = ry = rz = 0
    if direction.z != 0 or direction.x != 0:
        ry = Vec3(1, 0, 0).signed_angle_deg(direction, Vec3(0, 1, 0))
    if direction.y != 0 or direction.x != 0:
        rz = Vec3(1, 0, 0).signed_angle_deg(direction, Vec3(0, 0, 1))

    return Vec.at(rz, 0, ry)
