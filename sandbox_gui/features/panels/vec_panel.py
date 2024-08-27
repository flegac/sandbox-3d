from functools import cached_property
from typing import Callable

from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.base.widget.entry import MyEntry
from sandbox_gui.base.widget.text import Text
from procedural_gen.region.vec import Vec


class VecPanel:
    def __init__(self, name: str, on_validation: Callable[[], ...] = None):
        self.on_validation = on_validation
        self.panel = L.horizontal(
            ui=UiConfig(size=FrameSize.from_size(250, 25)),
            children=[
                Text.raw(name),
                Text.raw('x'), self.x,
                Text.raw('y'), self.y,
                Text.raw('z'), self.z
            ]
        )

    def get_value(self):
        return Vec.at(
            float(self.x.text),
            float(self.y.text),
            float(self.z.text),
        )

    @cached_property
    def x(self):
        return MyEntry(text='0.0', on_validation=self.on_validation)

    @cached_property
    def y(self):
        return MyEntry(text='0.0', on_validation=self.on_validation)

    @cached_property
    def z(self):
        return MyEntry(text='0.0', on_validation=self.on_validation)
