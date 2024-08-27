from sandbox_core.events.event_config import EventConfig
from sandbox_core.switchable import Switchable
from sandbox_core.switcher import Switcher
from sandbox_gui.base.panel import Panel


class ControlMode(Switchable):
    def __init__(self):
        Switchable.__init__(self)
        self.events = Switcher(EventConfig)
        self.panels = Switcher(Panel)

    def _enable(self):
        self.panels.switch(True)

    def _disable(self):
        self.panels.switch(False)
