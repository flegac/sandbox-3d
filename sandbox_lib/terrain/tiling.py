import math
from typing import NamedTuple, Self

from easy_kit.timing import time_func
from procedural_gen.region.vec import Vec


class Coord(NamedTuple):
    x: int
    y: int

    def dist(self, other: Self):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx * dx + dy * dy)


class Tiling[T]:
    def __init__(self, size: int):
        self.cache: dict[Coord, T] = {}
        self.size: float = size

    def to_coord(self, vec: Vec):
        return Coord(
            x=math.ceil((vec.x - self.size * .5) / self.size),
            y=math.ceil((vec.y - self.size * .5) / self.size)
        )

    def to_vec(self, coord: Coord):
        return Vec.at(coord.x * self.size, coord.y * self.size)

    def create(self, coord: Coord, tile: T):
        self.cache[coord] = tile

    @time_func
    def cells(self, center: Coord, radius: int = 2) -> set[Coord]:
        if center is None:
            return set()
        res = set()
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                coord = Coord(x=center.x + x, y=center.y + y)
                if center.dist(coord) <= radius + .5:
                    res.add(coord)
        return res

    def get(self, coord: Coord | Vec) -> T | None:
        if isinstance(coord, Vec):
            coord = self.to_coord(coord)
        return self.cache.get(coord, None)

    def __contains__(self, coord: Coord):
        return coord in self.cache
