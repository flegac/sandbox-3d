from pathlib import Path

from easy_config.my_model import MyModel
from sandbox_core.display.display import Display
from sandbox_core.display.geometry_model import GeometryModel
from sandbox_core.entity.entity import EntityNode
from sandbox_core.entity.health import Health
from sandbox_core.physics.rigid_body import RigidBody
from sandbox_core.physics.shapes.box_shape import BoxShape
from sandbox_core.transform import ETransform


class Building(MyModel):
    name: str
    thickness: float = .25
    health: float | None = 10

    def make_entity(self, transform: ETransform):
        return EntityNode(
            phys=RigidBody(
                transform=ETransform(
                    position=transform.position,
                    rotation=transform.rotation,
                ),
                shape=BoxShape(size=.5 * transform.scale)
            ),
            display=Display(
                model=GeometryModel(geometry_path=Path('shapes/cube.egg')),
                transform=ETransform(
                    scale=.5 * transform.scale,
                )
            ),
            health=Health(
                health=self.health
            ),

        )
