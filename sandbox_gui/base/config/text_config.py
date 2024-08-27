from panda3d.core import TextNode
from pydantic import Field

from easy_config.my_model import MyModel
from sandbox_gui.base.config.color import Color


class TextConfig(MyModel):
    # https://docs.panda3d.org/1.10/python/programming/gui/directgui/index
    text_fg: Color = Field(default=Color(0, 1, 0, .75))
    text_bg: Color = Field(default=Color())
    text_pos: tuple[int, int] = Field(default=(0, 0))
    text_scale: int = 20
    text_align: int = TextNode.ALeft

    def to_gui(self):
        return {
            'text_fg': self.text_fg.raw(),
            'text_bg': self.text_bg.raw(),
            'text_scale': self.text_scale,
            'text_align': self.text_align,
            'text_pos': self.text_pos
        }
