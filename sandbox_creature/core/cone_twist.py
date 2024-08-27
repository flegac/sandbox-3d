from panda3d.bullet import BulletConeTwistConstraint
from panda3d.core import TransformState, Point3, Vec3

from sandbox_creature.core.joint import Joint


class ConeTwist(Joint):
    swing1: float
    swing2: float
    twist: float

    def builder(self):
        body1 = self.referential.body
        body2 = self.pivot.body

        # state1 = self.other.transform_state(self.pivot.vec)

        offset = self.pivot.vec - self.referential.center
        axis = self.pivot.axis
        state1 = TransformState.make_pos_hpr(Point3(*offset.vec), Vec3(*axis.vec))

        state2 = self.pivot.transform_state(self.pivot.vec)
        cs = BulletConeTwistConstraint(body1, body2, state1, state2)
        cs.setLimit(
            self.swing1, self.swing2, self.twist,
            self.softness, self.bias, self.relaxation
        )
        return cs
