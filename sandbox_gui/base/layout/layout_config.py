from pydantic import Field

from easy_config.my_model import MyModel


class Spaces(MyModel):
    # external distance to siblings
    padding: int = 2
    # internal distance between each child
    margin: int = 2


class LConfig(MyModel):
    x: Spaces = Field(default_factory=Spaces)
    y: Spaces = Field(default_factory=Spaces)
