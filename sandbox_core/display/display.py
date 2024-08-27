from functools import cached_property
from pathlib import Path

from panda3d.core import NodePath
from pydantic import Field

from easy_kit.timing import time_func
from python_ecs.component import Component
from sandbox_core.display.model_provider import ModelProvider
from sandbox_core.physics.shapes.compund_shape import AnyShape
from sandbox_core.transform import ETransform


class Display(Component):
    model: ModelProvider
    transform: ETransform = Field(default_factory=ETransform)
    is_instance: bool = False

    @staticmethod
    def from_shape(shape: AnyShape):
        from sandbox_core.display.geometry_model import GeometryModel
        return Display(
            model=GeometryModel(geometry_path=Path('shapes/cube.egg')),
            transform=ETransform(
                scale=shape.size
            )
        )

    @cached_property
    @time_func
    def node(self) -> NodePath:
        node = self.transform.node
        model_node = self.model.model_node()
        self.model.update(node=model_node)
        if self.is_instance:
            model_node.instance_to(node)
        else:
            model_node.reparent_to(node)
        return node

    @property
    def type_id(self):
        return Display
