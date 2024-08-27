from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class Head(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, radius: float = .07, mobility: float = 20):
        bone = Head(
            tags='Head Bone',
            center=origin.vec + radius * Vec.z_axis() + .15 * radius * Vec.y_axis(),
        )
        bone.phys.shape = CapsuleShape.from_size(Vec.cast(2 * radius))

        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start', offset=-radius * Vec.z_axis(), axis=origin.axis),
            referential=origin._bone,
            tags='neck Joint',
            swing1=mobility,
            swing2=mobility,
            twist=mobility
        )
        skeleton.add_bone(bone)

        return bone
