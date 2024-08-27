from direct.gui import DirectGuiGlobals
from panda3d.core import WindowProperties

from sandbox.my_base import base
from sandbox_gui.base.panel import Panel


class HoverHandler:
    def __init__(self):
        self.old_cursor = None

    @staticmethod
    def manage(panel: Panel):
        handler = HoverHandler()

        panel.widget['state'] = DirectGuiGlobals.NORMAL
        panel.widget.bind(DirectGuiGlobals.WITHOUT, handler.on_hover, [False])
        panel.widget.bind(DirectGuiGlobals.WITHIN, handler.on_hover, [True])

        return panel

    def on_hover(self, status: bool, pos: tuple[float, float]):
        winprops = WindowProperties().get_config_properties()
        if status:
            self.old_cursor = winprops.get_cursor_filename()
            # print(f'enter: clear {self.old_cursor}')
            winprops.clearCursorFilename()
        else:
            winprops.setCursorFilename(self.old_cursor)
            # print(f'leave: reset {self.old_cursor}')

        base.win.requestProperties(winprops)
