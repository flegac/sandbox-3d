from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class Sword(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, length: float = 0.7, width=.05, depth: float = .005):
        grip_offset = .1 * length
        bone = Sword(
            tags='Sword upper Weapon',
            center=origin.vec,
            anchors={
                'start': Anchor(offset=-grip_offset * Vec.z_axis()),
                'end': Anchor(offset=(length - grip_offset) * Vec.z_axis()),
            }
        )
        bone.phys.shape = BoxShape.from_size(Vec.at(width, depth, length))
        bone.phys.density = 8_000
        bone.entity.health.hit_damage = 10
        joint = skeleton.new_cone_twist(
            pivot=bone.new_anchor('grip', axis=origin.axis),
            referential=origin._bone,
            tags='grip upper Weapon',
            swing1=0,
            swing2=0,
            twist=0,
        )
        joint.current = None
        skeleton.add_bone(bone)

        return bone
