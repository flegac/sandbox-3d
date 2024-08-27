from functools import cached_property

from direct.gui.DirectScrolledFrame import DirectScrolledFrame
from pydantic import Field

from python_ecs.component import Component
from python_ecs.ecs import sim
from sandbox.my_base import base
from sandbox_core._utils.mouse import Mouse
from sandbox_core.switchable import Switchable
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout import Layout


class MyWidget(Component):
    name: str = 'no_name'
    parent: 'Panel | None' = None
    ui: UiConfig = Field(default_factory=UiConfig)

    @property
    def parent_canvas(self):
        if self.parent:
            return self.parent.widget.canvas

        return base.pixel2d


class Panel(MyWidget, Switchable):
    layout: Layout | None = None
    canvas_size: FrameSize | None = None
    last_update: float | None = None
    children: list[MyWidget] = Field(default_factory=list)

    def add_child(self, *children: MyWidget):
        for child in children or []:
            assert isinstance(child, MyWidget), f'{type(child)}'
            child.parent = self
            self.children.append(child)

        return self

    @property
    def child_number(self):
        return len(self.children)

    @cached_property
    def widget(self) -> DirectScrolledFrame:
        widget = DirectScrolledFrame(
            parent=self.parent_canvas,
            canvasSize=self.get_canvas_size().raw(),
            scrollBarWidth=self.ui.scrollbar,
            horizontalScroll_frameSize=(0, 0, 0, 0),
            **self.ui.params(),
        )
        for child in self.children:
            child.parent = self

        # widget.bind(WHEEL_UP, Common.handleMouseScroll, [result, 1])
        # widget.thumb.bind(WHEEL_UP, Common.handleMouseScroll, [result, 1])
        # widget.bind(WHEEL_DOWN, Common.handleMouseScroll, [result, -1])
        # widget.thumb.bind(WHEEL_DOWN, Common.handleMouseScroll, [result, -1])

        # if 'scroll' in self.name:
        #     widget.accept('wheel_up', self.on_scroll, [False])
        #     widget.accept('wheel_down', self.on_scroll, [True])
        #     # widget.verticalScroll.bind(DirectGuiGlobals.WHEELDOWN, self.on_scroll)
        #     # widget.verticalScroll.bind(DirectGuiGlobals.WHEELUP, self.on_scroll)

        return widget

    def _enable(self):
        self.widget.show()
        sim.new_entity(self)

    def _disable(self):
        self.widget.hide()
        sim.destroy([self.eid])

    def on_scroll(self, down):
        # https://discourse.panda3d.org/t/scrolling-scrollers-via-the-mouse-wheel/26625/4
        # https://discourse.panda3d.org/t/directgui-mouse-wheel-scrolling/25429/3
        print(f'scroll: {self.ui.name}')
        scroll_bar: DirectScrolledFrame = self.widget.verticalScroll

        if Mouse.in_widget(self.widget):
            modifier = -1 if down else 1
            scroll_bar.setValue(scroll_bar.getValue() - modifier * scroll_bar['pageSize'])

    def get_canvas_size(self):
        if not self.canvas_size:
            self.canvas_size = self.ui.size
        return self.canvas_size
