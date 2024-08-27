from abc import abstractmethod
from functools import cached_property

from loguru import logger
from panda3d.bullet import BulletConstraint, BulletHingeConstraint, BulletConeTwistConstraint
from panda3d.core import QuatF, Vec3
from pydantic import Field

from easy_kit.timing import time_func
from python_ecs.ecs import sim
from python_ecs.system import System
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_creature.core.anatomic import Anatomic
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.symmetry import Symmetry
from sandbox_creature.gesture.joint_sequence import JointSequence
from procedural_gen.region.vec import Vec


class Joint(Anatomic):
    pivot: Anchor
    referential: Bone

    current: Vec | None = Field(default_factory=Vec)
    sequence: JointSequence = Field(default_factory=JointSequence)

    impulse: float = 1
    softness: float = 1
    bias: float = .35
    relaxation: float = 1
    debug_scale: float = .1
    linked_collision: bool = True
    damping: float = .9

    @abstractmethod
    def builder(self) -> BulletConstraint:
        ...

    @cached_property
    def cs(self):
        return self.builder()

    def create(self):
        self.cs.set_debug_draw_size(self.debug_scale)
        if not self.linked_collision:
            logger.warning(f'joint with link collision !')
        sim.find(PhysSystem).world.attach_constraint(self.cs, linked_collision=self.linked_collision)
        self.cs.set_enabled(True)

    @time_func
    def update(self):
        if not self.sequence.is_done:
            self.current = self.sequence.play(self.current)

        hpr = hpr_fix_symmetry(self.symmetry, self.current)

        cs = self.cs
        if hpr is None:
            cs.enable_motor(False)
            return
        quat = QuatF()
        quat.set_hpr(Vec3(*hpr.vec))
        cs.enable_motor(True)
        match cs:
            case BulletHingeConstraint():
                # cs.set_motor_target(quat, .1)
                raise NotImplementedError
            case BulletConeTwistConstraint():
                # cs.set_motor_target_in_constraint_space(quat)
                cs.set_motor_target(quat)

    @property
    def type_id(self):
        return Joint


def hpr_fix_symmetry(symmetry: Symmetry, vec: Vec):
    match symmetry:
        case Symmetry.default:
            return vec
        case Symmetry.left_up:
            return vec.invert_x
        case Symmetry.right_up:
            return vec.invert_z
        case Symmetry.left_low:
            return vec.invert_z
        case Symmetry.right_low:
            return vec
    raise NotImplementedError(f'{symmetry}')


class JointSystem(System):
    _signature = Joint
