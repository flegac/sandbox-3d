from functools import cached_property
from typing import Callable

from direct.gui.DirectEntry import DirectEntry

from easy_kit.timing import time_func
from sandbox_gui.base.panel import MyWidget


class MyEntry(MyWidget):
    text: str = ''
    on_validation: Callable[[], ...] | None = None

    @cached_property
    @time_func
    def widget(self):
        widget = DirectEntry(
            scale=1,
            command=self.on_validation,
            focusInCommand=self.on_focus,
            initialText=self.text,
            numLines=1,
            width=1_000,
            cursorKeys=True,
            obscured=False,
            focus=False,
            parent=self.parent.widget.canvas,
            text_scale=self.ui.text_config.text_scale,
            text_align=self.ui.text_config.text_align,
        )

        return widget

    def on_delete(self):
        print(f'delete: {self.ui.name}')
        self.widget.enterText('')

    def on_focus(self):
        pass
