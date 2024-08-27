from python_ecs.ecs import sim
from sandbox.my_base import base
from sandbox_core.physics.phys_system import PhysSystem
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.base.widget.button import MyButton
from sandbox_gui.base.widget.slider import Slider


def graphic_panel(size: FrameSize):
    physics = sim.find(PhysSystem)

    return L.vertical(
        ui=UiConfig(name='graphics', size=size),
        children=[
            MyButton(text='wireframe', on_click=base.toggle_wireframe),
            MyButton(text='texture', on_click=base.toggle_texture),
            MyButton(text='buffer', on_click=base.bufferViewer.toggleEnable),
            MyButton(text='debug', on_click=physics.toggle_debug),
            MyButton(text='run sim', on_click=physics.switch_play),
            Slider(name='sim speed', value=.5, updater=physics.set_speed),
        ]
    )
