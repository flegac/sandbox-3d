from pydantic import Field

from easy_config.my_model import MyModel
from sandbox_gui.base.config.color import Color
from sandbox_gui.base.config.fame_position import FramePosition
from sandbox_gui.base.config.frame_size import FrameSize
from sandbox_gui.base.config.text_config import TextConfig


class UiConfig(MyModel):
    name: str = 'no_name'
    frame_color: Color = Field(default=Color())
    pos: FramePosition = Field(default_factory=FramePosition)
    size: FrameSize = Field(default_factory=FrameSize)
    text_config: TextConfig = Field(default_factory=TextConfig)
    scrollbar: int = 15
    stretch: bool = True

    def params(self):
        return {
            'pos': self.pos.raw(),
            'frameColor': self.frame_color.raw(),
            'frameSize': self.size.raw(),
        }

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pos}, {self.size})'

    def __str__(self):
        return repr(self)
