from functools import cached_property

from easy_kit.timing import time_func
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.joint import Joint
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class SkeletonPhysics:
    def __init__(self, skeleton: Skeleton):
        self.skeleton = skeleton

    def search_bone(self, query: str) -> list[Bone]:
        return self.skeleton.search_bone(query)

    def single_bone(self, query: str) -> Bone:
        return self.skeleton.single_bone(query)

    def search_joint(self, query: str) -> list[Joint]:
        return self.skeleton.search_joint(query)

    def single_joint(self, query: str):
        return self.skeleton.single_joint(query)

    @property
    def mass_center(self):
        return self.skeleton.mass_center

    @time_func
    def get_mass_center_delta(self):
        return self.skeleton.local_derivation(
            self.foot_center,
            self.mass_center
        )

    @time_func
    def normalized_balance(self, center: Vec):
        foot_delta = self.foot_delta() * .5
        center_delta = self.skeleton.local_derivation(self.foot_center, center)
        if foot_delta.x != 0:
            center_delta.x /= foot_delta.x
        if foot_delta.y != 0:
            center_delta.y /= foot_delta.y
        if foot_delta.z != 0:
            center_delta.z /= foot_delta.z
        return center_delta

    @time_func
    def normalized_mass_center_delta(self):
        foot_delta = self.foot_delta() * .5
        center_delta = self.get_mass_center_delta()
        if foot_delta.x != 0:
            center_delta.x /= foot_delta.x
        if foot_delta.y != 0:
            center_delta.y /= foot_delta.y
        if foot_delta.z != 0:
            center_delta.z /= foot_delta.z
        return center_delta

    @time_func
    def get_upper_mass_center_delta(self):
        return self.skeleton.local_derivation(
            self.pelvis_center,
            self.upper_mass_center
        )

    @time_func
    def get_lower_mass_center_delta(self):
        return self.skeleton.local_derivation(
            self.foot_center,
            self.lower_mass_center
        )

    @property
    def pelvis_center(self):
        return self.pelvis.pos

    @property
    def foot_center(self):
        return (self.left_foot.pos + self.right_foot.pos) * .5

    @property
    def upper_mass_center(self):
        return RigidBody.mass_center([_.phys for _ in self._upper_bones])

    @property
    def lower_mass_center(self):
        return RigidBody.mass_center([_.phys for _ in self._lower_bones])

    @time_func
    def foot_delta(self):
        left = self.left_foot
        right = self.right_foot
        return self.skeleton.local_derivation(left.pos, right.pos) + self.foot_length * Vec.y_axis()

    @cached_property
    def foot_length(self):
        foot = self.left_foot
        return foot.at('front').offset.dist(foot.at('front').offset)

    @cached_property
    def left_foot(self):
        return self.single_bone('Foot left_low')

    @cached_property
    def right_foot(self):
        return self.single_bone('Foot right_low')

    @cached_property
    def _upper_bones(self):
        return self.search_bone('upper Bone')

    @cached_property
    def _lower_bones(self):
        return self.search_bone('lower Bone')
