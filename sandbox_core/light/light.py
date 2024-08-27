import time
from enum import Enum, auto
from functools import cached_property

from panda3d.core import PointLight, AmbientLight, DirectionalLight, Spotlight, NodePath
from pydantic import Field

from python_ecs.component import Component
from sandbox.my_base import base
from procedural_gen.region.vec import Vec


class LightType(Enum):
    ambient = auto()
    point = auto()
    spot = auto()
    directionnal = auto()

    def build(self, name: str):
        match self:
            case LightType.ambient:
                return AmbientLight(name)
            case LightType.point:
                return PointLight(name)
            case LightType.spot:
                return Spotlight(name)
            case LightType.directionnal:
                return DirectionalLight(name)


class LightConfig(Component):
    light_type: LightType = LightType.point
    shadow: bool = True
    shadow_size: int = 1024
    color_temperature: float = 6500
    max_distance: float = 10_000
    attenuation: tuple[float, float, float] = 0, 0, 0

    tremblote_amplitude: float = 100
    tremblote_radius: float = .01

    last_update: float = Field(default_factory=time.time)

    def attach(self, anchor: NodePath, offset: Vec = None):
        self.node.reparent_to(anchor)
        if offset is not None:
            self.node.set_pos(*offset.vec)
        return self

    @cached_property
    def light(self):
        light = self.light_type.build(f'light-{self.cid}')
        try:
            light.set_attenuation(self.attenuation)
        except:
            pass
        try:
            light.set_max_distance(self.max_distance)
        except:
            pass
        light.set_color_temperature(self.color_temperature)
        try:
            light.setShadowCaster(self.shadow, self.shadow_size, self.shadow_size)
        except:
            pass
        return light

    @cached_property
    def node(self) -> NodePath:
        return base.render.attach_new_node(f'root-light-{self.cid}')

    @cached_property
    def light_node(self) -> NodePath:
        return self.node.attach_new_node(self.light)

    def destroy(self):
        self.node.remove_node()
