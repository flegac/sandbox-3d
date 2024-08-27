from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Thigh(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .45, radius=.06):
        delta: Vec = radius * Vec.z_axis()
        bone = Thigh(
            tags=f'Thigh lower {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec - symmetry.direction * radius * 1.25,
            anchors={
                'start': Anchor(axis=origin.axis),
                'end': Anchor(offset=-length * Vec.z_axis(), axis=Vec.at(0, 0, 90)),
                'end_pivot': Anchor(offset=-length * Vec.z_axis() + delta, axis=Vec.at(0, 0, 90)),
            },
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.at(2 * radius, 2 * radius, length))
        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start_pivot', offset=- delta, axis=origin.axis),
            referential=origin._bone,
            tags=f'hips lower {symmetry.name} Joint',
            symmetry=symmetry,
            swing1=150,
            swing2=85,
            twist=90,
        )
        skeleton.add_bone(bone)

        return bone
