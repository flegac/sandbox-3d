from procedural_gen.region.vec import Vec
from python_ecs.ecs import sim
from sandbox.configgg import DATA_ROOT
from sandbox.my_base import base, GraphicConfig
from sandbox.sim_init import sim_init
from sandbox_core.camera.camera import CameraConfig
from sandbox_core.controls.axis_config import AxisConfig
from sandbox_core.controls.controller.phys_controller import PhysicController
from sandbox_core.controls.controller.skeleton_handler import SkeletonHandler
from sandbox_core.controls.follow import Follow
from sandbox_core.controls.params.float_param import FloatParam
from sandbox_core.controls.params.param_updater import ParamUpdater
from sandbox_core.display.display import Display
from sandbox_core.display.geometry_model import GeometryModel
from sandbox_core.entity.entity import EntityNode
from sandbox_core.entity.shooter.shooter_config import ShooterConfig
from sandbox_core.light.light import LightConfig
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.physics.shapes.capsule_shape import CapsuleShape
from sandbox_core.transform import ETransform
from sandbox_gui.features.mode_manager import ModeManager
from sandbox_lib.humanoid.behavior.complex_behavior import ComplexBehavior
from sandbox_lib.humanoid.behavior.standup_behavior import StandUpBehavior
from sandbox_lib.humanoid.humanoid import Humanoid
from sandbox_lib.terrain.terrain_system import TerrainSystem


def main():
    sim_init()

    camera = CameraConfig()
    skeleton = Humanoid().create(origin=3 * Vec.z_axis())
    starship = EntityNode(
        phys=RigidBody(
            transform=ETransform(
                position=Vec.at(0, 10, 3),
                rotation=Vec.at(0, 90, 180),
            ),
            density=1,
            is_ghost=True,
            shape=CapsuleShape(
                radius=1.,
                height=7,
            ),
        ),
        display=Display(
            model=GeometryModel(
                geometry_path=DATA_ROOT / 'fighter/fighter.fbx',
                color_path=DATA_ROOT / 'fighter/texture.jpg',
                # normal_path=DATA_ROOT / 'fighter/normal.jpg',
            ),
            transform=ETransform(
                scale=Vec.cast(.02)
            )
        )
    ).new_entity()

    # avatar = starship.phys
    avatar = skeleton.torso.phys

    sim.find(TerrainSystem).avatar = avatar

    # Viewport(skeleton.torso.phys.node)

    stand_up = StandUpBehavior(skeleton=skeleton)

    base.accept('i', stand_up.set_side)

    sim.create_all([
        # light
        LightConfig(
            color_temperature=4700,
            attenuation=(1.0, 0.0, 0.00)
        ).attach(
            anchor=camera.rotation_node,
            offset=Vec.at(0, -3, .25)
        ),

        # camera
        Follow.create(origin=camera.origin, target=avatar.node),
        [
            FloatParam(low=-90, high=0),
            ParamUpdater(updater=camera.rotation_node.setP),
            AxisConfig(name='vertical', events_incr=['arrow_down'], events_decr=['arrow_up'])
        ],
        [
            FloatParam(low=0, high=360, modulo=True),
            ParamUpdater(updater=camera.rotation_node.setH),
            AxisConfig(name='horizontal', events_incr=['arrow_right'], events_decr=['arrow_left'])
        ],
        [
            FloatParam(low=-100, high=-5),
            ParamUpdater(updater=camera.translation_node.setY),
            AxisConfig(name='distance', events_incr=['wheel_up', ], events_decr=['wheel_down', ])
        ],

        # creature
        PhysicController(
            power=25,
            targets=[
                _.phys
                for _ in [
                    # *skeleton.bone_map.values()
                    # *skeleton.search_bone('Thigh'),
                    *skeleton.search_bone('Leg'),
                    *skeleton.search_bone('WalkSupport'),
                    skeleton.pelvis, skeleton.torso
                ]
            ],
            rotate_target=[_.phys for _ in [skeleton.torso]],
            jump_target=[_.phys for _ in [
                skeleton.torso
                # * skeleton.bone_map.values()
            ]],
        ),
        ShooterConfig(origin=avatar, transform=ETransform(position=Vec.at(0, 0, 1))),

        SkeletonHandler(skeleton),
        skeleton,
        ComplexBehavior.from_states([
            stand_up,
        ]),

    ])

    others = [
        Humanoid().create(origin=Vec.at(-9 + 2 * x, 5 + 2 * y, 2))
        for x in range(2)
        for y in range(2)
    ]
    sim.create_all([
        *others,
        *[
            ComplexBehavior.from_states([
                StandUpBehavior(skeleton=_),
            ])
            for _ in others
        ]
    ])

    ModeManager().switch(True)

    GraphicConfig().setup(base.render)
    # GraphicConfig().setup(avatar.node)
    base.run()


if __name__ == '__main__':
    main()
