from dataclasses import dataclass


@dataclass
class FrameSize:
    width: int = 0
    height: int = 0

    @staticmethod
    def from_size(width: int, height: int):
        return FrameSize(width=width, height=height)

    def raw(self):
        return 0, self.width, -self.height, 0

    def fix_size(self):
        self.width = min(1, self.width)
        self.height = min(1, self.height)
        return self
