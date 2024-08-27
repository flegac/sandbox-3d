from easy_kit.timing import time_func
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout import Layout
from sandbox_gui.base.panel import Panel, MyWidget
from sandbox_gui.base.widget.button import MyButton


class TabLayout(Layout):
    selected: int = 0
    menu_height: int = 25

    @time_func
    def layout(self, panel: Panel):
        for idx, child in enumerate(panel.children):
            if idx == self.selected:
                child.widget.show()
            else:
                child.widget.hide()

    def tab_select(self, index: int):
        def updater():
            self.selected = index

        return updater

    def menu_size(self, ui: UiConfig):
        return FrameSize(
            width=ui.size.width,
            height=self.menu_height
        )

    def tab_size(self, ui: UiConfig):
        return FrameSize(
            width=ui.size.width,
            height=ui.size.height - self.menu_height - 4 * self.config.y.padding
        )

    def menu_panel(self, ui: UiConfig, children: list['MyWidget']):
        from sandbox_gui.base.layout.layout_factory import L
        return L.horizontal(
            ui=UiConfig(name='menu', size=self.menu_size(ui)),
            children=[
                MyButton(text=f'{tab.ui.name}', on_click=self.tab_select(idx))
                for idx, tab in enumerate(children)
            ],
        )

    def tabs_panel(self, ui: UiConfig, children: list['MyWidget']):
        return Panel(
            ui=UiConfig(name='tabs', size=self.tab_size(ui)),
            children=children,
            layout=self
        )
