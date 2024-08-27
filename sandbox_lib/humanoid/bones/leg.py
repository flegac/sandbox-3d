from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Leg(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .48, radius=.05):
        delta: Vec = Vec.z_axis() * radius

        bone = Leg(
            tags=f'Leg lower {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec + delta,
            anchors={
                'start': Anchor(axis=origin.axis),
                'end': Anchor(offset=-length * Vec.z_axis(), axis=origin.axis),
                # 'start_pivot': Anchor(offset=-delta, axis=origin.axis),
                'end_pivot': Anchor(offset=-length * Vec.z_axis() + delta, axis=origin.axis),
            },
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.at(2 * radius, 2 * radius, length))
        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start_pivot', offset=-delta, axis=origin.axis),
            referential=origin._bone,
            tags=f'knee lower {symmetry.name} Joint',
            symmetry=symmetry,
            swing1=180,
            swing2=10,
            twist=0,
            # low=0,
            # high=150,
        )
        # joint.current.z= -20
        skeleton.add_bone(bone)

        return bone
