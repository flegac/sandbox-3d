import random
import time
from typing import override

from panda3d.core import Vec3

from python_ecs.ecs import sim
from python_ecs.system import System
from sandbox_core.display.display_system import DisplaySystem
from sandbox_core.light.light import LightConfig
from procedural_gen.region.vec import Vec


class LightSystem(System):
    _signature = LightConfig

    @override
    def update_single(self, light: LightConfig):
        now = time.time()
        if now - light.last_update < .1:
            return

        light.last_update = now

        amplitude = light.tremblote_amplitude
        delta = (2 * random.random() - 1) * amplitude * .5
        temperature = light.light.color_temperature + delta
        temperature = min(temperature, light.color_temperature + amplitude)
        temperature = max(temperature, light.color_temperature - amplitude)
        light.light.set_color_temperature(temperature)

        var = Vec.rand_direction(light.tremblote_radius)
        light.light_node.set_pos(Vec3(*var.vec))

    @override
    def register(self, light: LightConfig):
        world = sim.find(DisplaySystem)
        world.node.set_light(light.light_node)
