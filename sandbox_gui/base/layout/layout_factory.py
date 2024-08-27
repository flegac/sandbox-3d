from typing import Type

from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.horizontal_layout import HLayout
from sandbox_gui.base.layout.layout import Layout
from sandbox_gui.base.layout.tab_layout import TabLayout
from sandbox_gui.base.layout.vertical_layout import VLayout
from sandbox_gui.base.panel import MyWidget


class L:
    @staticmethod
    def vertical(ui: UiConfig, children: list[MyWidget] = None):
        return L.new_panel(layout=VLayout, ui=ui, children=children)

    @staticmethod
    def horizontal(ui: UiConfig, children: list[MyWidget] = None):
        return L.new_panel(layout=HLayout, ui=ui, children=children)

    @staticmethod
    def tabs(ui: UiConfig, children: list[MyWidget] = None):
        layout = TabLayout()
        panel = L.vertical(
            ui=ui,
            children=[
                layout.menu_panel(ui, children),
                layout.tabs_panel(ui, children)
            ]
        )
        return panel

    @staticmethod
    def new_panel(layout: Type[Layout], ui: UiConfig, children: list[MyWidget] = None):
        from sandbox_gui.base.panel import Panel
        return Panel(
            ui=ui,
            layout=layout(),
            children=children or []
        )
