from functools import cached_property

from direct.gui.DirectWaitBar import DirectWaitBar

from easy_kit.timing import time_func
from sandbox_gui.base.panel import MyWidget


class ProgressBar(MyWidget):
    range: float = 100

    @property
    def value(self):
        return self.widget['value']

    @value.setter
    def value(self, value: float):
        self.widget['value'] = value

    @cached_property
    @time_func
    def widget(self):
        widget = DirectWaitBar(
            text=self.ui.name,
            range=self.range,
            parent=self.parent.widget.canvas,
            **self.ui.text_config.to_gui()
        )
        return widget
