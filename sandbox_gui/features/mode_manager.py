from python_ecs.ecs import sim
from sandbox.my_base import base
from sandbox.world_maker import make_floor
from sandbox_core.entity.shooter.shooter_config import ShooterConfig
from sandbox_core.events.event_config import EventConfig
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_gui.base.config.color import Color
from sandbox_gui.base.config.fame_position import FramePosition
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.hover_handler import HoverHandler
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.features.control_mode import ControlMode
from sandbox_gui.features.editor.builder_panel import builder_panel
from sandbox_gui.features.panels.graphic_panel import graphic_panel
from sandbox_gui.features.panels.sound_panel import sound_panel


class ModeManager(ControlMode):
    def __init__(self):
        super().__init__()
        panel_size = FrameSize.from_size(350, 800)

        gui = L.tabs(
            ui=UiConfig(
                name='root',
                pos=FramePosition(5, 5),
                size=FrameSize(355, 850),
                frame_color=Color(.1, .1, .1, .5)
            ),
            children=[
                builder_panel(make_floor(), panel_size),
                sound_panel(panel_size),
                graphic_panel(panel_size),
            ]
        )
        HoverHandler.manage(gui)
        self.panels.register(gui)

        physics = sim.find(PhysSystem)
        self.events.register(
            EventConfig(mapping={
                'escape': self.panels.switch,
            }),
            EventConfig(actions={
                'mouse1': ShooterConfig.handler(list(sim.db.iter(ShooterConfig))),
            }),

            EventConfig(mapping={
                'f5': base.toggle_wireframe,
                'f6': base.toggle_texture,
                # 'f7': lambda: print(f'f7'),
                'f8': base.bufferViewer.toggleEnable,

                'f9': physics.toggle_debug,
                'f10': physics.change_speed(-1),
                'f11': physics.switch_play,
                'f12': physics.change_speed(1),
            })
        )
