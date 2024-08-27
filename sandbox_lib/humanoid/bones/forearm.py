from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class ForeArm(Bone):

    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .27, radius: float = .025):
        pivot_delta = symmetry.direction * radius
        bone = ForeArm(
            tags=f'ForeArm upper {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec - pivot_delta,
            anchors={
                'start': Anchor(axis=origin.axis),
                'end': Anchor(offset=length * symmetry.direction, axis=origin.axis + Vec.at(90, 0, 0)),
                'end_pivot': Anchor(offset=length * symmetry.direction - pivot_delta,
                                    axis=origin.axis + Vec.at(90, 0, 0)),
            },
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.at(length, 2 * radius, 2 * radius))
        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start_pivot', offset=pivot_delta, axis=origin.axis),
            referential=origin._bone,
            tags=f'elbow upper {symmetry.name} Joint',
            symmetry=symmetry,
            swing1=90,
            swing2=0,
            twist=0,
        )
        skeleton.add_bone(bone)

        return bone
