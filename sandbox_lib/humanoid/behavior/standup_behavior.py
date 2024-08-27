from typing import override

from sandbox_core._utils.ray.physic_ray import PhysicRay
from sandbox_creature.behavior.behavior import Behavior
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class StandUpBehavior(Behavior):
    power: float = 2500
    side: Symmetry = Symmetry.left_low
    active_ratio: float = 1.0

    def set_side(self, side: Symmetry = None):
        if side is None:
            side = self.side.reverse()
        self.side = side

    @override
    def match(self):
        delta = self.skeleton.torso.pos - self.extra.foot_center
        dx = delta.x
        dy = delta.y
        dz = delta.z
        return dz > 0 and dz * self.active_ratio > max(dx, dy)

    @override
    def update(self):
        foot = self.skeleton.single_bone(f'Foot {self.side.name}')
        delta = (self.skeleton.torso.pos - foot.pos) * self.power
        dz = delta.z

        force = Vec()

        if dz * self.active_ratio > delta.x:
            force += delta.x * Vec.x_axis()
        if dz * self.active_ratio > delta.y:
            force += delta.y * Vec.y_axis()
        if force.length() > 0:
            self.apply_force(force)

        # ray = PhysicRay()
        # for bone in self.skeleton.bone_map.values():
        #     bone.phys.pos = ray.fix_z(bone.pos, force=False)

    def apply_force(self, force: Vec):
        foot = self.skeleton.single_bone(f'Foot {self.side.name}')
        foot.phys.apply_central_force(force)
        self.skeleton.torso.phys.apply_central_force(-force)
