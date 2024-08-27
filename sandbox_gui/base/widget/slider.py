from functools import cached_property
from typing import Callable

from direct.gui.DirectGuiGlobals import HORIZONTAL
from direct.gui.DirectSlider import DirectSlider
from direct.gui.DirectWaitBar import DirectWaitBar
from pydantic import Field

from easy_kit.event import Event
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.panel import MyWidget


class Slider(MyWidget):
    value: float = .5
    range: tuple[float, float] = (0, 1)
    updater: Callable[[float], ...] | None = None
    on_change: Event = Field(default_factory=Event)

    @property
    def interval(self):
        return self.range[1] - self.range[0]

    def get_value(self):
        return self.widget['value']

    def _on_change(self):
        self.wait_bar['value'] = self.widget['value'] - self.range[0]
        self.on_change.emit(self.get_value())
        if self.updater:
            self.updater(self.get_value())

    @property
    def widget(self):
        self.wait_bar.set_pos(self.slider.get_pos())
        return self.slider

    @cached_property
    def slider(self):
        return DirectSlider(
            range=self.range,
            value=self.value,
            thumb_frameSize=FrameSize().raw(),
            pageSize=self.interval,
            command=self._on_change,
            orientation=HORIZONTAL,
            **self.widget_params,
        )

    @cached_property
    def wait_bar(self):
        return DirectWaitBar(
            text=self.name,
            value=self.value,
            range=self.interval,
            **self.widget_params,
        )

    @property
    def widget_params(self):
        return {
            'parent': self.parent.widget.canvas,
            'frameSize': (0, 150, -10, 15),
            'frameColor': self.ui.frame_color.raw(),
            **self.ui.text_config.to_gui(),
        }
