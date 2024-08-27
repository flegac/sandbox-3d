from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from procedural_gen.region.vec import Vec


class Pelvis(Bone):
    @staticmethod
    def new(
            skeleton: Skeleton,
            origin: Vec,
            size: Vec,
    ):
        left_axis = Vec.at(0, 0, 0)
        right_axis = Vec.at(0, 0, 0)

        axis = Vec.at(0, 0, -90)
        bone = Pelvis(
            tags=f'Pelvis lower Bone',
            center=origin,
            anchors={
                'start': Anchor(axis=axis),
                'end': Anchor(offset=size.z * Vec.z_axis(), axis=axis),
                'front': Anchor(offset=.5 * size.y * Vec.y_axis()),
                'back': Anchor(offset=-.5 * size.y * Vec.y_axis()),
                'left': Anchor(offset=Vec.at(-.5 * size.x, 0, .5 * size.z), axis=left_axis),
                'right': Anchor(offset=Vec.at(.5 * size.x, 0, .5 * size.z), axis=right_axis),
                'left_up': Anchor(offset=Vec.at(-.5 * size.x, 0, .85 * size.z), axis=left_axis),
                'right_up': Anchor(offset=Vec.at(.5 * size.x, 0, .85 * size.z), axis=right_axis),
                'left_low': Anchor(offset=Vec.at(-.5 * size.x, 0, .15 * size.z), axis=left_axis),
                'right_low': Anchor(offset=Vec.at(.5 * size.x, 0, .15 * size.z), axis=right_axis),
            },
        )
        bone.phys.shape = BoxShape.from_size(size)
        skeleton.add_bone(bone)

        return bone
