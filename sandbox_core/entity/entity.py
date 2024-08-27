from pydantic import Field

from easy_config.my_model import MyModel
from easy_kit.timing import time_func
from python_ecs.ecs import sim
from sandbox_core.display.display import Display
from sandbox_core.display.display_system import DisplaySystem
from sandbox_core.entity.health import Health
from sandbox_core.entity.lifetime import Lifetime
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.transform import ETransform


class EntityNode(MyModel):
    phys: RigidBody = Field(default_factory=RigidBody)
    display: Display | None = Field(default=None)
    lifetime: Lifetime = Field(default_factory=Lifetime)
    health: Health = Field(default_factory=Health)

    @property
    def eid(self):
        return self.phys.eid

    @time_func
    def new_entity(self):
        items = [self.phys, self.health, self.lifetime, self.display]
        items = list(filter(None, items))
        sim.new_entity(items)
        return self

    async def new_entity_async(self):
        self.new_entity()



def complex_node(transform: ETransform, entities: list[EntityNode]):
    if entities:
        transform.node.reparent_to(sim.find(DisplaySystem).node)
        for _ in entities:
            _.new_entity()
            _.phys.node.reparent_to(transform.node)
