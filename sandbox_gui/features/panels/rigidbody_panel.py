from functools import cached_property

from sandbox_core.physics.rigid_body import RigidBody
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.features.panels.vec_panel import VecPanel


class RigidBodyPanel:
    def __init__(self, size: FrameSize):
        self.panel = L.vertical(
            ui=UiConfig(size=size),
            children=[
                self.position.panel,
                self.rotation.panel,
                self.scale.panel,
            ]
        )

    def get_value(self):
        res = RigidBody()
        res.transform.position = self.position.get_value()
        res.transform.rotation = self.rotation.get_value()
        res.transform.scale = self.scale.get_value()
        return res

    @cached_property
    def position(self):
        return VecPanel(name='position', on_validation=self.on_validation)

    @cached_property
    def rotation(self):
        return VecPanel(name='rotation', on_validation=self.on_validation)

    @cached_property
    def scale(self):
        return VecPanel(name='scaling ', on_validation=self.on_validation)

    def on_validation(self):
        print(self.get_value())
