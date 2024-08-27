from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Arm(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .27, radius: float = .035):
        pivot_delta = symmetry.direction * radius
        bone = Arm(
            tags=f'Arm upper {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec,
            anchors={
                'start': Anchor(axis=origin.axis),
                'end': Anchor(offset=symmetry.direction * length, axis=origin.axis + Vec.at(90, 0, 0)),
                'end_pivot': Anchor(
                    offset=symmetry.direction * length - pivot_delta,
                    axis=origin.axis + Vec.at(90, 0, 0)
                ),
            },
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.at(length, 2 * radius, 2 * radius))

        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start_pivot', offset=pivot_delta, axis=origin.axis),
            referential=origin._bone,
            tags=f'shoulder upper {symmetry.name} Joint',
            symmetry=symmetry,
            swing1=120,
            swing2=90,
            twist=90,
        )
        skeleton.add_bone(bone)

        return bone
