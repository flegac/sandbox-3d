import sys

from loguru import logger

from easy_kit.timing import setup_timing
from python_ecs.ecs import sim
from sandbox.configgg import DATA_ROOT
from sandbox.my_base import base
from sandbox_core.controls.axis_system import AxisSystem
from sandbox_core.controls.follow_system import FollowSystem
from sandbox_core.controls.params.float_param_system import ParamSystem
from sandbox_core.controls.params.param_follow_system import ParamFollowSystem
from sandbox_core.display.display_system import DisplaySystem
from sandbox_core.entity.living_system import LivingSystem
from sandbox_core.entity.shooter.shooter_system import ShooterSystem
from sandbox_core.events.event_system import EventSystem
from sandbox_core.light.light_system import LightSystem
from sandbox_core.physics.collisions import CollisionSystem
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_creature.behavior.behavior_system import BehaviorSystem
from sandbox_creature.core.skeleton_system import SkeletonSystem
from sandbox_gui.base.panel_system import PanelSystem
from sandbox_lib.terrain.terrain_system import TerrainSystem

log_config = {
    'timing.log': {
        'level': 'INFO',
        'filter': lambda x: x['module'] == 'timing',
        'mode': 'w'
    }
}


def accepted(x):
    for _ in log_config.values():
        if _['filter'](x):
            return False
    return True


def sim_init():
    logger.remove()
    for k, v in log_config.items():
        logger.add(k, **v)
    logger.add(sys.stdout, level='INFO', filter=accepted)
    setup_timing()

    sim.systems.extend([
        # events / gui
        EventSystem(),
        AxisSystem(),
        ParamSystem(),
        ParamFollowSystem(),
        PanelSystem(),

        # mechanics
        TerrainSystem(data_root=DATA_ROOT),
        BehaviorSystem(),
        SkeletonSystem(),
        FollowSystem(),
        ShooterSystem(),
        LivingSystem(),

        # core functions
        PhysSystem(),
        CollisionSystem(),
        LightSystem(),
        DisplaySystem(),

    ])
    base.add_updater(sim.update)
