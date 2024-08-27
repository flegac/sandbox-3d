from typing import Callable, Iterable

from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.ui_config import UiConfig
from sandbox_gui.base.layout.layout_factory import L
from sandbox_gui.base.widget.button import MyButton


class PanelList[T]:
    def __init__(
            self,
            size: FrameSize,
            on_select: Callable[[T], ...] = None,
            namer: Callable[[T], str] = None,
    ):
        self.panel = L.vertical(UiConfig(name='scroll', size=size))
        self.on_select = on_select
        self.namer = namer or str

    def on_click(self, item: T):
        if self.on_select is None:
            return None

        def _handler():
            self.on_select(item)

        return _handler

    def update(self, items: Iterable[T]):
        for _ in self.panel.children:
            _.widget.destroy()
        self.panel.children.clear()

        self.panel.add_child(*[
            MyButton(text=f'{self.namer(item)}', on_click=self.on_click(item))
            for idx, item in enumerate(items)
        ])
        return self
