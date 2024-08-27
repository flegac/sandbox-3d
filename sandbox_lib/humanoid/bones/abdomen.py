from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class Abdomen(Bone):
    @staticmethod
    def new(
            skeleton: Skeleton,
            origin: Anchor,
            size: Vec,
    ):
        left_axis = Vec.at(0, 0, 0)
        right_axis = Vec.at(0, 0, 0)

        axis = origin.axis
        bone = Abdomen(
            tags=f'Abdomen upper Bone',
            center=origin.vec,
            anchors={
                'start': Anchor(axis=axis),
                'end': Anchor(offset=size.z * Vec.z_axis(), axis=axis),
                'front': Anchor(offset=.5 * size.y * Vec.y_axis()),
                'back': Anchor(offset=-.5 * size.y * Vec.y_axis()),
                'left': Anchor(offset=Vec.at(-.5 * size.x, 0, .5 * size.z), axis=left_axis),
                'right': Anchor(offset=Vec.at(.5 * size.x, 0, .5 * size.z), axis=right_axis),
            },
        )
        # bone.phys.shape = CapsuleShape.from_size(size)
        bone.phys.shape = BoxShape.from_size(size)

        skeleton.new_cone_twist(
            pivot=bone.at('start'),
            referential=origin._bone,
            tags=f'abdomen upper Joint',
            swing1=25,
            swing2=25,
            twist=25,
        )
        skeleton.add_bone(bone)

        return bone
