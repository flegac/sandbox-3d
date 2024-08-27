from abc import abstractmethod

from pydantic import Field

from easy_config.my_model import MyModel
from sandbox_gui.base.layout.layout_config import LConfig


class Layout(MyModel):
    config: LConfig = Field(default_factory=LConfig)

    @abstractmethod
    def layout(self, panel: 'Panel'):
        ...

    def max_width(self, children: list['MyWidget']):
        res = 2 * self.config.x.padding
        for _ in children:
            res = max(_.ui.size.width, res)
        return res

    def max_height(self, children: list['MyWidget']):
        res = 2 * self.config.y.padding
        for _ in children:
            res = max(_.ui.size.height, res)
        return res

    def width_sum(self, children: list['MyWidget']):
        res = 2 * self.config.x.padding
        for _ in children:
            res += _.ui.size.width + self.config.x.margin
        return res

    def height_sum(self, children: list['MyWidget']):
        res = 2 * self.config.y.padding
        for _ in children:
            res += _.ui.size.height + self.config.y.margin
        return res
