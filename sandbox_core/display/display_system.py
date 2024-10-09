from functools import cached_property
from typing import override

from easy_kit.timing import time_func, timing
from python_ecs.system import System
from sandbox.my_base import base
from sandbox_core.display.display import Display
from sandbox_core.display.terrain_model import TerrainModel
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_lib.fog import MyFog


class DisplaySystem(System):
    _signature = Display

    @cached_property
    def node(self):
        node = base.render.attach_new_node(f'WorldRoot')
        MyFog().apply(node)
        node.reparent_to(base.render)
        return node

    @time_func
    @override
    def register(self, item: Display):
        phys = item.get(RigidBody)

        if phys:
            # FIXME: is it necessary ??
            phys.node.reparent_to(self.node)
            item.node.reparent_to(phys.node)

        if isinstance(item.model, TerrainModel):
            with timing('DisplaySystem.terrain.generate'):
                item.model.terrain.generate()
