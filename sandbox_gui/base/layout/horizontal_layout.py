from easy_kit.timing import time_func
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.layout.layout import Layout
from sandbox_gui.base.panel import Panel


class HLayout(Layout):
    @time_func
    def layout(self, panel: Panel):
        offset = self.config.y.padding
        for child in panel.children:
            child.ui.pos.x = offset
            child.ui.size = self.child_size(panel)

            offset += child.ui.size.width
            offset += self.config.y.margin

        new_size = FrameSize(
            width=self.width_sum(panel.children),
            height=self.max_height(panel.children)
        )
        if new_size.width > 0 and new_size.height > 0:
            panel.canvas_size = new_size

    def child_size(self, panel: Panel) -> FrameSize:
        n = max(1, panel.child_number)
        size = panel.ui.size.width - 2 * self.config.x.padding - (n - 1) * self.config.x.margin
        return FrameSize(size // n, panel.ui.text_config.text_scale)
