import time
from typing import Callable, override

from python_ecs.system import System
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.panel import Panel, MyWidget
from sandbox_gui.base.widget.text import Text
from sandbox_gui.gui_mapper import to_gui


class PanelSystem(System):
    _signature = Panel

    @override
    def update_single(self, item: Panel):
        match item:
            case Panel():
                self.update_panel(item)
            case MyWidget():
                self.update_panel_child(item)
            case _:
                raise NotImplementedError

    def update_panel(self, item: Panel):
        now = time.time()
        if item.last_update is not None and now - item.last_update < .1:
            return
        item.last_update = now

        for child in item.children:
            child.parent = item
            self.update_single(child)

        if item.layout:
            item.layout.layout(item)

        widget = item.widget
        widget.set_pos(item.ui.pos.raw())
        widget['frameColor'] = item.ui.frame_color.raw()
        widget['frameSize'] = item.ui.size.raw()
        widget['canvasSize'] = item.get_canvas_size().raw()

    def update_panel_child(self, item: MyWidget):

        if isinstance(item, Text):
            self.update_text(item)

        x, width, inv_height, y = item.widget.bounds
        item.ui.size = FrameSize(width=width, height=-inv_height + 15)
        pos = list(item.ui.pos.raw())
        pos[2] -= 20
        item.widget.set_pos(*pos)
        # item.widget['frameSize'] = item.ui.size.raw()

    def update_text(self, child: Text):
        lines = []
        for item in child.lines:
            if isinstance(item, Callable):
                item = item()
            lines.append(to_gui(item))
        full_text = '\n'.join(lines)

        child.widget.setText(full_text)
        child.ui.size.height = 20 + child.ui.text_config.text_scale * len(lines)
