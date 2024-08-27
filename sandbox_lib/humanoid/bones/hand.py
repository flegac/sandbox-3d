from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_creature.core.anchor import Anchor
from sandbox_creature.core.bone import Bone
from sandbox_creature.core.skeleton import Skeleton
from sandbox_creature.core.symmetry import Symmetry
from procedural_gen.region.vec import Vec


class Hand(Bone):
    @staticmethod
    def new(skeleton: Skeleton, origin: Anchor, symmetry: Symmetry, length: float = .17, radius: float = .01):
        closed = True
        if closed:
            width = length * .25
            length *= .65
            radius = width
            shape = CapsuleShape.from_size(Vec.at(length, 2 * radius, 2 * radius))
        else:
            width = length * .25
            shape = BoxShape.from_size(Vec.at(length, 2 * radius, 2 * width))
        bone = Hand(
            tags=f'Hand upper {symmetry.name} Bone',
            symmetry=symmetry,
            center=origin.vec,
            anchors={
                'center': Anchor(offset=.5 * length * symmetry.direction, axis=origin.axis),
                'end': Anchor(offset=length * symmetry.direction, axis=origin.axis),
            },
        )
        bone.phys.shape = shape
        skeleton.new_cone_twist(
            pivot=bone.new_anchor('start', axis=origin.axis),
            referential=origin._bone,
            tags=f'wrist upper {symmetry.name} Joint',
            symmetry=symmetry,
            swing1=90,
            swing2=90,
            twist=180,
        )
        skeleton.add_bone(bone)

        return bone
