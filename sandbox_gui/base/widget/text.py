from functools import cached_property
from typing import Callable

from direct.gui.DirectLabel import DirectLabel

from easy_kit.timing import time_func
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.panel import MyWidget


class Text(MyWidget):
    lines: list[str | Callable[[], ...]]

    @staticmethod
    def raw(text: str):
        res = Text(lines=[text])
        res.ui.size = FrameSize(width=10 * len(text), height=20)
        return res

    def write(self, text: str | Callable[[], ...]):
        self.lines.append(text)

    @cached_property
    @time_func
    def widget(self):
        widget = DirectLabel(
            parent=self.parent.widget.canvas,
            text='',
            text_wordwrap=self.parent.ui.size.width / self.ui.text_config.text_scale,
            **self.ui.params(),
            **self.ui.text_config.to_gui(),
        )
        return widget
