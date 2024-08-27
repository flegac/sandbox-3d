from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class Neck(Bone):
    @staticmethod
    def new(
            skeleton: Skeleton,
            origin: Anchor,
            length: float = .15,
            radius: float = .025,
            mobility: float = 25,
    ):
        bone = Neck(
            tags=f'Neck upper Bone',
            center=origin.vec,
            anchors={
                'start': Anchor(axis=origin.axis),
                'end': Anchor(offset=length * Vec.z_axis(), axis=origin.axis),
            },
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.at(2 * radius, 2 * radius, length))

        skeleton.new_cone_twist(
            pivot=bone.at('start'),
            referential=origin._bone,
            tags=f'neck upper Joint',
            swing1=mobility,
            swing2=mobility,
            twist=mobility,
        )
        skeleton.add_bone(bone)

        return bone
