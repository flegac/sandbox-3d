from abc import abstractmethod

from panda3d.bullet import BulletBodyNode
from pydantic import Field

from easy_config.my_model import MyModel
from procedural_gen.region.vec import Vec


class AbstractShape(MyModel):
    name: str
    size: Vec = Field(default_factory=lambda: Vec.cast(1))

    @abstractmethod
    def create(self, body: BulletBodyNode):
        ...

    @abstractmethod
    def volume(self) -> float:
        ...
