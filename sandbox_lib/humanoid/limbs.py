from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from sandbox_lib.humanoid.bones.arm import Arm
from sandbox_lib.humanoid.bones.foot import Foot
from sandbox_lib.humanoid.bones.forearm import ForeArm
from sandbox_lib.humanoid.bones.hand import Hand
from sandbox_lib.humanoid.bones.leg import Leg
from sandbox_lib.humanoid.bones.sword import Sword
from sandbox_lib.humanoid.bones.thigh import Thigh
from sandbox_lib.humanoid.bones.walk_support import WalkSupport
from procedural_gen.region.vec import Vec


class Limbs:
    @staticmethod
    def lower(skeleton: Skeleton, origin: Bone, symmetry: Symmetry = None):
        if symmetry is None:
            Limbs.lower(skeleton, origin, Symmetry.left_low)
            Limbs.lower(skeleton, origin, Symmetry.right_low)
            return
        thigh = Thigh.new(skeleton, origin.at(symmetry.name), symmetry)
        leg = Leg.new(skeleton, thigh.at('end_pivot'), symmetry)
        foot = Foot.new(skeleton, leg.at('end'), symmetry)
        walk_support = WalkSupport.new(skeleton, leg.at('end'), symmetry, size=Vec.at(.25, .35, .05))

    @staticmethod
    def upper(skeleton: Skeleton, origin: Bone, symmetry: Symmetry = None):
        if symmetry is None:
            Limbs.upper(skeleton, origin, Symmetry.left_up)
            Limbs.upper(skeleton, origin, Symmetry.right_up)
            return
        arm = Arm.new(skeleton, origin.at(symmetry.name), symmetry)
        forearm = ForeArm.new(skeleton, arm.at('end_pivot'), symmetry)
        hand = Hand.new(skeleton, forearm.at('end'), symmetry)

        if symmetry is Symmetry.right_up:
            sword = Sword.new(skeleton, hand.at('center'))
