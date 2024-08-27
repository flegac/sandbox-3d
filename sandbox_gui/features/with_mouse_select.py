from direct.showbase.DirectObject import DirectObject
from loguru import logger

from python_ecs.ecs import sim
from sandbox_core._utils.ray.physic_ray import PhysicRay, RayCollision
from sandbox_gui.features.selection import Selection
from sandbox_core.entity.entity import EntityNode


class WithMouseSelect(DirectObject):
    def __init__(self):
        self.selection = Selection(EntityNode)

    @property
    def selected(self):
        return self.selection.selected

    def click_select(self):
        self._select(PhysicRay().mouse_ray())

    def _select(self, item: RayCollision):
        try:
            for _ in self.selection:
                _.node.set_color_scale((1, 1, 1, 1))
            self.selection.clear()

            if item.entity:
                self.selection.switch(item.entity)
                scale = (.9, 2, .9, 1) if item.entity in self.selection else (1, 1, 1, 1)
                item.entity.node.set_color_scale(scale)
        except Exception as e:
            logger.warning(f'{e}')

    def delete(self):
        for item in self.selection:
            sim.destroy([item.eid])

        self.selection.clear()
