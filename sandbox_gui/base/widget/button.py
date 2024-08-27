from functools import cached_property
from typing import Callable

from direct.gui.DirectButton import DirectButton

from sandbox_gui.base.panel import MyWidget


class MyButton(MyWidget):
    text: str
    on_click: Callable[[], ...] | None = None

    @cached_property
    def widget(self):
        widget = DirectButton(
            text=self.text,
            command=self.on_click,
            parent=self.parent.widget.canvas,
            text_scale=self.ui.text_config.text_scale,
            text_align=self.ui.text_config.text_align,
        )
        return widget
