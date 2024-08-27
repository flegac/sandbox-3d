from typing import override

from sandbox_creature.behavior.behavior import Behavior
from procedural_gen.region.vec import Vec


class FallingBehavior(Behavior):
    power: float = 1200

    @override
    def match(self):
        pelvis = self.skeleton.pelvis
        feet = self.skeleton.feet
        foot_center = self.extra.foot_center
        delta_pelvis = pelvis.pos - foot_center

        return delta_pelvis.z < .5

    @override
    def update(self):
        torso = self.skeleton.torso
        pelvis = self.skeleton.pelvis
        feet = self.skeleton.feet
        foot_center = self.extra.foot_center

        delta_pelvis = pelvis.pos - foot_center

        stand_up_force = delta_torso * self.power * Vec.at(1, 1, 0)

        for foot in feet:
            foot.phys.apply_central_force(stand_up_force)
        torso.phys.apply_central_force(-stand_up_force)
