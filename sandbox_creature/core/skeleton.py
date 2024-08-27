from functools import cached_property

from pydantic import Field

from easy_kit.timing import time_func
from python_ecs.component import Component
from sandbox_core.controls.controller.stance_config import StanceConfig
from sandbox_core.controls.params.vec_param import VecParam
from sandbox_core._utils.coord_manager import CoordManager
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_creature.core.anatomic import Anatomic
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.joint import Joint
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Skeleton(Component):
    bone_map: dict[str, Bone] = Field(default_factory=dict)
    joint_map: dict[str, Joint] = Field(default_factory=dict)
    config: StanceConfig = Field(default_factory=StanceConfig)

    def new_cone_twist(
            self,
            tags: str | None,
            pivot: Anchor,
            referential: Bone,
            swing1: float,
            swing2: float,
            twist: float,
            symmetry: Symmetry = Symmetry.default
    ):
        from sandbox_creature.core.cone_twist import ConeTwist
        joint = ConeTwist(
            tags=tags,
            symmetry=symmetry,
            pivot=pivot,
            referential=referential,
            swing1=swing1,
            swing2=swing2,
            twist=twist
        )
        joint.referential = referential
        self.add_joint(joint)
        return joint

    def add_joint(self, joint: Joint):
        self.joint_map[joint.tags] = joint
        self.config.with_vec(
            joint.tags, VecParam.create(
                value=Vec(),
                low=Vec.at(-joint.swing1, -joint.swing2, -joint.twist),
                high=Vec.at(joint.swing1, joint.swing2, joint.twist),
                speed=Vec.cast(5)
            )
        )

        return joint

    @time_func
    def search_bone(self, query: str) -> list[Bone]:
        return Anatomic.parse(f'{query} Bone').search(self, joints=False)

    def single_bone(self, query: str) -> Bone:
        return Anatomic.parse(f'{query} Bone').single(self, joints=False)

    @time_func
    def search_joint(self, query: str) -> list[Joint]:
        return Anatomic.parse(f'{query} Joint').search(self, bones=False)

    def single_joint(self, query: str) -> Joint:
        return Anatomic.parse(query).single(self, bones=False)

    @cached_property
    def pelvis(self):
        return self.single_bone('Pelvis')

    @cached_property
    def torso(self):
        return self.single_bone('Torso')

    def hips(self, side: Symmetry):
        return self.single_joint(f'hips {side.name}')

    def knee(self, side: Symmetry):
        return self.single_joint(f'knee {side.name}')

    def ankle(self, side: Symmetry):
        return self.single_joint(f'ankle {side.name}')

    @cached_property
    def feet(self):
        return self.search_bone('Foot')

    def hips_local(self):
        return CoordManager(self.pelvis.entity.phys.node).get_local()

    @time_func
    def local_derivation(self, p1: Vec, p2: Vec):
        derive = p2 - p1
        forward, up, right = self.hips_local()

        dx = derive.dot(right) / right.length()
        dy = derive.dot(forward) / forward.length()
        dz = derive.dot(up) / up.length()

        return Vec.at(dx, dy, dz)

    @property
    def mass_center(self):
        return RigidBody.mass_center([_.phys for _ in self.bone_map.values()])

    def add_bone(self, bone: Bone):
        self.bone_map[bone.tags] = bone
        bone.create()
        return bone

    @property
    def type_id(self):
        return Skeleton
