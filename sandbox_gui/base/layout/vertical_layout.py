from easy_kit.timing import time_func
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.layout.layout import Layout
from sandbox_gui.base.panel import Panel


class VLayout(Layout):
    @time_func
    def layout(self, panel: Panel):
        offset = self.config.x.padding
        for child in panel.children:
            child.ui.pos.y = offset
            offset += child.ui.size.height
            offset += self.config.x.margin

        new_size = FrameSize(
            width=self.max_width(panel.children),
            height=self.height_sum(panel.children)
        )
        if new_size.width > 0 and new_size.height > 0:
            panel.canvas_size = new_size
