from direct.task import Task
from panda3d.core import Vec3

from sandbox_core.entity.entity import EntityNode


async def grid_maker(n: int = 10, size: float = 1.):
    spacing = 4 * size
    boxes = []
    for i in range(-n, n):
        for j in range(-n, n):
            boxes.append(EntityNode(
                name=f'box_{i}_{j}',
                position=Vec3(spacing * i, spacing * j, 30),
                size=size
            ))
            await Task.pause(0)

    for box in boxes:
        box.new_entity()
