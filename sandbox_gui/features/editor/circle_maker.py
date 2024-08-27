import math
from dataclasses import dataclass

from direct.task import Task
from panda3d.core import Vec3

from sandbox_core.entity.entity import EntityNode


@dataclass
class CircleMaker:
    entity: EntityNode
    radius: float
    items: int

    async def create(self, origin: Vec3 = None):
        origin = origin or Vec3()
        items: list[EntityNode] = []
        for i in range(self.items):
            angle = 2 * math.pi * i / self.items
            items.append(self.entity.copy(
                name=f'{self.entity.name}_{i}',
                position=origin + self.entity.position + Vec3(self.radius * math.cos(angle),
                                                              self.radius * math.sin(angle), 0)
            ))
        await Task.pause(0)

        for item in items:
            item.new_entity()
            item.node.look_at(Vec3(0, 0, item.position.z))
        await Task.pause(0)
