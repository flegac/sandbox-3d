from functools import cached_property

from panda3d.core import NodePath
from pydantic import model_validator

from python_ecs.component import Component
from sandbox.my_base import base


class CameraConfig(Component):
    fov: float = 90
    z_near: float = .1
    z_far: float = 10_000

    @cached_property
    def origin(self) -> NodePath:
        return base.render.attach_new_node('cam-origin')

    @cached_property
    def rotation_node(self) -> NodePath:
        return self.origin.attach_new_node('cam-rotation')

    @cached_property
    def translation_node(self) -> NodePath:
        return self.rotation_node.attach_new_node('cam-translate')

    @model_validator(mode='after')
    def post_init(self):
        base.disableMouse()
        base.camLens.set_fov(self.fov)
        base.camLens.set_near_far(self.z_near, self.z_far)
        base.camera.reparent_to(self.translation_node)
        return self

