from panda3d.core import Vec3
from pydantic import Field

from sandbox.my_base import base
from sandbox_core._utils.coord_manager import CoordManager
from sandbox_core.events.event_config import EventConfig
from sandbox_core.physics.rigid_body import RigidBody
from procedural_gen.region.vec import Vec

KEY_BINDING = {
    'forward': 'z',
    'reverse': 's',
    'left': 'q',
    'right': 'd',
    'turnLeft': 'a',
    'turnRight': 'e',
    'up': 'space',
    'down': 'g',
}


class PhysicController(EventConfig):
    power: float
    status_binding: dict[str, str] = KEY_BINDING
    targets: list[RigidBody] = Field(default_factory=list)
    jump_target: list[RigidBody] = Field(default_factory=list)
    rotate_target: list[RigidBody] = Field(default_factory=list)
    _force: Vec3 = Vec3()
    _torque: Vec3 = Vec3()

    def reset(self):
        self._force = Vec3()
        self._torque = Vec3()

    def referential(self):
        # return Vec.y_axis(), Vec.z_axis(), Vec.x_axis()
        return CoordManager(base.camera).get_local()

    def force(self, ref: tuple[Vec, Vec, Vec]):
        forward, up, right = ref

        forward = forward * self._force.x
        right = right * self._force.y
        up = Vec3(0, 0, 1) * self._force.z

        return (forward + right + up)

    def torque(self, ref: tuple[Vec, Vec, Vec]):
        forward, up, right = ref
        forward = forward * self._torque.x
        right = right * self._torque.y
        up = Vec3(0, 0, 1) * self._torque.z

        return (forward + right + up) * .025

    def update(self):
        self.input_handler()
        ref = self.referential()
        torque = self.torque(ref)
        force = self.force(ref)

        for phys in self.targets:
            phys.apply_central_force(force * phys.mass * Vec.at(1, 1, 0))
        for phys in self.jump_target:
            phys.apply_central_force(force * phys.mass * Vec.z_axis())
        for _ in self.rotate_target:
            _.apply_torque(torque * _.mass)

    def input_handler(self):
        self.reset()

        if self.is_set('forward'):
            self._force.x += self.power
        if self.is_set('reverse'):
            self._force.x -= self.power

        if self.is_set('right'):
            self._force.y += self.power
        if self.is_set('left'):
            self._force.y -= self.power

        if self.is_set('up'):
            self._force.z += self.power
        if self.is_set('down'):
            self._force.z -= self.power

        if self.is_set('turnRight'):
            self._torque.z -= self.power
        if self.is_set('turnLeft'):
            self._torque.z += self.power
