from direct.gui.DirectGuiBase import DirectGuiWidget

from easy_kit.timing import time_func
from sandbox.my_base import base
from sandbox_core._utils.screen import Screen


class Mouse:
    @staticmethod
    @time_func
    def in_widget(widget: DirectGuiWidget):
        x, y = Mouse.position()
        x1, x2, y1, y2 = widget.getBounds()
        return x1 <= x <= x2 and y1 <= y <= y2

    @staticmethod
    @time_func
    def position(screen_coord: bool = False):
        mouse = base.mouseWatcherNode
        x, y = mouse.getMouse()
        if screen_coord:
            screen = Screen.region()
            x = .5 * (x + 1) * screen.x.size
            y = .5 * (y + 1) * screen.y.size
        return x, y
