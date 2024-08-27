from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_core.physics.shapes.sphere_shape import SphereShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Foot(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .25, width: float = .09,
            mobility: float = 360):
        heel = .25 * length
        bone = Foot(
            tags=f'Foot lower {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec,
            anchors={
                'center': Anchor(axis=origin.axis),
                'front': Anchor(offset=(length - heel) * Vec.y_axis()),
                'back': Anchor(offset=- heel * Vec.y_axis()),
                'bottom': Anchor(offset=-.03 * Vec.z_axis())
            }
        )
        bone.phys.shape = BoxShape.from_size(size=Vec.at(width, length, .03))
        # bone.phys.shape = SphereShape(radius=length * .25)
        skeleton.new_cone_twist(
            pivot=bone.at('center'),
            referential=origin._bone,
            tags=f'ankle lower {symmetry.name} Joint',
            swing1=mobility,
            swing2=mobility,
            twist=5,
        )
        skeleton.add_bone(bone)

        return bone
