from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class WalkSupport(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, size: Vec):
        bone = WalkSupport(
            tags=f'WalkSupport {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec,
            anchors={
                'top': Anchor(offset=size.z * .5 * Vec.z_axis()),
                'bottom': Anchor(offset=-size.z * .5 * Vec.z_axis()),
            }
        )
        bone.is_hidden = True
        bone.phys.only_static_collision = True
        bone.phys.density = 10
        bone.phys.shape = BoxShape(size=size * .5)

        skeleton.new_cone_twist(
            pivot=bone.at('top'),
            referential=origin._bone,
            tags=f'WalkSupport lower {symmetry.name} Joint',
            swing1=360,
            swing2=360,
            twist=360,
        )

        skeleton.add_bone(bone)

        return bone
