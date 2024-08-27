from dataclasses import dataclass


@dataclass
class Color:
    r: float = 0
    g: float = 0
    b: float = 0
    a: float = 0

    def raw(self):
        return self.r, self.g, self.b, self.a
