import math
import random
from functools import cached_property

from pydantic import Field

from easy_config.my_model import MyModel
from sandbox_lib.rooms.pilar import Pilar
from sandbox_lib.rooms.wall import Wall
from procedural_gen.region.region import Region


class Room(MyModel):
    region: Region
    pilars: list[Pilar]
    doors: list[int] = Field(default_factory=lambda: [0])

    @staticmethod
    def square(region: Region, n: int = 6):
        return Room(
            region=region,
            pilars=[
                *[Pilar.at(
                    x=region.x.interpolate(i / n),
                    y=region.y.start,
                    z=region.z.size,
                ) for i in range(n)],
                *[Pilar.at(
                    x=region.x.end,
                    y=region.y.interpolate(i / n),
                    z=region.z.size,
                ) for i in range(n)],
                *[Pilar.at(
                    x=region.x.interpolate((n - i) / n),
                    y=region.y.end,
                    z=region.z.size,
                ) for i in range(n)],
                *[Pilar.at(
                    x=region.x.start,
                    y=region.y.interpolate((n - i) / n),
                    z=region.z.size,
                ) for i in range(n)],
            ],
            doors=[i * n + 2 for i in range(4)]
        )

    @staticmethod
    def circular(region: Region, n: int = 12):
        return Room(
            region=region,
            pilars=[
                *[Pilar.at(
                    x=region.x.size * math.cos(math.pi * 2 * i / n),
                    y=region.y.size * math.sin(math.pi * 2 * i / n),
                    z=region.z.size,
                ) for i in range(n)],
            ],
            doors=[i * n + random.randrange(0, n) for i in range(4)]
        )

    @cached_property
    def walls(self):
        n = len(self.pilars)
        return [
            Wall.link(self.pilars[i % n], self.pilars[(i + 1) % n])
            for i in range(n)
            # if i not in self.doors
        ]
