from dataclasses import dataclass
from typing import Self


@dataclass
class FramePosition:
    x: int = 0
    y: int = 0

    def raw(self):
        return self.x, 0, -self.y

    def __add__(self, other: Self):
        return FramePosition(x=self.x + other.x, y=self.y + other.y)
